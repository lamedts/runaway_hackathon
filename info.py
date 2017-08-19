from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['laters']
train = db.laters
test = db.test



data = []
cursor = db.img_match.find({}, {"_id": 0, "update_time": 0})

for item in cursor:
    print(item)
    data.append(item['id'].replace(".jpg", ""))

print(data)