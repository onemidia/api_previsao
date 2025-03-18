from flask import Flask, Response
import requests
import datetime

app = Flask(__name__)

# Sua chave de API do OpenWeather
API_KEY = '9a0dec7f2d04b94b78a7db7f1193fc51'
CITY = 'Taquaritinga,BR'
URL = f'http://api.openweathermap.org/data/2.5/forecast?q={CITY}&units=metric&cnt=5&appid={API_KEY}'

@app.route("/rss")
def gerar_rss():
    response = requests.get(URL)
    weather_data = response.json()

    # Pega o ícone para o primeiro item (ou você pode ajustar para pegar o ícone que deseja)
    icon_code = weather_data['list'][0]['weather'][0]['icon']
    icon_url = f"https://openweathermap.org/img/wn/{icon_code}.png"
    
    # Formatação da data
    agora = datetime.datetime.now()
    data_formatada = agora.strftime("%Y-%m-%d %H:%M:%S")

    # Criação do XML RSS
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
    <channel>
        <title>Previsão do Tempo</title>
        <description>Feed de previsão do tempo para Taquaritinga, SP</description>
        <link>https://seu-servidor.onrender.com/rss</link>
        <lastBuildDate>{data_formatada}</lastBuildDate>
        <item>
            <title>Previsão de hoje</title>
            <description>Temperatura: {weather_data['list'][0]['main']['temp']}°C, {weather_data['list'][0]['weather'][0]['description']}</description>
            <link>https://seu-servidor.onrender.com/rss</link>
            <image>
                <url>{icon_url}</url>
                <title>Ícone do tempo</title>
            </image>
        </item>
    </channel>
</rss>
"""
    return Response(xml, mimetype="application/rss+xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
