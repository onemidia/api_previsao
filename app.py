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
def generate_rss():
    """Gera o feed RSS com os dados da previsão do tempo formatados para o Xibo."""
    response = requests.get(URL)
    weather_data = response.json()

    rss = ET.Element("rss", version="2.0", xmlns_media="http://search.yahoo.com/mrss/")
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = "Previsão do Tempo - Taquaritinga"
    ET.SubElement(channel, "link").text = "http://m.onemidia.tv.br"
    ET.SubElement(channel, "description").text = "Previsão do tempo para os próximos dias"

    for forecast in weather_data["list"][:5]:  # Pegando apenas os primeiros 5 períodos
        weather_icon_code = forecast["weather"][0]["icon"]
        icon_url = get_xibo_icon(weather_icon_code)
        temp = forecast["main"]["temp"]
        description = forecast["weather"][0]["description"].capitalize()

        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = "Previsão do Tempo"
        ET.SubElement(item, "description").text = f"{description} - {temp}°C"
        ET.SubElement(item, "link").text = "http://m.onemidia.tv.br"
        media_content = ET.SubElement(item, "media:content", url=icon_url, type="image/png")

    rss_feed = ET.tostring(rss, encoding="utf-8", method="xml").decode()
    return Response(rss_feed, mimetype="application/xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
