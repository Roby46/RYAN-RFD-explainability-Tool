import requests
import csv
from flask import Flask, redirect, url_for, request, jsonify, render_template
from flask_cors import CORS
from io import BytesIO
import pandas as pd
from StarDust import PatternLoader
import sys
import numpy as np
import copy
import llm_interaction as llm

app = Flask(__name__, template_folder='./templates', static_url_path='/static')
CORS(app)
model = llm.load_model()
print("Large Language Model",model)
global dataset,prompt,rhs,lhs,old_lhs,old_rhs,rfd_type

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/explain')
def explain():
   global dataset,prompt,rhs,lhs,old_lhs,old_rhs,rfd_type

   # Recupera i dati dalla query string
   rhs = request.args.get('rhs')
   lhs = request.args.get('lhs')
   old_lhs = request.args.get('old_lhs')
   old_rhs = request.args.get('old_rhs')
   rfd_type = request.args.get('type')

   # Usa i dati come desideri
   print("Param1:", rhs)
   print("Param2:", lhs)
   print("Param3:", old_lhs)
   print("Param4:", old_rhs)
   print("Param5:", rfd_type)

    
    # Logica per generare la pagina HTML
   return render_template('LLM_Answer2.html')

# Funzione per calcolare la differenza tra partizioni
def compute_difference(obj1, obj2):
    diff_obj = {}
    for attribute in obj1:
        #print(attribute)
        diff_obj[attribute] = {}
        for pattern_value in obj2[attribute]:
            #print(pattern_value)
            if pattern_value in obj1.get(attribute, {}):
                diff_obj[attribute][pattern_value] = obj2[attribute][pattern_value] - obj1[attribute][pattern_value]
            else:
                diff_obj[attribute][pattern_value] = obj2[attribute][pattern_value]  # Aggiungi il valore dall'oggetto 2
    return diff_obj

   # Funzione per calcolare la differenza tra partizioni

def clean_partition(obj1, indexes):
    for attribute in obj1:
      for pattern_value in obj1[attribute]:
         obj1[attribute][pattern_value]= obj1[attribute][pattern_value] - set(indexes)       
    return obj1

def remove_columns_if_exist(df, columns):
    existing_columns = [col for col in columns if col in df.columns]
    return df.drop(existing_columns, axis=1)

def deep_copy_dict(d):
    new_dict = {}
    for key, value in d.items():
        new_dict[key] = copy.deepcopy(value)
    return new_dict

