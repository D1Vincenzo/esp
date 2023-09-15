import socket
from unlocker import light_off
from light_off_webpage import *

def handle_client(client):
    request = client.recv(1024).decode('utf-8')
    print('Received request:')
    print(request)

    if 'GET /lightoff' in request:
        light_off()
        response = 'OK'
       
#    elif 'GET /poweroff' in request:
#        poweroff()
#        response = 'OK'

    else:
        response = html

    client.send('HTTP/1.1 200 OK\n')
    client.send('Content-Type: text/html\n')
    client.send('Connection: close\n\n')
    client.sendall(response)
    client.close()

def start_web():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)

    print('Server listening on port 80...')

    # 监听连接并处理请求
    while True:
        client, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        handle_client(client)

if __name__ == "__main__":
    start_web()
