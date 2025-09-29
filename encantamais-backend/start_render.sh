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

# --- NOVAS VERIFICAÇÕES E INICIALIZAÇÃO SIMPLIFICADA DO GUNICORN ---
echo "=== Testando importação do módulo WSGI === "
python -c "import EncantaMais.wsgi" || { echo "Falha ao importar EncantaMais.wsgi! Verifique o nome do projeto e o arquivo wsgi.py"; exit 1; }

echo "=== Tentando iniciar Gunicorn com comando simplificado === "

# ADICIONE ESTA LINHA PARA DEPURACAO TEMPORARIA
export SECRET_KEY="p(&(c^ljh_6nm8ih#=84(z#-d8@e)v9)kjusij+=i!0#y%%ar-"

exec gunicorn EncantaMais.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --timeout 30 \
    --log-level debug
# --- FIM DAS NOVAS VERIFICAÇÕES ---

