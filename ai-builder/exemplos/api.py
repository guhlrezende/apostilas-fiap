"""API mínima de triagem de pedidos (exemplo da apostila de AI Builder, cap. 6).

Rodar:  pip install fastapi uvicorn
        uvicorn api:app --reload
Abrir:  http://127.0.0.1:8000/docs  (a documentação interativa vem pronta)
"""
import os

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Triagem de pedidos")

# A chave vem do ambiente, nunca do código. Sem a variável, usa um valor de teste.
CHAVE = os.environ.get("API_KEY", "chave-de-teste")


class Pedido(BaseModel):
    cliente: str
    valor: float
    urgente: bool = False


@app.get("/saude")
def saude():
    """Rota que o monitoramento chama para saber se a API está de pé."""
    return {"status": "ok"}


@app.post("/triagem")
def triagem(pedido: Pedido, x_api_key: str = Header(default="")):
    """Recebe um pedido em JSON e devolve a fila para onde ele vai."""
    if x_api_key != CHAVE:
        raise HTTPException(status_code=401, detail="chave inválida")
    if pedido.urgente or pedido.valor >= 1000:
        fila = "prioridade"
    else:
        fila = "normal"
    return {"cliente": pedido.cliente, "fila": fila}
