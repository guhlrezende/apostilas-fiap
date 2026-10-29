"""Testes da API de triagem. Rodar:  pip install pytest httpx  e depois  pytest -q"""
from fastapi.testclient import TestClient

from api import app

cliente = TestClient(app)
CAB = {"x-api-key": "chave-de-teste"}


def test_saude():
    r = cliente.get("/saude")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_pedido_grande_vai_para_prioridade():
    r = cliente.post("/triagem", json={"cliente": "Ana", "valor": 1500}, headers=CAB)
    assert r.json()["fila"] == "prioridade"


def test_pedido_pequeno_vai_para_normal():
    r = cliente.post("/triagem", json={"cliente": "Bia", "valor": 80}, headers=CAB)
    assert r.json()["fila"] == "normal"


def test_sem_chave_da_401():
    r = cliente.post("/triagem", json={"cliente": "Caio", "valor": 80})
    assert r.status_code == 401


def test_json_sem_campo_obrigatorio_da_422():
    r = cliente.post("/triagem", json={"cliente": "Davi"}, headers=CAB)
    assert r.status_code == 422
