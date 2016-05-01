A. Installing dependencies:



The implementation is done using Flask-SocketIO. The requirements.txt has all necessary applications to run the Flask-SocketIO.
To install the Flask dependencies run the following command:

		$ pip install -r requirements.txt

pygal is a module which renders a graph onto a webpage. The following command can be used to install pygal
		
		$ pip install pygal

The documentation on pygal and the various formatting of the graph can be found at : http://www.pygal.org/en/latest/documentation/


B. Running the code:


Getting the data from the GFW API:
1. For the iamazon alerts:
	http://api.globalforestwatch.org/forest-change/imazon-alerts/admin/country_iso_code/?period=start_to_end_dates
2. For the umd alerts:
	http://api.globalforestwatch.org/forest-change/umd-loss-gain/admin/country_iso_code/?period=start_to_end_dates

For further information on the GFW API:
	https://github.com/wri/gfw-api

Getting the data from quandl API:
	https://www.quandl.com/api/v3/datasets/commodity_code/data.json?start_date=''&end_date=''&column_index=4&collapse=annual&order=asc&api_key=''	


To specify the country and the commodity for which the data is to be received, change the 'country' and 'commodity_code' value in the file charts.py
To get the country iso code go to https://en.wikipedia.org/wiki/ISO_3166-1 and select the Alpha-3 code of the country
To get the commodity code go to https://www.quandl.com/blog/api-for-commodity-data and get the code for the commodity which is required


After making the changes to the required variables, run the file as:
		
		$ python charts.py

To view the output got to http://localhost:5000 in Google Chrome
