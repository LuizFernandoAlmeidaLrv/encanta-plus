import requests

url = "http://127.0.0.1:8000/api/pedido/pedidos/"
headers = {"Content-Type": "application/json"}
data = {
    "cliente": "1",
    "id_forma_pagamento": 1,
    "tipo_entrega": 1,
    "valor_pedido": 23,
    "itens": [
        {
            "produto": 1,  # Agora é 'produto' ao invés de 'produto_id'
            "quantidade_pedida": 1,
            "valor_unitario": "23.00",
            "composicao": [
                {
                "ingrediente": 1,
                "quantidade": 1
                },
                {
                    "ingrediente": 2,
                    "quantidade": 1
                }
            ]
        }
    ]
}
response = requests.post(url, json=data, headers=headers)
print("Status Code:", response.status_code)
print("Resposta:", response.json())
