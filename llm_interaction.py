from gpt4all import GPT4All
import requests
import sseclient
import json
import time

#orca-mini-3b-gguf2-q4_0.g  gpt4all-13b-snoozy-q4_0.gguf

def load_model(type_model="orca-mini-3b-gguf2-q4_0.gguf"):
    model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")
    #model = ""
    print("Modello Caricato!")
    return model

def ask_llm(model, prompt, max_tokens=100, streaming=False):
    #output = model.generate("What is a relaxed functional dependency? ", max_tokens=100)
    output = model.generate(prompt+" ", max_tokens=max_tokens, streaming=streaming)
    print("[ask_llm]",output)
    return output

def ask_ddgo_llm(prompt):
    session_code = get_status_code()
    output=get_llm_answer(session_code, prompt)
    return output


def get_status_code():
	cookies = {
	    'dcm': '3',
	}

	headers = {
	    'accept': '*/*',
	    'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7,de-DE;q=0.6,de;q=0.5,es;q=0.4,pl;q=0.3',
	    'cache-control': 'no-store',
	    # 'cookie': 'dcm=3',
	    'priority': 'u=1, i',
	    'referer': 'https://duckduckgo.com/',
	    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
	    'sec-ch-ua-mobile': '?0',
	    'sec-ch-ua-platform': '"macOS"',
	    'sec-fetch-dest': 'empty',
	    'sec-fetch-mode': 'cors',
	    'sec-fetch-site': 'same-origin',
	    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
	    'x-vqd-accept': '1',
	}

	response = requests.get('https://duckduckgo.com/duckchat/v1/status', cookies=cookies, headers=headers)
	session_code = response.headers['x-vqd-4']
	print("Status Response:",response,session_code)
	return session_code

def get_llm_answer(session_code, prompt):
	url = 'https://duckduckgo.com/duckchat/v1/chat'
	headers = {
	    'accept': 'text/event-stream',
	    'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7,de-DE;q=0.6,de;q=0.5,es;q=0.4,pl;q=0.3',
	    'content-type': 'application/json',
	    # 'cookie': 'dcm=3',
	    'origin': 'https://duckduckgo.com',
	    'priority': 'u=1, i',
	    'referer': 'https://duckduckgo.com/',
	    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
	    'sec-ch-ua-mobile': '?0',
	    'sec-ch-ua-platform': '"macOS"',
	    'sec-fetch-dest': 'empty',
	    'sec-fetch-mode': 'cors',
	    'sec-fetch-site': 'same-origin',
	    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
	    'x-vqd-4': session_code
	}
	print(headers)
	data = {
	    #"model": "gpt-3.5-turbo-0125",
	    'model': 'gpt-4o-mini',
	    "messages": [{
	        "role": "user",
	        "content":  prompt
        }]
	}

	response = requests.post(url, headers=headers, json=data, stream=True)

	#session_code = response.headers['x-vqd-4']
	#print("Chat Response:", response.headers)
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
	                print(d['message'],end="")
	    except:
	        break

	# Unisci tutti i messaggi in una singola stringa
	complete_message = ''.join(messages)

	# Stampa il messaggio completo
	#print(complete_message)

	return complete_message