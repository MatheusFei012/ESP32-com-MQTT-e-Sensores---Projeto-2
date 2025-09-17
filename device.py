import paho.mqtt.client as mqtt
import json
import time
import random

CHAVE = "4jggokgpepnvsb2uv4s40d59ov"
DISPOSITIVO = "dht22_001"

TOPICO_ENVIO = f"/json/{CHAVE}/{DISPOSITIVO}/attrs"
TOPICO_COMANDO = f"/1234iotapikey/{DISPOSITIVO}/cmd"
TOPICO_RESPOSTA = f"/json/1234iotapikey/{DISPOSITIVO}/cmdexe"

# Callback de conexão
def on_connect(client, userdata, flags, rc, properties=None):
    print("Conectado ao broker com resultado: " + str(rc))
    client.subscribe(TOPICO_COMANDO)

def on_message(client, userdata, msg):
    print(f"[COMANDO RECEBIDO] {msg.topic}: {msg.payload.decode()}")
    try:
        comando = json.loads(msg.payload.decode())
        if comando.get("relay") == "on":
            print(">>> Relé ligado")
            resposta = {"relay": "ligado"}
        elif comando.get("relay") == "off":
            print(">>> Relé desligado")
            resposta = {"relay": "desligado"}
        else:
            print(">>> Comando desconhecido")
            resposta = {"erro": "Comando inválido"}
        client.publish(TOPICO_RESPOSTA, json.dumps(resposta))
    except Exception as e:
        print("Erro ao processar comando:", e)

# Setup MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.loop_start()

# Loop de envio de dados
try:
    while True:
        temperatura = round(random.uniform(20.0, 30.0), 2)
        umidade = round(random.uniform(40.0, 60.0), 2)
        dados = {
            "temperature": temperatura,
            "humidity": umidade
        }
        client.publish(TOPICO_ENVIO, json.dumps(dados))
        print(f"[DADOS ENVIADOS] {dados}")
        time.sleep(10)
except KeyboardInterrupt:
    print("Encerrando...")
    client.loop_stop()
    client.disconnect()
