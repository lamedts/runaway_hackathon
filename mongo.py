from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['laters']
train = db.laters
test = db.test


def getTrain():
    data = []
    cursor = train.find({}, {"_id": 0, "update_time": 0})

    for item in cursor:
        print(item)
        data.append(item)

    return data

def getTest():
    data = []
    cursor = train.find({}, {"_id": 0, "update_time": 0})

    for item in cursor:
        print(item)
        data.append(item)

    return data

def getImgMatch():
    data = []
    cursor = db.img_match.find({}, {"_id": 0, "update_time": 0})

    for item in cursor:
        print(item)
        data.append(item)

    return data

def getInfoMatch():
    data = []
    cursor = db.img_match.find({}, {"_id": 0, "update_time": 0})

    for item in cursor:
        print(item)
        data.append(item)

    return data