@app.route('/ask', methods = ['GET'])
def ask_prompt():
   global dataset,prompt,rhs,lhs,old_lhs,old_rhs,rfd_type
   tmp = rhs.split("_")
   rhs = tmp[0]
   rhs_thr = tmp[1]
   if old_rhs != "none":
      tmp = old_rhs.split("_")
      old_rhs = tmp[0]
      old_rhs_thr = tmp[1]

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
   lhs_thr = []
   for attr in lhs_attr:
      tmp = attr.split("_")
      lhs_puliti.append(tmp[0])
      lhs_thr.append(tmp[1])

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
      old_lhs_thr = []
      for attr in old_lhs_attr:
         tmp = attr.split("_")
         old_lhs_puliti.append(tmp[0])
         old_lhs_thr.append(tmp[1])

      old_rhs = old_rhs.strip()
      old_rhs_col = dataset.loc[:,old_rhs]
      #print(old_rhs_col)
      old_rhs_data = (old_rhs,old_rhs_col)

      for i in range(0,len(old_lhs_puliti)):
         old_lhs_puliti[i] = old_lhs_puliti[i].strip()

      old_lhs_data = []
      for i in old_lhs_puliti:
         elem = i.strip()
         old_lhs_col = dataset.loc[:,elem]
         tmp = (elem,old_lhs_col)
         old_lhs_data.append(tmp)


      rfd_data = {"rhs":rhs_data, "rhs_thr":rhs_thr, "lhs":lhs_data, "lhs_thr":lhs_thr, "type":rfd_type, "old_rhs":old_rhs_data, "old_rhs_thr":old_rhs_thr, "old_lhs":old_lhs_data, "old_lhs_thr":old_lhs_thr}
      #print(rfd_data)
   else:
      rfd_data = {"rhs":rhs_data, "rhs_thr":rhs_thr, "lhs":lhs_data, "lhs_thr":lhs_thr, "type":rfd_type, "old_rhs_thr":"none", "old_lhs":"none", "old_lhs_thr":"none"}
      #print(rfd_data)

   #print(rfd_data['rhs'][1].tolist())
   #print(rfd_data['lhs'][1].tolist())
 

   #Lista di colonne da mantere -- cambia sulla base di generalizzazioni e specializzazioni
   columns_to_keep=[]
   if(rfd_type == "specialization"):
      columns_to_keep=['operation', 'index'] + old_lhs_puliti
   elif(rfd_type == "generalization"):
      columns_to_keep=['operation', 'index'] + lhs_puliti
   columns_to_keep.append(rhs)
   print("Cols to keep: ", columns_to_keep)
   
   #Filtro del dataset, mantenendo operation, index, lhs e rhs
   df=dataset[columns_to_keep]   
   #Ordinamento delle colonne per rimettere la colonna rhs nella giusta posizione
   df = df[dataset.columns.intersection(columns_to_keep)]
   print("Filtered dataset: \n", df)


   columns_to_remove = ['operation', 'index']
   #DF con solo i dati per le partizioni
   df_data = remove_columns_if_exist(df, columns_to_remove)

   #Indice di posizione dell'rhs nel dataset fitrato
   index_rhs=df_data.columns.get_loc(rhs)

   index_lhs=[]
   if(rfd_type == "specialization"):
      for attr in old_lhs_puliti:
         index_lhs.append(df_data.columns.get_loc(attr))
   elif(rfd_type == "generalization"):
      for attr in lhs_puliti:
         index_lhs.append(df_data.columns.get_loc(attr))
   
   print("Posizione RHS", index_rhs)
   print("Array posizioni LHS: ", index_lhs)

   #Creazione di un array di treshold della nuova dipendenza, prendendo quelle dell'lhs e inserendo quella dell'rhs nell'ordine giusto
   all_thresholds=lhs_thr.copy()
   all_thresholds.insert(index_rhs,rhs_thr)
   all_thresholds = [int(x) for x in all_thresholds]

   #Creazione di un array di treshold della dipendenza oracolo , prendendo quelle dell'lhs e inserendo quella dell'rhs nell'ordine giusto
   all_thresholds_old=old_lhs_thr.copy()
   all_thresholds_old.insert(index_rhs,old_rhs_thr)
   all_thresholds_old = [int(x) for x in all_thresholds_old]

   print("Thresholds ordinate nuova dipendenza: ", all_thresholds)
   print("Thresholds ordinate dipendenza oracolo: ", all_thresholds_old)

   # Dataset con solo righe originali
   df_zero = df[df["operation"] == 0]

   # Dataset contenente solo le tuple inserite
   df_insertions = df[df["operation"] > 0]

   # Dataset contenente solo le tuple cancellate
   df_deletions = df[df["operation"] < 0]

   if (rfd_type == "specialization"):
      print(30 * "-")
      print("Caso con solo inserimenti")
      
      #DF con dati originali più inserimenti
      merged_df = pd.concat([df_zero, df_insertions])

      #DF con dati originali più inserimenti, togliendo le colonne aggiuntive e l'intestazione
      df_full_data = remove_columns_if_exist(merged_df, columns_to_remove)
      df_full_data.columns = range(len(df_full_data.columns))

      #DF con dati originali, togliendo le colonne aggiuntive e l'intestazione
      df_zero_data = remove_columns_if_exist(df_zero, columns_to_remove)
      df_zero_data.columns = range(len(df_zero_data.columns))

      print("Dati con inserimenti: \n", df_full_data, "\n\n")
      print("Dati originali: \n", df_zero_data)

      #Pattern dati aggiornati
      sys.setrecursionlimit(1500)
      pattern_loader = PatternLoader("", "", all_thresholds_old, df_full_data)
      M, initial_partitions = pattern_loader.get_partition_local()
      print("Partizioni con gli inserimenti\n", M)

     
      #Pattern dati originali
      pattern_loader_old = PatternLoader("", "", all_thresholds_old, df_zero_data)  #gestire vecchie thresholds
      M_old, initial_partitions_old = pattern_loader_old.get_partition_local()
      print("Partizioni originali\n", M_old)

      difference = compute_difference(M_old, M)
      print("Differenza\n", difference)


      # Trova gli indici delle righe con valore maggiore di 0 nella colonna specificata
      lista_indici_inserimenti = df[df["operation"] > 0].index.tolist()

      for idx in lista_indici_inserimenti:
         print("\n\nControllo la tupla inserita:", idx)

         lhs_valid=True
         rhs_valid=True

         similarity_set=set()

         for attribute in range(len(df_zero_data.columns)):
            #print(attribute)
            if(attribute in index_lhs):
               trovato = False
               for ptnv in difference[attribute]:
                  print(ptnv)
                  if(idx in difference[attribute][ptnv]):
                     similarity_set.update(M[attribute][ptnv])
                     #print("Sono presente")
                     trovato=True
               if(not trovato):
                  lhs_valid = False
                  break
            elif(attribute == index_rhs):
               trovato = False
               for ptnv in difference[attribute]:
                  #print(ptnv)
                  if(idx in difference[attribute][ptnv]):
                     print("Sono presente")
                     trovato=True
               if(not trovato):
                  rhs_valid = False

         if(lhs_valid and not rhs_valid):
            column_names=df_data.columns.tolist()
            selected_column_names = [column_names[index] for index in index_lhs]
            print(80 * "=")
            print("La tupla\n",  df_data.iloc[idx], "\nha portato ad una specializzazione.")      
            similarity_set.remove(idx)
            for i in similarity_set:
               print(40 * "*")
               print("---- Simile sull'lhs (attributi", selected_column_names, ") con la tupla", i , "ma diversa sull'rhs (attributo [", rhs ,"])")
               print(df_data.iloc[i])
               print(40 * "*")
            print(80 * "=")

      #Se la specializzazione aggiunge due o più attributi, spiegare  perché quelle intermedie non valgono
      #Iterare su tutte le tuple, valutando come hanno impattato sulle partizioni

   #Fine if specializzazioni

   elif (rfd_type == "generalization"):
      print(30 * "-")
      print("Caso con solo cancellazioni")

      lista_indici_cancellazioni = df_deletions['index'].tolist()

      df_canc = df_zero.drop(lista_indici_cancellazioni)

      df_canc_data = remove_columns_if_exist(df_canc, columns_to_remove)
      df_canc_data.columns = range(len(df_canc_data.columns))

      df_zero_data = remove_columns_if_exist(df_zero, columns_to_remove)
      df_zero_data.columns = range(len(df_zero_data.columns))

      print("Dati originali: \n", df_zero_data, "\n\n")
      print("Dati con cancellazioni: \n", df_canc_data)
        
      pattern_loader_old = PatternLoader("", "", all_thresholds, df_zero_data)  #gestire  thresholds
      M_old, initial_partitions_old = pattern_loader_old.get_partition_local()
      print("Partizioni originali\n", M_old)

      M_old_2 = deep_copy_dict(M_old)

      #Rimuove dalle partizioni originali le tuple cancellate
      M = clean_partition(M_old_2, lista_indici_cancellazioni)

      print("Partizioni con cancellazioni\n", M)


      difference = compute_difference(M, M_old)
      print("Differenza\n", difference)

      for idx in lista_indici_cancellazioni:
         print("\n\nControllo la tupla cancellata:", idx)

         lhs_valid=True
         rhs_valid=True

         similarity_set=set()

         for attribute in range(len(df_zero_data.columns)):
            #print(attribute)
            if(attribute in index_lhs):
               trovato = False
               for ptnv in difference[attribute]:
                  #print(ptnv)
                  if(idx in difference[attribute][ptnv]):
                     similarity_set.update(M_old[attribute][ptnv])
                     #print("Sono presente")
                     trovato=True
               if(not trovato):
                  lhs_valid = False
                  break
            elif(attribute == index_rhs):
               trovato = False
               for ptnv in difference[attribute]:
                  #print(ptnv)
                  if(idx in difference[attribute][ptnv]):
                     #print("Sono presente")
                     trovato=True
               if(not trovato):
                  rhs_valid = False

         if(lhs_valid and not rhs_valid):
            column_names=df_data.columns.tolist()
            selected_column_names = [column_names[index] for index in index_lhs]
            print(80 * "=")
            print("La tupla\n", df_data.iloc[idx], "\nviolava una dipendenza, con la rimozione ha portato alla generalizzazione.")      
            similarity_set.remove(idx)
            for i in similarity_set:
               print(40 * "*")
               print("---- Era simile sull'lhs (attributi", selected_column_names, ") con la tupla", i , "ma differiva sull'rhs (attributo", rhs ,")")
               print(df_data.iloc[i])
               print(40 * "*")
            print(80 * "=")

   # ---------------- Interact with LLM
   prompt = "Give me the definition of computer"
   output = llm.ask_llm(model, prompt, max_tokens=300, streaming=False)
   print("llm", output)
   # ---------------- Interact with LLM
   return {"LLMAnswer": output}

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
   dataset = pd.read_csv("./static/Datasets/"+name, delimiter=";")
   print(dataset)
   return 'File caricato con successo!', 200 




'''@app.route('/getRFD',methods = ['POST'])
def get_rfds():
   global dataset,prompt,rhs,lhs,old_lhs,old_rhs,rfd_type
   #print(dataset)
   # Leggi il JSON inviato nel corpo della richiesta
   json_data = request.get_json()
   
   # Estrai i valori dal JSON
   rhs = json_data.get('rhs')
   lhs = json_data.get('lhs')
   old_lhs = json_data.get('old_lhs')
   old_rhs = json_data.get('old_rhs')
   rfd_type = json_data.get('type')

   

         #Valuto LHS

   #prompt = "Give me the definition of relaxed functional dependencies"
   return {"prompt": prompt}
'''

if __name__ == '__main__':
   app.run(debug = True)