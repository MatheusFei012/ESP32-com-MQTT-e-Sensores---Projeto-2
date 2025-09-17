# Relatório Final

Nome: Matheus Da Silva Cruz
RA: 521240135

##  Introdução

Este projeto consiste no desenvolvimento e implementação de um sistema de monitoramento de temperatura utilizando uma arquitetura baseada em Internet das Coisas (IoT) com a plataforma FIWARE. O sistema tem como objetivo principal simular a operação de um dispositivo IoT que coleta dados de temperatura e umidade, além de controlar um atuador (módulo relé) para simular um sistema de ar-condicionado. Adicionalmente, o sistema integra dados climáticos externos de uma API de terceiros para enriquecer o contexto e permitir análises comparativas.

A arquitetura do projeto é composta por diversos componentes modulares, que trabalham em conjunto para garantir a coleta, processamento, gestão de contexto, persistência e visualização dos dados. Utilizamos o broker MQTT para a comunicação de mensagens entre o dispositivo simulado e a plataforma, que é então processada por um IoT Agent (JSON) para ser convertida para o padrão NGSI-LD, compreendido pelo Orion Context Broker. O Orion, por sua vez, atua como o coração do sistema, mantendo o estado em tempo real de todas as entidades e gerenciando as subscrições para a persistência de dados (via Cygnus) e para a integração com serviços externos.

A escolha dos componentes da plataforma FIWARE permite a criação de uma solução robusta, escalável e interoperável, seguindo padrões abertos para a construção de cidades inteligentes e outras aplicações IoT. Este documento detalha a estrutura do projeto, os componentes utilizados e as etapas para replicar e validar o sistema.

## Objetivo

O objetivo principal deste projeto é desenvolver e demonstrar um sistema de monitoramento de temperatura que simule o comportamento de um dispositivo IoT (sensor e atuador) e realize sua comunicação com uma plataforma de Internet das Coisas baseada em FIWARE. Mais especificamente, os objetivos secundários incluem:

* **Simular a leitura de um sensor DHT22/DHT11:** Desenvolver um script Python que gere dados de temperatura e umidade, simulando a operação de um sensor DHT22/DHT11.
* **Simular o controle de um módulo relé:** Implementar a lógica para que o script Python possa receber comandos para ativar ou desativar um atuador (simulando um ar-condicionado) via MQTT.
* **Estabelecer comunicação MQTT bidirecional:** Garantir que o dispositivo simulado possa publicar dados de sensor e receber comandos de controle através de um broker MQTT (Mosquitto).
* **Integrar o dispositivo à plataforma FIWARE:** Registrar o dispositivo no IoT Agent JSON, configurando-o para que seus dados sejam enviados ao Orion Context Broker e seus comandos sejam recebidos de forma adequada.
* **Gerenciar o contexto de informações com o Orion Context Broker (OCB):**
    * Assegurar que os dados do sensor cheguem e sejam armazenados corretamente como entidades no OCB.
    * Integrar dados climáticos externos de uma API (OpenWeatherMap) no OCB, enriquecendo o contexto das informações.
* **Persistir dados com o Cygnus:** Configurar o Cygnus para receber dados do OCB e persistí-los em um banco de dados (MySQL ou MongoDB) para análise histórica.
* **Visualizar dados com o Grafana:** Criar um painel personalizado no Grafana para exibir:
    * Gráficos históricos de temperatura interna (do sensor simulado) e externa (da API climática).
    * Valores presentes (últimos dados) de temperatura interna e externa.
* **Validar a comunicação e o fluxo de dados:** Utilizar ferramentas como MQTTX e comandos cURL para verificar a correta operação de cada componente e o fluxo de informações através de toda a arquitetura.

Este projeto visa proporcionar uma compreensão prática de como construir uma solução IoT completa utilizando componentes FIWARE, desde a simulação do dispositivo até a visualização dos dados em um painel interativo.

## Dispositivo IoT

O dispositivo IoT desenvolvido simula as seguintes funcionalidades:

* Leitura de Temperatura e Umidade (DHT22 simulado): O script Python simula a coleta de dados de temperatura e umidade, gerando valores aleatórios dentro de uma faixa realista para um ambiente interno.

* Envio de Dados via MQTT: Os dados de temperatura e umidade simulados são publicados periodicamente em um tópico MQTT específico para o sensor, permitindo que a plataforma IoT os consuma.

* Recepção de Comandos de Controle (Módulo Relé simulado): O script Python se inscreve em um tópico MQTT de comando para o módulo relé, aguardando instruções para ligar ou desligar o atuador (simulando um ar-condicionado).

