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
def get_data():
   # Leggi il JSON inviato nel corpo della richiesta
    json_data = request.get_json()
    
    # Estrai i valori dal JSON
    rhs = json_data.get('rhs')
    lhs = json_data.get('lhs')
    rfd_type = json_data.get('type')

    # Ad esempio, puoi stampare i valori ricevuti
    print("RHS:", rhs)
    print("LHS:", lhs)
    print("Type:", rfd_type)
   return "json ricevuto con successo.",200

if __name__ == '__main__':
   app.run(debug = True)