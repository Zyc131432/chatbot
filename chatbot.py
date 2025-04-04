from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackContext)
import os
from dotenv import load_dotenv
import logging
from ChatGPT import HKBU_ChatGPT
import firebase_admin
from firebase_admin import credentials, firestore

def main():
    load_dotenv(dotenv_path='.env')
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    firebase_key_path = os.getenv("FIREBASE_KEY_PATH")

    updater = Updater(token=telegram_token, use_context=True)
    dispatcher = updater.dispatcher

    cred = credentials.Certificate(firebase_key_path)
    firebase_admin.initialize_app(cred)
    global db
    db = firestore.client()  # 获取 Firestore 客户端
    # dispatcher for chatgpt
    global chatgpt
    chatgpt = HKBU_ChatGPT()
    chatgpt_handler = MessageHandler(Filters.text & (~Filters.command),
                                     equiped_chatgpt)

    # 注册命令处理器
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("training_plan", training_plan))
    dispatcher.add_handler(CommandHandler("recipe", recipe))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), handle_response))
    dispatcher.add_handler(chatgpt_handler)
    # To start the bot:
    updater.start_polling()
    updater.idle()


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("🏋️ 欢迎使用健身助手！可用命令：\n"
                                    "/training_plan - 获取训练计划\n"
                                    "/recipe - 获取营养食谱\n"
                                    "其他健身相关的问题请直接输入自然语言"
                              )


# 训练计划命令处理
def training_plan(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [KeyboardButton("三分化训练"), KeyboardButton("五分化训练")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "请选择训练类型：",
        reply_markup=reply_markup
    )
    context.user_data['awaiting_training_type'] = True


# 食谱命令处理
def recipe(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [KeyboardButton("增肌食谱"), KeyboardButton("减脂食谱")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "请选择食谱类型：",
        reply_markup=reply_markup
    )
    context.user_data['awaiting_recipe_type'] = True


# 处理用户选择
def handle_response(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    user_data = context.user_data

    if user_data.get('awaiting_training_type'):
        plan_ref = db.collection('training_plans').where('name', '==', text).limit(1)
        plans = plan_ref.stream()

        if plans:
            for plan in plans:
                plan_data = plan.to_dict()
                response = "🏋️ 您的训练计划：\n\n"
                for session in plan_data['sessions']:
                    response += f"【{session['day']}】\n"
                    for exercise in session['exercises']:
                        response += f"- {exercise['name']}: {exercise['sets']}组 x {exercise['reps']}次\n"
                    response += "\n"
                update.message.reply_text(response)
                # 保存到用户历史记录（可选）
                save_user_history(update.effective_user.id, text)
        else:
            update.message.reply_text("⚠️ 未找到相关训练计划")
        user_data['awaiting_training_type'] = False

    elif user_data.get('awaiting_recipe_type'):
            # 从 Firestore 获取食谱
            recipe_ref = db.collection('recipes').where('name', '==', text).limit(1)
            recipes = recipe_ref.stream()

            if recipes:
                for recipe in recipes:
                    recipe_data = recipe.to_dict()
                    response = "🍽️ 今日推荐食谱：\n\n"
                    response += f"⭐ {recipe_data['name']}：\n"
                    response += f"描述：{recipe_data['description']}\n"
                    response += "食材：\n" + "\n".join(recipe_data['ingredients']) + "\n"
                    response += "步骤：\n" + "\n".join(recipe_data['instructions']) + "\n"
                    update.message.reply_text(response)
                    # 生成购物清单（可选）
                    generate_shopping_list(update.effective_user.id, recipe_data['ingredients'])
            else:
                update.message.reply_text("⚠️ 未找到相关食谱")
            user_data['awaiting_recipe_type'] = False

    else:
            # 其他消息处理（原GPT逻辑）
        response = equiped_chatgpt(update, context)
        update.message.reply_text(response)

def save_user_history(user_id, plan_name):
    user_ref = db.collection('users').document(str(user_id))
    user_ref.set({
        'last_plan': plan_name,
        'timestamp': firestore.SERVER_TIMESTAMP
    }, merge=True)

def generate_shopping_list(user_id, ingredients):
    shopping_list_ref = db.collection('shopping_lists').document(str(user_id))
    shopping_list_ref.set({
        'ingredients': ingredients,
        'timestamp': firestore.SERVER_TIMESTAMP
    }, merge=True)

def equiped_chatgpt(update, context):
    global chatgpt
    reply_message = chatgpt.submit(update.message.text)
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

if __name__ == '__main__':
    main()