* Atuação do Módulo Relé (simulado): Ao receber um comando de "ligar" ou "desligar" via MQTT, o script simula a mudança de estado do relé e, consequentemente, do ar-condicionado.

* Confirmação de Execução de Comando: Após processar um comando recebido, o dispositivo envia uma mensagem de retorno (confirmação ou status) para o Broker MQTT, indicando que a ação foi executada.

# Códigos e suas Explicações

## Relatório Técnico – Simulador IoT com MQTT em Python

---

##  Descrição Completa
Simulador de dispositivo IoT com:
- Sensor DHT22 virtual (temperatura/umidade)
- Módulo relé controlável
- Comunicação via MQTT com JSON

## Configuração e Código Principal

### device.py

```python
# Importando as bibliotecas necessárias. 
# Caso precise instalar as biliotecas use o comando abaixo:
# pip install paho-mqtt json

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
```
### Explicação:

Este código em Python implementa um cliente MQTT utilizando a biblioteca paho.mqtt.client para simular um dispositivo IoT que envia dados de temperatura e umidade, além de receber e responder comandos de controle (ligar/desligar um relé). Abaixo está o resumo detalhado do seu funcionamento:

### 1. Definições Iniciais

* CHAVE e DISPOSITIVO: Identificadores do dispositivo IoT e da chave de autenticação.
* TOPICO_ENVIO: Tópico MQTT onde os dados do sensor (temperatura e umidade) são publicados.
* TOPICO_COMANDO: Tópico onde o dispositivo escuta comandos externos (como ligar/desligar o relé).
* TOPICO_RESPOSTA: Tópico usado para responder à execução dos comandos recebidos.

### 2. Função on_connect

* Callback executado quando o cliente MQTT se conecta ao broker.
* Imprime uma mensagem de sucesso com o código de retorno da conexão (rc).
* Realiza a inscrição (subscribe) no tópico de comando, para que o cliente possa escutar mensagens vindas do servidor.

### 3. Função on_message

 Callback executado quando uma mensagem é recebida no tópico ao qual o cliente está inscrito.

* Decodifica e exibe o comando recebido.
* Interpreta o comando como JSON.
* Verifica se há uma instrução para o relé:

"relay": "on" → liga o relé e responde com "relay": "ligado".

"relay": "off" → desliga o relé e responde com "relay": "desligado".

* Caso contrário, retorna erro com "erro": "Comando inválido".
* Publica a resposta no tópico de resposta definido.

### 4. Configuração do Cliente MQTT

* Cria o cliente usando a versão 2 da API de callbacks do paho.mqtt.client.
* Associa as funções on_connect e on_message aos respectivos eventos.
* Conecta ao broker MQTT local (localhost na porta 1883).
* Inicia o loop de eventos do cliente (loop_start()), que roda em segundo plano.

### 5. Loop de Envio de Dados

* Dentro de um try contínuo:
* Gera aleatoriamente valores de temperatura (20.0 a 30.0 °C) e umidade (40.0 a 60.0 %).
* Monta um dicionário com os dados e converte para JSON.
* Publica os dados no tópico de envio.
* Exibe os dados enviados no terminal.
* Espera 10 segundos antes de repetir.

### 6. Encerramento Gracioso

* Se o programa for interrompido pelo usuário (ex: Ctrl+C):
* Exibe mensagem de encerramento.
* Para o loop MQTT (loop_stop()).
* Desconecta do broker (disconnect()).

### Resumo Funcional

* Este código simula um sensor IoT com MQTT:
* Publica leituras periódicas de temperatura e umidade.
* Escuta comandos para controle de um relé (liga/desliga).
* Responde aos comandos recebidos com confirmações ou mensagens de erro.
* É útil para testes locais com brokers MQTT e prototipagem de soluções IoT.

## Código Postman

