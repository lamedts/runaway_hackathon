import pandas as pd
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
        

def basicFilter(test, train):
    for index, row in test.iterrows():
        newdata = test[test['Unique.No'] == row['Unique.No']].iloc[0]
        result = train[train['TypeProduct_Desc'] == newdata['TypeProduct_Desc']]
        result = result[result['Retail_Class_Desc'] == newdata['Retail_Class_Desc']]
        result = result[result['Retail_SubClass_Desc'] == newdata['Retail_SubClass_Desc']]
        result['scores'] = 0
        for col in ['Main_Fabric_Desc', 'StyleDescription', 'Wash', 'Year', 'Silhouette_Cd']:
            if col != 'Year':
                result['{}_score'.format(col)] = result[col].apply(lambda x: similar(row[col], x) if x is not None and row[col] is not None else 0 )
            else:
                result['{}_score'.format(col)] = result[col].apply(lambda x: similar(row[col], x.split(' ')[0]) if x is not None and row[col] is not None else 0 )
            result['scores'] = result['scores'] + result['{}_score'.format(col)]
            result.drop('{}_score'.format(col), axis = 1, inplace = True)
        result['scores'] = result['scores'].map(lambda x: x/5)
        result = result.sort_values('scores', ascending = False)
        if len(result['Unique.No'])<0:
            test.loc[index, 'searchResult'] = str(result['Unique.No'].tolist())[1:-1]
        else:
            test.loc[index, 'searchResult'] = str(result['Unique.No'][:10].tolist())[1:-1]
    return test

train_data = pd.read_json('train_data.json')
test_data = pd.read_json('test_data.json')
test_result = basicFilter(test_data, train_data)