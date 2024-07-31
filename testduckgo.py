import requests
import sseclient
import json

url = 'https://duckduckgo.com/duckchat/v1/chat'
#headers = {
#    'accept': 'text/event-stream',
#    'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7,de-DE;q=0.6,de;q=0.5,es;q=0.4,pl;q=0.3',
#    'content-type': 'application/json',
#    'cookie': 'dcm=3; ae=-1',
#    'origin': 'https://duckduckgo.com',
#    'priority': 'u=1, i',
#    'referer': 'https://duckduckgo.com/',
#    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
#    'sec-ch-ua-mobile': '?0',
#    'sec-ch-ua-platform': '"macOS"',
#    'sec-fetch-dest': 'empty',
#    'sec-fetch-mode': 'cors',
#    'sec-fetch-site': 'same-origin',
#    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
#    'x-vqd-4': '4-211122308202828671676848603708400720389'
#}

headers = {
    'accept': 'text/event-stream',
    'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    # 'cookie': 'dcm=1',
    'origin': 'https://duckduckgo.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://duckduckgo.com/',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'x-vqd-4': '4-64989446206168759335115125981870622892',
}

data = {
    "model": "gpt-3.5-turbo-0125",
    "messages": [{
        "role": "user",
        "content": ("In relational databases, a Relaxed Functional Dependency (RFD) is an integrity constraint "
                    "X -> Y between two sets of attributes X and Y, meaning that if two tuples have similar value on X, "
                    "then they must have similar values on Y. X is named Left Hand Side (LHS), while Y is the Right Hand Side (RHS). "
                    "Two values of an attribute are similar if their distance is lower than the similarity threshold defined on that attribute. "
                    "The function to assess similarity is edit distance for strings and difference for numbers. After the insertion of a new tuple, "
                    "an existing RFD can be invalidated only if the new tuple has similar values on the LHS with respect other tuples but it has "
                    "different values on the RHS. In this case, a specialized RFD with additional attributes on the LHS may be valid on the dataset. "
                    "You will be provided with an RFD that gets invalidated after the insertion of a batch of tuples, and with the tuples that caused "
                    "the violation and their values. The RFD {LHS: [ age (threshold=6), platelets (threshold=244)], RHS: [serum-creatinine(threshold=1.0)]} "
                    "was invalidated and specialized by a new RFD {LHS: [ age (threshold=6.0), platelets (threshold=244.0), serum-sodium (threshold=2.0)], "
                    "RHS: [serum-creatinine(threshold=1.0)]}. This happened because: --The insertion of Tuple 52 (age=60.0, platelets=263358.03, serum-creatinine=6.8) "
                    "caused a violation considering tuple 8 (age=65.0, platelets=263358.03, serum-creatinine=1.5) tuple 1 (age=55.0, platelets=263358.03, serum-creatinine=1.1) "
                    "Basing on this information, provide an extensive explanation of why the RFD was invalidated. To do this, analyze the attribute values and consider the similarity thresholds.")
    }]
}

response = requests.post(url, headers=headers, json=data, stream=True)
client = sseclient.SSEClient(response)

print("Waiting for answers...\n\n")

# Lista per raccogliere tutti i messaggi
messages = []

# Itera sugli eventi nello stream e aggiungi i dati alla lista
for event in client.events():
    try:
        if len(event.data) >0:
            d = json.loads(event.data)
            #print(d, type(d), d.keys)
            if 'message' in d:
                messages.append(d['message'])
    except:
        break

# Unisci tutti i messaggi in una singola stringa
complete_message = ''.join(messages)

# Stampa il messaggio completo
print(complete_message)
