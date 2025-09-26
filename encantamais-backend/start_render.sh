#!/bin/bash
set -e  # sai se algum comando falhar
set -x  # mostra cada comando enquanto executa

echo "=== Instalando dependências ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== Rodando migrações ==="

# Função para rodar migrate com retry
retry_migrate() {
  n=0
  until [ $n -ge 5 ]
  do
    python manage.py migrate && break
    n=$((n+1))
    echo "Falha ao conectar no banco, tentando novamente ($n/5)..."
    sleep 5
  done
}

# CHAMANDO a função
retry_migrate

echo "=== Criando superusuário (se não existir) ==="
python create_admin.py || echo "Superusuário já existe, pulando"

echo "=== Iniciando Gunicorn ==="
exec gunicorn EncantaMais.wsgi:application --bind 0.0.0.0:$PORT
