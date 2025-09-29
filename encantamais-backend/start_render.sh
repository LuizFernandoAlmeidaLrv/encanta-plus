#!/bin/bash
set -e  # Sai se algum comando falhar
set -x  # Mostra cada comando enquanto executa

echo "=== Instalando dependências === "
pip install --upgrade pip
pip install Pillow
pip install -r requirements.txt

echo "=== Rodando migrações === "

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

echo "=== Criando superusuário (se não existir) === "
python create_admin.py || echo "Superusuário já existe, pulando"

echo "=== Verificando instalação do Gunicorn === "
command -v gunicorn || { echo "Gunicorn não encontrado! Verifique requirements.txt"; exit 1; }

echo "=== Testando importação do módulo WSGI === "
python -c "import EncantaMais.wsgi" || { echo "Falha ao importar EncantaMais.wsgi! Verifique o nome do projeto e o arquivo wsgi.py"; exit 1; }


echo "=== Tentando iniciar Gunicorn com comando simplificado === "

# PASSE A SECRET_KEY DIRETAMENTE COMO UMA VARIAVEL DE AMBIENTE PARA O GUNICORN
exec gunicorn EncantaMais.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --timeout 30 \
    --log-level debug \
    --env SECRET_KEY="$SECRET_KEY"

echo "=== Gunicorn iniciado (se você vir isso, algo está errado) === "
