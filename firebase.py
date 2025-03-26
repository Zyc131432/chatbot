import firebase_admin
from firebase_admin import credentials, firestore

# 初始化 Firebase
def initialize_firebase():
    cred = credentials.Certificate('/Users/ci1/Desktop/chatbot_db.json')  # 替换为你的 Firebase 服务账户密钥文件路径
    firebase_admin.initialize_app(cred)
    return firestore.client()

# 批量写入训练计划
def batch_add_training_plans(db):
    # 训练计划数据
    training_plans = [
        {
            'id': 'plan1',
            'name': '三分化训练',
            'description': '适合中级健身者的三分化训练计划。',
            'level': 'intermediate',
            'duration': '6 weeks',
            'days_per_week': 3,
            'split': ['push', 'pull', 'legs'],
            'sessions': [
                {
                    'day': 'Monday',
                    'type': 'push',
                    'exercises': [
                        {'name': '平板杠铃卧推', 'sets': 4, 'reps': '8-12'},
                        {'name': '哑铃肩推', 'sets': 3, 'reps': '10-12'},
                        {'name': '绳索下压', 'sets': 3, 'reps': '12-15'}
                    ]
                },
                {
                    'day': 'Wednesday',
                    'type': 'pull',
                    'exercises': [
                        {'name': '引体向上', 'sets': 4, 'reps': '8-10'},
                        {'name': '杠铃划船', 'sets': 4, 'reps': '8-12'},
                        {'name': '哑铃弯举', 'sets': 3, 'reps': '10-12'}
                    ]
                },
                {
                    'day': 'Friday',
                    'type': 'legs',
                    'exercises': [
                        {'name': '深蹲', 'sets': 4, 'reps': '8-12'},
                        {'name': '罗马尼亚硬拉', 'sets': 4, 'reps': '8-10'},
                        {'name': '腿举', 'sets': 3, 'reps': '10-12'}
                    ]
                }
            ]
        },
        {
            'id': 'plan2',
            'name': '五分化训练',
            'description': '适合高级健身者的五分化训练计划。',
            'level': 'advanced',
            'duration': '8 weeks',
            'days_per_week': 5,
            'split': ['chest', 'back',  'shoulders', 'arms', 'legs'],
            'sessions': [
                {
                    'day': 'Monday',
                    'type': 'chest',
                    'exercises': [
                        {'name': '平板杠铃卧推', 'sets': 4, 'reps': '8-12'},
                        {'name': '上斜哑铃卧推', 'sets': 3, 'reps': '10-12'},
                        {'name': '蝴蝶机夹胸', 'sets': 3, 'reps': '12-15'}
                    ]
                },
                {
                    'day': 'Tuesday',
                    'type': 'back',
                    'exercises': [
                        {'name': '引体向上', 'sets': 4, 'reps': '8-10'},
                        {'name': '杠铃划船', 'sets': 4, 'reps': '8-12'},
                        {'name': '坐姿划船', 'sets': 3, 'reps': '10-12'}
                    ]
                },
                {
                    'day': 'Wednesday',
                    'type': 'shoulder',
                    'exercises': [
                        {'name': '哑铃推肩', 'sets': 4, 'reps': '8-10'},
                        {'name': '面拉', 'sets': 4, 'reps': '8-12'},
                        {'name': '侧平举', 'sets': 5, 'reps': '10-15'}
                    ]
                },
                {
                    'day': 'Thursday',
                    'type': 'arms',
                    'exercises': [
                        {'name': '杠铃弯举', 'sets': 4, 'reps': '8-10'},
                        {'name': '绳索下压', 'sets': 4, 'reps': '8-12'},
                        {'name': '垂式弯举', 'sets': 4, 'reps': '10-12'}
                    ]
                },
                {
                    'day': 'Friday',
                    'type': 'legs',
                    'exercises': [
                        {'name': '深蹲', 'sets': 4, 'reps': '8-12'},
                        {'name': '罗马尼亚硬拉', 'sets': 4, 'reps': '8-10'},
                        {'name': '腿举', 'sets': 3, 'reps': '10-12'}
                    ]
                },
            ]
        }
    ]

    # 创建批量写入对象
    batch = db.batch()

    # 遍历训练计划数据并添加到批量写入
    for plan in training_plans:
        doc_ref = db.collection('training_plans').document(plan['id'])
        batch.set(doc_ref, plan)

    # 提交批量写入
    batch.commit()
    print("训练计划批量写入成功！")

# 批量写入食谱
def batch_add_recipes(db):
    # 食谱数据
    recipes = [
        {
            'id': 'recipe1',
            'name': '增肌食谱',
            'description': '高蛋白增肌食谱，适合健身者。',
            'calories': 500,
            'ingredients': ['鸡胸肉 200g', '糙米 100g', '西兰花 150g', '鸡蛋 2个'],
            'instructions': [
                '鸡胸肉煮熟切块。',
                '糙米煮熟。',
                '西兰花焯水。',
                '将所有食材混合，加入调味料。'
            ]
        },
        {
            'id': 'recipe2',
            'name': '减脂食谱',
            'description': '低卡路里减脂食谱，适合减脂期。',
            'calories': 300,
            'ingredients': ['鸡胸肉 150g', '生菜 100g', '番茄 1个', '黄瓜 1根'],
            'instructions': [
                '鸡胸肉煮熟切块。',
                '蔬菜洗净切好。',
                '将所有食材混合，加入低脂调味料。'
            ]
        }
    ]

    # 创建批量写入对象
    batch = db.batch()

    # 遍历食谱数据并添加到批量写入
    for recipe in recipes:
        doc_ref = db.collection('recipes').document(recipe['id'])
        batch.set(doc_ref, recipe)

    # 提交批量写入
    batch.commit()
    print("食谱批量写入成功！")

# 主函数
if __name__ == '__main__':
    # 初始化 Firebase
    db = initialize_firebase()

    # 批量写入训练计划和食谱
    batch_add_training_plans(db)
    batch_add_recipes(db)