![image](https://github.com/user-attachments/assets/9b58d125-a3ef-4e58-871b-d9113381aade)

## POST

### http://{{orion}}/v2/entities/
```json
{
    "id": "urn:ngsi-ld:Weather:001",
    "type": "Weather",
    "dateObserved": {
        "type": "Datetime"
    },
    "temperature": {
        "type": "Number",
        "value": 0
    },
    "pressure": {
        "type": "Number",
        "value": 0
    },
    "humidity": {
        "type": "Number",
        "value": 0
    }
}
```

"id": "urn:ngsi-ld:Weather:001"

* Um identificador único para a entidade do tipo Weather (tempo climático).
* O prefixo urn:ngsi-ld: é uma convenção para entidades no padrão NGSI-LD (mas Orion também aceita NGSIv2).
* "type": "Weather"
* O tipo da entidade, que neste caso representa dados meteorológicos.
* "dateObserved"
* Um atributo que indica a data e hora da observação.
* Aqui está apenas definido o tipo como "Datetime", mas não há valor preenchido ainda.
* "temperature", "pressure" e "humidity"
* São atributos numéricos (com "type": "Number"), cada um com valor inicial igual a 0.

### Objetivo:

* Essa requisição está criando uma nova entidade no Orion Context Broker representando uma medição do clima com valores iniciais zerados, para depois serem atualizados conforme os dados forem coletados (por sensores, por exemplo).

### http://{{orion}}/v2/subscriptions/

```json
{
    "description": "Sobscrevendo a mudanças na entidade",
    "subject": {
        "entities": [
            {
                "id": "dht22_001",
                "type": "Device"
            }
        ]
    },
    "notification": {
        "http": {
            "url": "http://cygnus:5050/notify"
        },
        "attrs": [
            "temperature",
            "humidity"
        ]
    },
    "throttling": 5
}
```

* Monitora a entidade dht22_001 do tipo Device.
* Atributos observados: temperature e humidity.
* Sempre que um desses valores mudar, Orion envia uma notificação HTTP POST para:
* http://cygnus:5050/notify (no caso, o conector Cygnus).
* throttling: 5 → Limita as notificações para no máximo uma a cada 5 segundos, mesmo que os valores mudem com mais frequência.

### Objetivo:

* Enviar os dados automaticamente para outros serviços (como Cygnus, QuantumLeap, etc).
* Ideal para armazenar dados históricos, visualizar gráficos, ou reagir a eventos (ex: alertas).

### GET

* 1. GET http://{{orion}}/v2/entities/urn:ngsi-ld:Weather:001?options=keyValues

Para que serve:
Lê todos os atributos da entidade Weather:001.
A opção options=keyValues faz com que a resposta venha de forma simples, apenas com os valores (sem metadados).

```json
{
  "id": "urn:ngsi-ld:Weather:001",
  "type": "Weather",
  "temperature": 26.5,
  "humidity": 58,
  "pressure": 1012
}
```

* 2. GET http://{{orion}}/v2/entities/urn:ngsi-ld:Device:001?options=keyValues

Para que serve:
Similar ao anterior, mas agora está consultando uma entidade diferente: Device:001.
Essa entidade pode representar um dispositivo físico, como um sensor ou atuador.

```json
{
  "id": "urn:ngsi-ld:Device:001",
  "type": "Device",
  "status": "on",
  "lastSeen": "2025-05-30T14:10:00Z"
}
```

* 3. GET http://localhost:1026/v2/subscriptions/

Para que serve:
Lista todas as subscrições ativas no Orion.
Subscrições são usadas para monitorar mudanças de dados e enviar notificações para um endpoint (como uma URL webhook).

```json
[
  {
    "id": "68311c6d8ac18490c10b75c3",
    "description": "Notifica quando temperatura muda",
    "subject": {
      "entities": [
        { "id": "urn:ngsi-ld:Weather:001" }
      ],
      "condition": {
        "attrs": ["temperature"]
      }
    },
    "notification": {
      "http": { "url": "http://meuendpoint/api" },
      "attrs": ["temperature"]
    },
    "status": "active"
  }
]
```
### PATCH

```json
{
  "activate": {
    "type": "command",
    "value": "on"
  }
}
```
Envia o comando "on" para o dispositivo Device:001, indicando que ele deve ligar.

### Como funciona:

* activate é um comando reconhecido pelo IoT Agent.
* O IoT Agent recebe esse comando e executa a ação no dispositivo físico (como acender uma luz ou ligar um motor).
* Esse comando é normalmente usado com dispositivos conectados via IoT Agent (ex: JSON, MQTT, UL, etc).

### DEL

### Objetivo:

* Remove a subscrição identificada pelo ID.
* Após a remoção:
* O Orion não enviará mais notificações relacionadas a essa subscrição.
* O recurso (como Cygnus, QuantumLeap, etc.) deixará de ser informado sobre mudanças nas entidades monitoradas.

### Quando usar:

* Quando você não precisa mais acompanhar mudanças em uma entidade.
* Para limpar subscrições antigas ou duplicadas.
* Em casos de ajuste ou reinicialização de componentes (como o Cygnus ou IoT Agent).

## Interface de Usuário.

![Grafana, tela ](https://github.com/user-attachments/assets/6aae95f9-d905-4647-961e-823e4d21bbe0)

### O que a imagem mostra:

* Gráfico:
* Cada ponto representa um valor de temperatura ou umidade ao longo do tempo.
* Os dados estão sendo atualizados rapidamente (intervalos de poucos segundos).
* O gráfico mostra grande variação (oscilação), indicando mudança constante nos sensores.

### Consulta SQL usada (abaixo do gráfico):

```sql
SELECT
  STR_TO_DATE(recvTime, '%Y-%m-%d %H:%i:%s.%f') AS time,
  CAST(attrValue AS DECIMAL(10,2)) AS data
FROM
  openiot.dht22_001_TemperatureSensor
WHERE
  attrName IN ('temperature', 'humidity');
```

* STR_TO_DATE(recvTime, '%Y-%m-%d %H:%i:%s.%f') AS time:
Converte a string de data e hora (recvTime) para o formato de data/hora real (datetime), que o Grafana entende como eixo de tempo.

* CAST(attrValue AS DECIMAL(10,2)) AS data:
Converte o valor (attrValue) de texto para número decimal, com duas casas decimais.
Isso garante que os valores como temperatura ou umidade possam ser corretamente exibidos como números no gráfico.

* openiot.dht22_001_TemperatureSensor:
Define de qual tabela os dados estão sendo buscados:
openiot.dht22_001_TemperatureSensor
Essa tabela foi criada pelo Cygnus, que gravou os dados enviados pelo Orion Context Broker.

* attrName IN ('temperature', 'humidity'); Filtra os dados para mostrar somente os registros de temperature e humidity.
Isso é útil se a tabela tiver também outros atributos (como pressão, luminosidade, etc), que não são relevantes nesse gráfico.

### Como funciona por trás:

* Orion Context Broker recebe os dados do sensor.
* Subscrição envia esses dados para o Cygnus.
* Cygnus grava os dados no MySQL na tabela openiot.dht22_001_TemperatureSensor.
* O Grafana consulta esse banco e gera o gráfico.

## Conclusão

A execução deste projeto teve como objetivo o desenvolvimento de um sistema simples de monitoramento de temperatura utilizando um sensor DHT22, um módulo relé de 1 canal (para controle do ar-condicionado), uma API climática externa e uma arquitetura baseada na plataforma FIWARE. Foram utilizados componentes como o IoT Agent JSON, Orion Context Broker (OCB), Cygnus, MySQL, MongoDB e Mosquitto MQTT Broker para garantir a integração, persistência e visualização dos dados coletados.

O objetivo do projeto foi plenamente atingido. Foi possível simular com sucesso a leitura periódica de temperatura pelo sensor DHT22, o envio dessas leituras via MQTT ao Mosquitto Broker, e o controle do módulo relé com base em comandos MQTT. Além disso, o sistema foi capaz de se comunicar adequadamente com o IoT Agent JSON, garantindo que os dados fossem recebidos pelo Orion Context Broker. O OCB foi configurado com subscrições específicas, possibilitando o envio dos dados ao Cygnus e sua posterior persistência em banco de dados (MySQL/MongoDB). A API do OpenWeather foi devidamente integrada através do serviço Proxy-Clima, e os dados externos foram registrados como entidades distintas no OCB.

O único contratempo significativo enfrentado durante o desenvolvimento foi relacionado ao uso do Postman para testes de requisições HTTP. Durante os testes com métodos POST e GET, algumas inconsistências foram observadas, especialmente na validação de respostas e headers. Como alternativa, foi necessário criar um método DELETE para realizar limpezas pontuais e corrigir conflitos de entidades durante o desenvolvimento. Fora isso, todos os componentes da arquitetura se comportaram como esperado.

Os principais aprendizados obtidos incluem a compreensão mais profunda do funcionamento da arquitetura FIWARE, especialmente a integração entre seus componentes centrais (IoT Agent, OCB, Cygnus), o uso do protocolo MQTT para simulações em tempo real e o consumo de APIs externas em ambientes IoT. O projeto também proporcionou uma boa experiência prática com a criação de subscrições, persistência de dados e visualização com o Grafana, fortalecendo os conhecimentos sobre arquiteturas orientadas a contexto e Big Data.

Como melhorias futuras, seria interessante:

* Automatizar o provisionamento de entidades e dispositivos no IoT Agent por meio de scripts.
* Integrar funcionalidades de alerta em tempo real (ex.: e-mail ou Telegram) quando a temperatura ultrapassar determinados limites.
* Adicionar sensores adicionais (ex.: umidade ou presença) para enriquecer os dados coletados.
* Implementar autenticação JWT entre os serviços para aumentar a segurança da plataforma.

Por fim, o painel desenvolvido no Grafana permitiu uma visualização clara e objetiva tanto dos dados históricos quanto dos últimos valores de temperatura (interna e externa), o que demonstra a eficiência e aplicabilidade da solução proposta em contextos reais de monitoramento ambiental e automação de sistemas HVAC.





















