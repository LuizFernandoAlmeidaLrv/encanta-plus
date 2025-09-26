#!/bin/bash
set -e  # Sai se algum comando falhar
set -x  # Mostra cada comando enquanto executa

echo "=== Instalando dependências ==="
pip install --upgrade pip
pip install Pillow
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

# Chamando a função
retry_migrate

echo "=== Criando superusuário (se não existir) ==="
python create_admin.py || echo "Superusuário já existe, pulando"

echo "=== Iniciando Gunicorn ==="

# Ajustes importantes para Render:
# 1. Usa a porta que o Render fornece via variável $PORT
# 2. Define 2 workers para não travar se um worker travar
# 3. Timeout maior para evitar que o Render marque como travado
exec gunicorn EncantaMais.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 60 \
    --log-level info
