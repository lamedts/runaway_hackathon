from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['laters']


import pandas as pd
import json
import mongo

test_result = pd.read_json(json.dumps(mongo.getTest()))
train_data = pd.read_json(json.dumps(mongo.getTrain()))

def get_matched_json(new_unique_id):
    # print(type(test_result))
    # print(test_result['Unique_No'])
    # print(test_result.loc[test_result['Unique_No'] == int(new_unique_id)])
    df = test_result.loc[test_result['Unique_No'] == new_unique_id, ['searchResult', 'searchResult2']]
    commonunid = []
    # print(df['searchResult2'].iloc[0])
    # print(df['searchResult'])
    # test = [x for x in df['searchResult'] if x in df['searchResult2']]
    # print(test)

    matches = [x for x in df['searchResult'].iloc[0] if x in df['searchResult2'].iloc[0]]

    result_data = pd.DataFrame()
    for match in matches:
        matchdf = train_data[train_data['Unique_No'] == match]
        result_data = pd.concat([result_data, matchdf], axis = 0)
    vendorjsonlist = []
    try:
        for vendor in result_data['Vendor_No'].unique():
            vendor_result = result_data[result_data['Vendor_No'] == vendor]
            order_json = []
            # print(vendor_result.shape)
            for index, row in vendor_result.iterrows():
                order_json.append(json.loads(row.to_json()))
            vendorjsonlist.append({
                'Vendor_No': vendor_result.iloc[0]['Vendor_No'],
                'Country_Cd': vendor_result.iloc[0]['Country_Cd'],
                'items': order_json
            })
        # with open('sample.json', 'w') as outfile:
        #     json.dump(vendorjsonlist, outfile, indent = 4)
    except:
        vendorjsonlist = None
    # print(vendorjsonlist)
    return vendorjsonlist

def search(id):
    data = []
    # cursor = db.test_final.find({"Unique_No": int(id)}, {"_id": 0, "update_time": 0})

    # for item in cursor:
    #     print(item)
    #     # data.append(item['id'].replace(".jpg", ""))

    # # print(data)
    
    return get_matched_json(int(id))

# print(get_matched_json(int(140168737)))

# def getAllTestImg():
#     import mongo
#     data = mongo.getTrain()
#     for item in data:
#         print(item['Unique_No'])

#     return 
# # getAllTestImg()