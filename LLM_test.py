import llm_interaction as llm
model = llm.load_model()

prompt = "relaxed functional dependencies"
# ---------------- Interact with LLM
output = llm.ask_llm(model, prompt, max_tokens=300)
print("llm", output)