import flask
import requests
from flask import request
import redis
import collections
import json
import numpy as np
import pygal
from pygal.style import LightSolarizedStyle as st
from pygal.style import LightGreenStyle as st2
from pygal.style import DarkGreenStyle as st3

app = flask.Flask(__name__)

##This method creates a bar chart when we
##load our web page using the pygal module
@app.route("/")
def histogram():
    start14=['2014-01-01','2014-02-01','2014-03-01','2014-04-01','2014-05-01','2014-06-01','2014-07-01','2014-08-01','2014-09-01','2014-10-01','2014-11-01','2014-12-01']
    ends14=['2014-02-01','2014-03-01','2014-04-01','2014-05-01','2014-06-01','2014-07-01','2014-08-01','2014-09-01','2014-10-01','2014-11-01','2014-12-01','2015-01-01']
    starts=['2015-01-01','2015-02-01','2015-03-01','2015-04-01','2015-05-01','2015-06-01','2015-07-01','2015-08-01','2015-09-01','2015-10-01','2015-11-01','2015-12-01','2016-01-01']
    ends=['2015-02-01','2015-03-01','2015-04-01','2015-05-01','2015-06-01','2015-07-01','2015-08-01','2015-09-01','2015-10-01','2015-11-01','2015-12-01','2016-01-01','2016-02-01']
##    starts=start14+starts
##    ends=ends14+ends
    terrai_values=[]
    months=['January','February','March','April','May','June','July','August','September','October','November','December','January']
    for i in range(len(starts)):
        ep='http://api.globalforestwatch.org/forest-change/imazon-alerts/admin/bra/?period='+starts[i]+','+ends[i]
        pl={"geojson":'{"type":"Polygon","coordinates":[[[12.8,8.9],[13.3,-7.3],[32.5,-6.6],[32.5,7.7],[12.8,8.9]]]}'}
        res=requests.post(ep,pl)
        r=res.json()
        s=r['value']
        for i in s:
            if i['data_type']=='defor':
                terrai_values.append(i['value'])

    ep='http://api.globalforestwatch.org/forest-change/umd-loss-gain/admin/bra/?period=2015-12-01,2016-01-01'
    pl={"geojson":'{"type":"Polygon","coordinates":[[[12.8,8.9],[13.3,-7.3],[32.5,-6.6],[32.5,7.7],[12.8,8.9]]]}'}
    res=requests.post(ep,pl)
    print res
    r=res.json()
    net_values=[]
    years=[]
    s=r['years']
    for i in s:
        loss=i['loss']
        gain=i['gain']
        if gain is None:
            gain=0
        net=loss-gain
        net_values.append(net)
        years.append(i['year'])
    coffee=[]
    years=['2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014']
    epComm='https://www.quandl.com/api/v3/datasets/OFDP/FUTURE_KC1/data.json?start_date=2001-01-01&end_date=2014-01-31&column_index=4&collapse=annual&order=asc&api_key=SQx81iJsvvNB_CfFP-5q'
    result=requests.get(epComm)
    r=result.json()
    s=r['dataset_data']
    for i in s['data']:
        coffee.append(i[1])
    title='Forest loss in Brazil from January 2015'
##    we create the bar chart here:
    bar_chart = pygal.Bar(width=1200, height=600,
                          explicit_size=True, title=title, style=st)
##    we add the candidates to the x axis of the chart
    bar_chart.x_labels = months

##    The probability values are added to the y axis of the chart
    bar_chart.add('Hectares', terrai_values)

    titlec='Coffee prices over 2015'
##    we create the bar chart here:
    bar_chartc = pygal.Bar(width=1200, height=600,
                          explicit_size=True, title=titlec, style=st3)
##    we add the candidates to the x axis of the chart
    bar_chartc.x_labels = years

##    The probability values are added to the y axis of the chart
    bar_chartc.add('Price', coffee)


    title2='Annual net forest area loss in Brazil- UMD alerts'
##    we create the umd bar chart here:
    bar_chart2 = pygal.Bar(width=1200, height=600,
                          explicit_size=True, title=title2, style=st2)
##    we add the candidates to the x axis of the chart
    bar_chart2.x_labels = years

##    The probability values are added to the y axis of the chart
    bar_chart2.add('Hectares', net_values)

    
## we create the html string that we want our web page
## to render
    html = """
        <html>
             <head>
                  <title>%s</title>
             </head>
              <body>
                 %s
                 %s
                 %s
             </body>
        </html>
        """ % (title, bar_chart.render(),bar_chart2.render(),bar_chartc.render())
    return html

##We start the flask server here
if __name__ == "__main__":
    app.debug=True
    app.run()
