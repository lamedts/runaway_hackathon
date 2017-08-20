import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import plotly 
import pandas as pd

import mongo
import json
test_result = pd.read_json(json.dumps(mongo.getTest()))
train_data = pd.read_json(json.dumps(mongo.getTrain()))

plotly.tools.set_credentials_file(username='qfnreneeleung', api_key='IHR5ewSbmpkeCJiWkkvu')

def get_chart(vendorlist):
    vendorlist =vendorlist[1:-1].replace('"', "").split(',')
    # print("!!!!!!!!!!!!!!!!!!", vendorlist)
    report_data = pd.DataFrame()
    for vendor in vendorlist:
        report_data = pd.concat([report_data,train_data[train_data['Vendor_No'] == vendor]], axis = 0)
    dimension = ['Year', 'Vendor_No']
    plot_data = []
    for col in ['TypeProduct_Desc','Retail_Class_Desc', 'Gender_Desc']:
        dimension2 = ['Vendor_No', col, 'Year']
        plot_data.append(report_data.groupby(dimension2).count()['Unique_No'].reset_index())

    subplot_titles = ()
    for col in [' (by Product Type)','(by Retail Class)', '(by Gender)']:
        for Vendor in vendorlist:
            subplot_titles = subplot_titles + ('{} {}'.format(Vendor, col),)

    fig = plotly.tools.make_subplots(rows = 3, cols=len(vendorlist), 
                                     shared_xaxes = True, shared_yaxes=True, 
                                     subplot_titles=subplot_titles)

    j = 1
    for data in plot_data:
        i = 1
        # print(">>>>>",vendorlist)
        # print(data)
        for Vendor in vendorlist:
        # for Vendor in vendorlist[1:-1].split(','):
            # print(">>>>>",Vendor)
            # print(">>>>>",data['Vendor_No'])
            df1 = data[data['Vendor_No'] == Vendor]

            for cat in df1.ix[:,1].unique():
                df2 = df1[df1.ix[:,1] == cat]
                # print(sorted(df2['Year'], key=lambda x: int(x.split(' ')[1])))
                fig.append_trace(go.Bar(
                    x=sorted(df2['Year'], key=lambda x: int(x.split(' ')[1])),
                    y=df2['Unique_No'],
                    name= cat
                ), j,i)

            i = i + 1
        j = j + 1

    fig['layout'].update(title='Vendor Comparision', barmode = 'stack')


    return plotly.tools.get_embed(py.plot(fig, filename = 'temp', auto_open = False))

#sample
# print(get_chart('["Vendor 14","Vendor 7"]'))
# print(get_chart(["Vendor 14","Vendor 7"]))