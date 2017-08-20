from pprint import pprint
import os
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['laters']


PREFIX_PATH = './img'
APP = ClarifaiApp(api_key='cd507789e04b4566938bd00424f8fda5')

def imgExtractor ():
    img1 = './img/140149598.jpg'
    img2 = './img/140149599.jpg'

    # # get the general model
    # model = APP.models.get("general-v1.3")

    # # predict with the model
    # abc = model.predict_by_url(url='..\\data\\Challenge - Matching Tool\\tool1\\140149598.jpg')

    # print(abc)

    image1 = ClImage(file_obj=open(img1, 'rb'))
    image2 = ClImage(file_obj=open(img2, 'rb'))

    model = APP.models.get('general-v1.3')
    general_result = model.predict([image1])
    gd1 = general_result['outputs'][0]['data']
    model = APP.models.get('color')
    color_result = model.predict([image1])
    cd1 = color_result['outputs'][0]['data']
    model = APP.models.get('apparel')
    apparel_result = model.predict([image1])
    ad1 = apparel_result['outputs'][0]['data']

    model = APP.models.get('general-v1.3')
    general_result = model.predict([image2])
    gd2 = general_result['outputs'][0]['data']
    model = APP.models.get('color')
    color_result = model.predict([image2])
    cd2 = color_result['outputs'][0]['data']
    model = APP.models.get('apparel')
    apparel_result = model.predict([image2])
    ad2 = apparel_result['outputs'][0]['data']

    img1_obj = {"gd": gd1, "cd": cd1, "ad": ad1}
    img2_obj = {"gd": gd2, "cd": cd2, "ad": ad2}

    return {"img1": img1_obj, "img2": img2_obj}



def bulkInsert(start, end, path, filesAry):
    apparel_Model = APP.models.get('apparel')
    imgAry = []
    print(filesAry)
    try:
        for filename in filesAry[start:end]:
            obj = open(os.path.join(path, filename), "rb")
            #print(os.path.join(path, filename))
            conceptObj = apparel_Model.predict([ClImage(file_obj=obj)])
            #print("enter")
            mainConcept = ''
            for key in conceptObj['outputs'][0]['data']['concepts']:
                mainConcept = key['name']
                break

            imgAry.append(
                ClImage(
                    file_obj=obj,
                    image_id=filename,
                    concepts=[mainConcept],
                    metadata={'key':mainConcept}
                )
            )
            # break
    except:
        pass
    #print(imgAry[:10])
    APP.inputs.bulk_create_images(imgAry)

def bulkInput():
    filesAry = []
    path = ''

    for path, dirs, files in os.walk('./img'):
        filesAry = files
        path = path

    
    bulkInsert(0, 60, path, filesAry)
    # bulkInsert(100, 200, path, filesAry)
    # bulkInsert(200, 300, path, filesAry)
    # bulkInsert(300, 400, path, filesAry)
    
    # print(imgAry[:20])
    return

def input(filename=''):
    apparel_Model = APP.models.get('apparel')
    obj = open(filename, "rb")
    conceptObj = apparel_Model.predict([ClImage(file_obj=obj)])
    mainConcept = ''
    for key in conceptObj['outputs'][0]['data']['concepts']:
        mainConcept = key['name']
        break

    APP.create_image_from_filename(filename, concepts=[mainConcept])
    return

def search (filename='./img/140149599.jpg'):
    fio = open(filename, 'rb')
    abc = APP.inputs.search_by_image(fileobj=fio, page=1, per_page=5)
    # print(vars(abc[0]))
    ary = []
    for item in abc:
        print(item.input_id)
        print(item.score)
        ary.append({"input_id":item.input_id, "score":item.score})

    return ary

def searchAndUpload ():
    for path, dirs, files in os.walk('./test'):
        for filename in files:
            fio = open(os.path.join(path, filename), 'rb')
            abc = APP.inputs.search_by_image(fileobj=fio)
            
            ary = []
            searchResAry = []
            for item in abc:
                obj = {}
                obj['other_id'] = item.input_id
                obj['score'] = item.score
                ary.append(obj)
                searchResAry.append(int(item.input_id.replace(".jpg", "")))
            img_searchResAry = {'id':int(filename.replace(".jpg", "")), "match": ary, "searchResult":searchResAry}
            result = db.test_final.update_one(
                {"Unique_No": int(filename.replace(".jpg", ""))},
                {
                    "$set": {
                        "searchResult2":searchResAry
                    }
                }
            )
            print("e")

    # cursor = db.test_final.update_one(
    #     {"Unique_No": 140168573},
    #     {
    #         "$set": {
    #             "abc":[1,1,1]
    #         }
    #     }
    # )
    # print(cursor)

def delAll():
    APP.inputs.delete_all()

def uploadTrain():
    apparel_Model = APP.models.get('apparel')
    imgAry = []
    import mongo
    data = mongo.getTrain()
    print(len(data))
    for item in data[401:]:
        #print(item['Unique_No'])
        try:
            obj = open('./img/'+ str(item['Unique_No']) + '.jpg', "rb")
            # print(obj)
            conceptObj = apparel_Model.predict([ClImage(file_obj=obj)])
            mainConcept = ''
            for key in conceptObj['outputs'][0]['data']['concepts']:
                mainConcept = key['name']
                break

            imgAry.append(
                ClImage(
                    file_obj=obj,
                    image_id=str(item['Unique_No']) + '.jpg',
                    concepts=[mainConcept],
                    metadata={'key':mainConcept}
                )
            )
        except Exception as e:
            print(e)
            pass
        #print(imgAry[:10])
    APP.inputs.bulk_create_images(imgAry)

# bulkInput()
# search()
# delAll()
# uploadTrain()

# searchAndUpload()