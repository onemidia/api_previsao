from flask import Flask, Response
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

# Chave da API do OpenWeatherMap
API_KEY = "9a0dec7f2d04b94b78a7db7f1193fc51"
CITY = "Taquaritinga,BR"
URL = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric&lang=pt_br"

# Mapeamento de ícones do OpenWeatherMap para IDs no Xibo
icon_map = {
    "01d": "48165", "01n": "48166", "02d": "48170", "02n": "48168",
    "03d": "48169", "03n": "48167", "04d": "48171", "04n": "48172",
    "09d": "48174", "09n": "48173", "10d": "48177", "10n": "48176",
    "11d": "48175", "11n": "48178", "13d": "48179", "13n": "48180",
    "50d": "48152", "50n": "48149"
}

def get_xibo_icon(weather_icon_code):
    """Retorna a URL do ícone do Xibo correspondente ao código do OpenWeatherMap."""
    xibo_icon_id = icon_map.get(weather_icon_code, "48165")  # Ícone padrão: céu limpo (dia)
    return f"http://m.onemidia.tv.br/library/preview/{xibo_icon_id}"

@app.route("/rss")
def gerar_rss():
    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
        <channel>
            <title>Previsão do Tempo</title>
            <description>Feed de previsão do tempo</description>
            <link>https://seu-servidor.onrender.com/rss</link>
            <item>
                <title>Previsão de hoje</title>
                <description>Tempo ensolarado com máximas de 30°C</description>
                <link>https://seu-servidor.onrender.com/rss</link>
            </item>
        </channel>
    </rss>
    """
    return Response(xml, mimetype="application/rss+xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
