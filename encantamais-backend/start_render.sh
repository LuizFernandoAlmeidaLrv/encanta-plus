#!/bin/bash
# start_render.sh

echo "Instalando dependências..."
pip install -r requirements.txt

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

echo "Rodando migrations..."
retry_migrate

echo "Criando superuser se não existir..."
python create_admin.py

echo "Iniciando Gunicorn..."
exec gunicorn EncantaMais.wsgi:application --bind 0.0.0.0:$PORT
