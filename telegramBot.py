import requests

#envia_msg
TOKEN = '8718298300:AAFK_X2P2D1u7uAUa6Lq05OaRgAw_RXqTBU'
CHAT_ID = '6215630573'

def envia_msg(msg):
    requests.post(
        f'https://api.telegram.org/bot{TOKEN}/sendMessage',
        data={'chat_id': CHAT_ID, 'text': msg},
        timeout=5
    )


#envia_imagem
def envia_imagem(caminho):
    url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
    
    with open(caminho, 'rb') as foto:
        files = {'photo': foto}
        data = {'chat_id': CHAT_ID}
        
        r = requests.post(url, files=files, data=data)
    
    return r