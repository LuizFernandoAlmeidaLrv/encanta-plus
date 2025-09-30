#!/bin/bash
set -e  # sai se algum comando falhar
set -x  # mostra cada comando enquanto executa

echo "=== Rodando migrações ==="

# Função para rodar migrate com retry (em caso de banco ainda não pronto)
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

retry_migrate

echo "=== Criando superusuário (se não existir) ==="
python create_admin.py || echo "Superusuário já existe, pulando"

echo "=== Verificando Gunicorn ==="
command -v gunicorn || { echo "Gunicorn não encontrado! Verifique requirements.txt"; exit 1; }

echo "=== Verificando SECRET_KEY no runtime ==="
if [ -z "$SECRET_KEY" ]; then
  echo "ERRO: SECRET_KEY não está definida no ambiente!"
  exit 1
else
  echo "DEBUG: SECRET_KEY carregada (tamanho: ${#SECRET_KEY})"
fi

echo "=== Iniciando Gunicorn ==="
exec gunicorn EncantaMais.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --timeout 30 \
    --log-level debug
