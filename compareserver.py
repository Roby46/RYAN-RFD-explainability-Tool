import requests
import csv
from flask import Flask, redirect, url_for, request, jsonify
from flask_cors import CORS
from io import BytesIO
import pandas as pd

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


@app.route('/upload',methods = ['POST'])
def get_data():
   file = request.data
   print("request data\n",file)
   return 'File caricato con successo!', 200 

if __name__ == '__main__':
   app.run(debug = True)