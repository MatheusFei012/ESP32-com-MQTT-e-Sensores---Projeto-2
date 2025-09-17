# Utilizado o comando "pip install paho-mqtt" para instalar a biblioteca paho-mqtt

import paho.mqtt.client as mqtt
import json
import time

# Este script cria um cliente MQTT que se conecta ao mosquitto localmente. 
# O comando deve ser definido como uma subscrição. Para cada subscrição, tem-se um dispositivo diferente. 
# Lembre-se que os comandos do fiware são enviados para “/<chave>/<id do dispositivo>/cmd”

CHAVE = "4jggokgpepnvsb2uv4s40d59ov" # Chave do dispositivo
DISPOSITIVO = "urn:ngsi-ld:Bell:001" # ID do dispositivo

# Função de callback quando o cliente se conecta ao broker
def on_connect(client, userdata, flags, reasonCode, properties):
    print("Conectado com o resultado: " + str(reasonCode))
    client.subscribe(f"/{CHAVE}/+/cmd")

    
# Função de callback quando uma mensagem é recebida
def on_message(client, userdata, msg):
    print("Mensagem recebida no tópico: " + msg.topic)
    print("Mensagem: " + str(msg.payload.decode()))
    
    # Aqui você pode adicionar o código para processar a mensagem recebida
    # Se a mensagem for do dispositivo "urn:ngsi-ld:Bell:001"
    if msg.topic == f"/{CHAVE}/{DISPOSITIVO}/cmd":
        # Decodifica a mensagem json e converte para dicionário
        # msg.payload.decode() -> converte a mensagem de bytes para string
        mensagem = json.loads(msg.payload.decode())
        # Aqui você pode adicionar o código para processar a mensagem recebida
        if "ring" in mensagem:
            # Se a mensagem contiver o comando "ring"
            print("Blim Blim Blim")
            
            # Aqui você deveria enviar uma mensagem de execução do comando via publicação. 
            # Exemplo:
            client.publish(f"/{CHAVE}/{DISPOSITIVO}/cmdexe", json.dumps({"ring": "Executado"}))
        
    
# Cria um cliente MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
# Define as funções de callback
client.on_connect = on_connect
client.on_message = on_message
# Conecta-se ao broker MQTT local
client.connect("localhost", 1883, 60)
# Inicia o loop do cliente
# Inicia o loop do cliente sem bloquear 
client.loop_start()

time.sleep(1) # Aguarda 1 segundo para garantir que o cliente esteja conectado
