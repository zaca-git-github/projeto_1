import pandas as pd
import time
import json
import os
from flask import Flask, Response

app = Flask(__name__)

# --- LÓGICA DE LOCALIZAÇÃO DO DATASET ---
# O código tenta encontrar o arquivo na raiz ou na pasta /data para evitar erros de volume
if os.path.exists('train_sample.csv'):
    DATASET_PATH = 'train_sample.csv'
elif os.path.exists('data/train_sample.csv'):
    DATASET_PATH = 'data/train_sample.csv'
else:
    # Se não encontrar, ele lista os arquivos para ajudar no diagnóstico (Senioridade!)
    print(f"❌ ERRO: Arquivo não encontrado. Arquivos na pasta: {os.listdir('.')}")
    DATASET_PATH = None

def generate():
    """
    Simula um gerador de eventos em tempo real (Streaming).
    Lê o CSV linha a linha e envia para o Consumer via Server-Sent Events (SSE).
    """
    if not DATASET_PATH:
        yield "data: {\"error\": \"Arquivo CSV não encontrado no container\"}\n\n"
        return

    # Lê o dataset original
    df = pd.read_csv(DATASET_PATH)
    
    print(f"🚀 Iniciando stream de {len(df)} registros...")

    for i in range(len(df)):
        # Converte a linha do DataFrame para JSON
        data = df.iloc[i].to_json()
        
        # O formato 'data: {json}\n\n' é o padrão para protocolos SSE
        yield f"data: {data}\n\n"
        
        # Simula uma latência de 0.5 segundos entre eventos
        time.sleep(0.5)

@app.route('/stream')
def stream():
    """ Rota interna que o Consumer chama para receber os dados """
    return Response(generate(), mimetype='text/event-stream')

@app.route('/start')
def start():
    """ Rota que você acessa no navegador para iniciar a demonstração """
    return "🚀 Stream iniciado com sucesso! O pipeline está rodando."

if __name__ == '__main__':
    # Roda o servidor Flask na porta 5000
    # O host 0.0.0.0 permite que o container seja acessado externamente
    app.run(host='0.0.0.0', port=5000, debug=False)