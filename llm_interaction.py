from gpt4all import GPT4All

def load_model(type_model="orca-mini-3b-gguf2-q4_0.gguf"):
    model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")
    print("Modello Caricato!")
    return model

def ask_llm(model, prompt, max_tokens=100, streaming=False):
    #output = model.generate("What is a relaxed functional dependencies? ", max_tokens=100)
    output = model.generate(prompt+" ", max_tokens=max_tokens, streaming=streaming)
    print("[ask_llm]",output)
    return output