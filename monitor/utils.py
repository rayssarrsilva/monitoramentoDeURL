import requests

def verificar_status(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return 'online'
        return 'offline'
    except:
        return 'offline'
