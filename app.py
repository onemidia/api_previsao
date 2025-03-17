from flask import Flask, Response
import requests
import xml.etree.ElementTree as ET
import os

# Obtendo variáveis do ambiente
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY = os.getenv("CITY", "Taquaritinga")
COUNTRY = os.getenv("COUNTRY", "BR")
XIBO_ICON_URL = os.getenv("XIBO_ICON_URL", "https://seu-xibo.com/icones")

app = Flask(__name__)

API_URL = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY},{COUNTRY}&appid={OPENWEATHER_API_KEY}&units=metric&lang=pt"

def generate_rss(data):
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = f"Previsão do Tempo - {CITY}"
    ET.SubElement(channel, "link").text = "https://seu-dominio.com/rss"
    ET.SubElement(channel, "description").text = "Previsão do tempo para os próximos 5 dias."
    
    added_dates = set()
    
    for item in data['list']:
        date = item['dt_txt'].split(" ")[0]  # Pegando apenas a data (YYYY-MM-DD)
        if date not in added_dates:
            added_dates.add(date)
            entry = ET.SubElement(channel, "item")
            temp = item['main']['temp']
            weather_desc = item['weather'][0]['description'].capitalize()
            icon_code = item['weather'][0]['icon']
            icon_url = f"{XIBO_ICON_URL}/{icon_code}.png"
            
            ET.SubElement(entry, "title").text = f"{date}: {weather_desc}, {temp}°C"
            ET.SubElement(entry, "description").text = f"Temperatura: {temp}°C - {weather_desc}"
            ET.SubElement(entry, "link").text = "https://seu-dominio.com/rss"
            ET.SubElement(entry, "pubDate").text = date
            enclosure = ET.SubElement(entry, "enclosure")
            enclosure.set("url", icon_url)
            enclosure.set("type", "image/png")
    
    return ET.tostring(rss, encoding='utf8', method='xml')

@app.route("/rss")
def rss_feed():
    response = requests.get(API_URL)
    if response.status_code == 200:
        rss = generate_rss(response.json())
        return Response(rss, mimetype='application/rss+xml')
    return "Erro ao obter dados", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)