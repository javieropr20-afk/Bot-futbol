import time
import requests

# --- CONFIGURACIÓN ---
TELEGRAM_TOKEN = "8936396425:AAFMF0LIoDpFsiSuhnC0BjzK4a2CvZtmpnI"
TELEGRAM_CHAT_ID = "1360963923"
API_FOOTBALL_KEY = "f760f2558b2c1c3f12b76cf0a2754dbc6194e673d7d510ef261367576f7bb4f8"

# Memoria para no repetir alertas del mismo partido
partidos_alertados = set()

def enviar_telegram(mensaje):
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    datos = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensaje,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=datos)

def obtener_partidos_en_vivo():
    url = "https://api-sports.io"
    headers = {"x-apisports-key": API_FOOTBALL_KEY}
    respuesta = requests.get(url, headers=headers)
    if respuesta.status_code == 200:
        return respuesta.json().get("response", [])
    return []

def analizar_partidos():
    partidos = obtener_partidos_en_vivo()
    print(f"Analizando {len(partidos)} partidos en vivo...")

    for partido in partidos:
        fixture_id = partido["fixture"]["id"]
        minuto = partido["fixture"]["status"]["elapsed"]
        liga = partido["league"]["name"]
        pais = partido["league"]["country"]
        
        local = partido["teams"]["home"]["name"]
        visitante = partido["teams"]["away"]["name"]
        goles_local = partido["goals"]["home"]
        goles_visitante = partido["goals"]["away"]

        # Filtro 1: Entre minuto 70 y 85, partido empatado o diferencia de 1 gol
        if minuto and 70 <= minuto <= 85 and abs(goles_local - goles_visitante) <= 1:
            if fixture_id not in partidos_alertados:
                # Construir alerta
                mensaje = (
                    f"⚽ *ALERTA DE POSIBLE GOL TARDÍO*\n\n"
                    f"🏆 *Liga:* {liga} ({pais})\n"
                    f"🆚 *Partido:* {local} {goles_local} - {goles_visitante} {visitante}\n"
                    f"⏱ *Minuto:* {minuto}'\n\n"
                    f"📊 Revisa estadísticas en vivo para entrar al mercado Over."
                )
                enviar_telegram(mensaje)
                partidos_alertados.add(fixture_id)
                print(f"Alerta enviada: {local} vs {visitante}")

if __name__ == "__main__":
    enviar_telegram("🤖 *Bot de fútbol iniciado correctamente.*")
    while True:
        try:
            analizar_partidos()
        except Exception as e:
            print(f"Error en el ciclo: {e}")
        
        # Espera 15 minutos (900 seg) para cuidar las 100 peticiones gratis diarias
        time.sleep(900)
