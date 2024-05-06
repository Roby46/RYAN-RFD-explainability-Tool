import requests
import csv
from flask import Flask, redirect, url_for, request, jsonify
from flask_cors import CORS
from io import BytesIO
import pandas as pd
from StarDust import PatternLoader
import sys
import numpy as np

app = Flask(__name__)
CORS(app)

global dataset

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
   global dataset
   name = request.data.decode("utf-8")
   print("request data\n",name)
   dataset = pd.read_csv("./datasets/"+name, delimiter=";")
   print(dataset)
   return 'File caricato con successo!', 200 





@app.route('/getRFD',methods = ['POST'])
def get_rfds():
   global dataset
   #print(dataset)
   # Leggi il JSON inviato nel corpo della richiesta
   json_data = request.get_json()
   
   # Estrai i valori dal JSON
   rhs = json_data.get('rhs')
   lhs = json_data.get('lhs')
   old_lhs = json_data.get('old_lhs')
   old_rhs = json_data.get('old_rhs')
   rfd_type = json_data.get('type')

   tmp = rhs.split("_")
   rhs = tmp[0]
   if old_rhs != "none":
      tmp = old_rhs.split("_")
      old_rhs = tmp[0]


   print("RHS:", rhs)
   print("LHS:", lhs)
   print("LHS_OLD", old_lhs)
   print("RHS_OLD", old_rhs)
   print("Type:", rfd_type)
   
   lhs = lhs.replace("'","")
   lhs = lhs.replace("[","")
   lhs = lhs.replace("]","")
   #print(lhs)
   lhs_attr = lhs.split(", ")

   lhs_puliti = []
   for attr in lhs_attr:
      tmp = attr.split("_")
      lhs_puliti.append(tmp[0])

   rhs = rhs.strip()
   rhs_col = dataset.loc[:,rhs]
   #print(rhs_col)
   rhs_data = (rhs,rhs_col)

   lhs_data = []
   for i in lhs_puliti:
      elem = i.strip()
      lhs_col = dataset.loc[:,elem]
      tmp = (elem,lhs_col)
      lhs_data.append(tmp)

   if old_lhs != "none":
      old_lhs = old_lhs.replace("'","")
      old_lhs = old_lhs.replace("[","")
      old_lhs = old_lhs.replace("]","")
      #print(old_lhs)
      old_lhs_attr = old_lhs.split(", ")

      old_lhs_puliti = []
      for attr in old_lhs_attr:
         tmp = attr.split("_")
         old_lhs_puliti.append(tmp[0])

      old_rhs = old_rhs.strip()
      old_rhs_col = dataset.loc[:,old_rhs]
      #print(old_rhs_col)
      old_rhs_data = (old_rhs,old_rhs_col)

      old_lhs_data = []
      for i in old_lhs_puliti:
         elem = i.strip()
         old_lhs_col = dataset.loc[:,elem]
         tmp = (elem,old_lhs_col)
         old_lhs_data.append(tmp)


      rfd_data = {"rhs":rhs_data, "lhs":lhs_data, "type":rfd_type, "old_rhs":old_rhs_data, "old_lhs":old_lhs_data}
      print(rfd_data)
   else:
      rfd_data = {"rhs":rhs_data, "lhs":lhs_data, "type":rfd_type, "old_rhs":"none", "old_lhs":"none"}
      print(rfd_data)



   

   return "json ricevuto con successo.",200
   response = render_template('LLM_Answer2.html', explaination = results)



if __name__ == '__main__':
   app.run(debug = True)