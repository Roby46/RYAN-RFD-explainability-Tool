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
   name = request.data.decode("utf-8")
   print("request data\n",name)
   df = pd.read_csv("./datasets/"+name, delimiter=";")
   print(df)
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

   print("RHS:", rhs)
   print("LHS:", lhs)
   print("LHS_OLD", old_lhs)
   print("RHS_OLD", old_rhs)
   print("Type:", rfd_type)
   
   lhs = lhs.replace("'","")
   lhs = lhs.replace("{","")
   lhs = lhs.replace("}","")
   lhs_attr = lhs.split(", ")

   rhs = rhs.strip()
   rhs_col = dataset.loc[:,rhs]
   print(rhs_col)
   rhs_data = (rhs,rhs_col)

   lhs_data = []
   for i in lhs_attr:
      elem = i.strip()
      lhs_col = dataset.loc[:,elem]
      tmp = (elem,lhs_col)
      lhs_data.append(tmp)

   rfd_data = {"rhs":rhs_data, "lhs":lhs_data, "type":rfd_type}
   print(rfd_data)

   return "json ricevuto con successo.",200
   response = render_template('Explaination.html', explaination = results)


if __name__ == '__main__':
   app.run(debug = True)