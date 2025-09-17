"""
Escreva aqui o código Python para simular o funcionamento de um dispositivo. 
Lembre-se que:
    - A comunicação entre o dispositivo e a plataforma é feita através de um protocolo MQTT.
    - O dispositivo deve ser capaz de enviar mensagens para a plataforma e receber mensagens da plataforma.
    - Os dados são enviados para o tópico no formato '\<protocolo>\<chave>\<id do dispositivo>\attrs'
    - Os comandos são recebidos no tópico no formato '\<chave>\<id do dispositivo>\cmd'
    - Os resultados dos comandos são enviados para o tópico no formato '\<protocolo>\<chave>\<id do dispositivo>\cmdexe'
    - O dispositivo deve simular um sensor DHT22 (temperatura e umidade) e um módulo relé de estado (ligado/desligado).
"""

# Importando as bibliotecas necessárias. 
# Caso precise instalar as biliotecas use o comando abaixo:
# pip install paho-mqtt json
import paho.mqtt.client as mqtt
import json

#