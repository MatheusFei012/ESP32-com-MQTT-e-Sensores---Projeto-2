# Utilizado o comando "pip install paho-mqtt" para instalar a biblioteca paho-mqtt

import paho.mqtt.client as mqtt
import json
import time

# Este script cria um cliente MQTT que se conecta ao mosquitto localmente. 
# O comando deve ser definido como uma subscrição. Para cada subscrição, tem-se um dispositivo diferente. 
# Lembre-se que os comandos do fiware são enviados para “/<chave>/<id do dispositivo>/cmd”

CHAVE = "4jggokgpepnvsb2uv4s40d59ov" # Chave do dispositivo
DISPOSITIVO = "urn:ngsi-ld:Motion:001" # ID do dispositivo

# Função de callback quando o cliente se conecta ao broker
def on_connect(client, userdata, flags, reasonCode, properties):
    print("Conectado com o resultado: " + str(reasonCode))
    client.subscribe(f"/{CHAVE}/+/cmd")

    
# Função de callback quando uma mensagem é recebida
def on_message(client, userdata, msg):
    print("Mensagem recebida no tópico: " + msg.topic)
    print("Mensagem: " + str(msg.payload.decode()))
        
# Cria um cliente MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
# Define as funções de callback
client.on_connect = on_connect
client.on_message = on_message
# Conecta-se ao broker MQTT local
client.connect("localhost", 1883, 60)
# Inicia o loop do cliente sem bloquear 
client.loop_start()

time.sleep(1) # Aguarda 1 segundo para garantir que o cliente esteja conectado
c = 0

while True:
    input("Aperte 'enter' para passar no sensor!")
    # Envia uma mensagem para atualizar o contador "c" do sensor. 
    client.publish(f"/json/{CHAVE}/{DISPOSITIVO}/attrs", json.dumps({"c": c}))
    c = c + 1
    