import requests
import json
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

# Defina a chave de API e as coordenadas da localização desejada
API_KEY = "1b43995d45e76484eac79c54b28ad885" # Chave de API do Open Weather Map
LATITUDE = -23.73
LONGITUDE = -46.58
HOST = "Orion:1026"


# Função principal
def main():
    # Cria a entidade WeatherCurrent no Orion
    status_code = create_entity()
    
    # Verifica se a entidade foi criada com sucesso (201 Created)
    while status_code != 201 or status_code != 422:
        if status_code == 422:
            print("Entidade já existe, atualizando dados...")
            get_openweather()
            break
        elif status_code == 201:
            print("Entidade criada com sucesso!")
            get_openweather()
            break
        else:
            print("Erro ao criar a entidade. Código de status:", status_code)

    # Configura o agendador para executar a função a cada 1 minutos
    scheduler = BlockingScheduler()
    scheduler.add_job(get_openweather, 'interval', minutes=1)
    
    # Inicia o agendador
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass

# Função para obter dados do Open Weather Map API
def get_openweather():
    # Realiza a requisição para obter os dados do clima atual
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LATITUDE}&lon={LONGITUDE}&exclude=minutely,hourly&appid={API_KEY}&units=metric"
    payload = {}
    headers= {}
    response = requests.request("GET", url, headers=headers, data = payload)
    r = response.json()
    print(r)

    # Send Data to the entity "WeatherCurrent"
    url = f"http://{HOST}/v2/entities/urn:ngsi-ld:Weather:001/attrs"

    payload = json.dumps({
        "temperature": {
            "type": "Number",
            "value": r["main"]["temp"]
        },
        "pressure": {
            "type": "Number",
            "value": r["main"]["pressure"]
        },
        "humidity": {
            "type": "Number",
            "value": r["main"]["humidity"]
        }
    })

    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("PATCH", url, headers=headers, data = payload)
    print(response.text.encode('utf8'))

def create_entity():
    # Cria a entidade "WeatherCurrent" no Orion
    url = f"http://{HOST}/v2/entities"

    payload = json.dumps({
        "id": "urn:ngsi-ld:Weather:001",
        "type": "Weather",
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
    })

    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data = payload)
    print(response.text.encode('utf8'))
    return response.status_code
    
if __name__ == "__main__":
    main()
        
        