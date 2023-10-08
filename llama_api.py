from fastapi import FastAPI, Query, HTTPException
import llama_cpp
import ctypes
import time
import datetime

app = FastAPI()

@app.post("/chat")
def chat(prompt: str = Query(...), max_tokens: int = Query(100), temperature: float = Query(0.8), system_prompt: str = Query("Eres un filósofo.")):
    try:
        start_time = time.time()
        llama_cpp.llama_backend_init(numa=False)
        params = llama_cpp.llama_context_default_params()
        params.temperature = temperature
        params.max_tokens = max_tokens
        model = llama_cpp.llama_load_model_from_file(b"./models/7b/llama-model.gguf", params)
        ctx = llama_cpp.llama_new_context_with_model(model, params)
        tokens = (llama_cpp.llama_token * int(max_tokens)) ()
        n_tokens = llama_cpp.llama_tokenize(ctx, (system_prompt + " " + prompt).encode())
        response_tokens = [item for item in tokens[:n_tokens]]
        response_text = "".join(response_tokens)
        processing_time = time.time() - start_time

        # Estimación del costo en GCP
        # Supongamos que el costo por hora es de $1.50 (esto puede variar dependiendo de la instancia de GCP que estés utilizando)
        cost_per_second = 1.50 / 3600
        estimated_cost = processing_time * cost_per_second

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "response": response_text,
        "parameters": {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "system_prompt": system_prompt,
        },
        "token_counts": {
            "prompt_tokens": len(prompt.split()),
            "response_tokens": len(response_text.split()),
            "total_tokens": len(prompt.split()) + len(response_text.split()),
        },
        "metadata": {
            "creation_time": datetime.datetime.now().isoformat(),
            "processing_time_seconds": processing_time,
            "estimated_cost_usd": estimated_cost,
        },
    }
