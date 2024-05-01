import requests
import csv
from flask import Flask, redirect, url_for, request, jsonify
from flask_cors import CORS
from io import BytesIO
import pandas as pd
import jsonForChartCreator as creator

app = Flask(__name__)
CORS(app)



@app.route('/compare',methods = ['POST', 'GET'])
def login():
   print("request\n",request)
   json_data = request.form or request.get_json()
   data = dict(json_data)
   print("request data\n",data)
   print("request json_data\n",json_data)
   print("request request.form\n",request.form)

   if request.method == 'POST':
      return "Ciao Post"
   else:
      user = request.args.get('nm')
      return "Ciao GET"


def post_search_doi():
    csv = request.files.get('file')
    print(csv)


@app.route('/accedifile',methods = ['POST', 'GET'])
def get_data():
   json_data = request.form or request.get_json()
   data = dict(json_data)
   print(data)
   oracle = data["rfds1"][0]
   resulting_rfds = data["rfds"][0]
   dataset_oracle = requests.get('http://localhost:3000/uploads/{}'.format(oracle)).content
   dataset_resultingrfds = requests.get('http://localhost:3000/uploads/{}'.format(resulting_rfds)).content

   df=pd.read_csv(BytesIO(dataset_oracle), sep=";")
   #print(df)
   oraclepath = './dataset/oracle.csv'
   df.to_csv(oraclepath, sep=";", index=False)
   
   df2=pd.read_csv(BytesIO(dataset_resultingrfds), sep=";")
   #print(df2)
   resultingpath = './dataset/resultingrfds.csv'
   df2.to_csv(resultingpath, sep=";", index=False)

   creator.create_json(oraclepath,resultingpath)
   path_jsonchart = "D:\github\VisualRFD-BigVis2024\server-comparison\dataset\jsonForChart_results.json"
   path_percentuali = "D:\github\VisualRFD-BigVis2024\server-comparison\dataset\percentuali_results.json"
   info = {
        "jsonforchart" : path_jsonchart,
        "percentages" : path_percentuali
    }
   return jsonify(info) # returning a JSON response


if __name__ == '__main__':
   app.run(debug = True)