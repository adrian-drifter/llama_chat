from llama_cpp import Llama

model_dir = "/home/drifter/models/Llama-2-7b-chat-hf"
model = Llama(model_dir)

message = "¿Hola como estas?"

response = model.generate(message)

print(response)
