##The following are the modules that need to be imported
##for the code to run. You will need to install flask,numpy
##and pygal for rendering charts on the web page
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

##This method polls the GFW API and creates a web page with
##bar chart showing monthly imazon alerts and annual umd-loss-gain
##alerts as well as the yearly prices for a commodity 
@app.route("/")
def histogram():
##    The following lists store the start and end dates we need to poll the GFW data multiple
##    times and allows the user to specify the dates that he wants to use for his analysis
    starts=['2015-01-01','2015-02-01','2015-03-01','2015-04-01','2015-05-01','2015-06-01','2015-07-01','2015-08-01','2015-09-01','2015-10-01','2015-11-01','2015-12-01','2016-01-01']
    ends=['2015-02-01','2015-03-01','2015-04-01','2015-05-01','2015-06-01','2015-07-01','2015-08-01','2015-09-01','2015-10-01','2015-11-01','2015-12-01','2016-01-01','2016-02-01']
    terrai_values=[]
##    The months list is used in rendering the x axis of the bar chart
    months=['January','February','March','April','May','June','July','August','September','October','November','December','January']
##    We loop over the start and end dates and poll the api to
##    obtain the imazon alerts
    for i in range(len(starts)):
##        This is the url endpoint for GFW imazon alerts
        ep='http://api.globalforestwatch.org/forest-change/imazon-alerts/admin/bra/?period='+starts[i]+','+ends[i]
##        The following is a geojson which must be passed in the POST request, however since
##        we mention country iso code in the url endpoint, alerts are given for the nation
        pl={"geojson":'{"type":"Polygon","coordinates":[[[12.8,8.9],[13.3,-7.3],[32.5,-6.6],[32.5,7.7],[12.8,8.9]]]}'}
##        The request is communicated using the POST
        res=requests.post(ep,pl)
        r=res.json()
        s=r['value']
        for i in s:
##            The imazon alerts have 2 components 'defor' standing for deforestation and
##            'degrad' standing for degradation, we need the 'defor' values
            if i['data_type']=='defor':
                terrai_values.append(i['value'])

##This is the url endpoint for umd-loss-gain alert
    ep='http://api.globalforestwatch.org/forest-change/umd-loss-gain/admin/idn/?period=2015-12-01,2016-01-01'
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
##        The umd-loss-gain alerts have a gain and loss component in their response,
##        we calculate the net loss as follows:
        if gain is None:
            gain=0
        net=loss-gain
        net_values.append(net)
        years.append(i['year'])
    commodity=[]
##    The years list is used for rendering x axis of annual deforestation and commodity
##    charts    
    years=['2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014']
##    This is the endpoint of the quandl API
    epComm='https://www.quandl.com/api/v3/datasets/OFDP/FUTURE_CC1/data.json?start_date=2001-01-01&end_date=2014-01-31&column_index=4&collapse=annual&order=asc&api_key=SQx81iJsvvNB_CfFP-5q'
    result=requests.get(epComm)
    r=result.json()
    s=r['dataset_data']
    for i in s['data']:
        commodity.append(i[1])

    for i in xrange(len(years)):
        print years[i]+','+str(commodity[i])+','+str(net_values[i])

    title='Forest loss in Brazil from January 2015'
##    we create the bar chart here:
    bar_chart = pygal.Bar(width=1200, height=600,
                          explicit_size=True, title=title, style=st)
##    we add the candidates to the x axis of the chart
    bar_chart.x_labels = months

##    The probability values are added to the y axis of the chart
    bar_chart.add('Hectares', terrai_values)

    titlec='Soybean prices over 2015'
##    we create the bar chart here:
    bar_chartc = pygal.Bar(width=1200, height=600,
                          explicit_size=True, title=titlec, style=st3)
##    we add the candidates to the x axis of the chart
    bar_chartc.x_labels = years

##    The probability values are added to the y axis of the chart
    bar_chartc.add('Price', commodity)


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
