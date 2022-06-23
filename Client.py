# Import socket module
import socket
import re
import os
import sys
from urllib.parse import urlparse

os.environ['no_proxy'] = '127.0.0.1,localhost'
linkRegex = re.compile('<a\s*href=[\'|"](.*?)[\'"].*?>')
CRLF = "\r\n\r\n"
default = 'GET'  

def config(url):
    socket.setdefaulttimeout(0.50)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.30)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if 'localhost' in url:
        path = getPath(url)

        HOST = 'localhost'
        if len(path) == 2:
            path = path[1].split('/')[0]
            PORT = int(path) if path.isdigit() else 80

    else:
        url = urlparse(url)
        path = getPath(url.netloc)

        HOST = path[0]  
        PORT = int(path[1]) if len(path) == 2 else 80  

    s.connect((HOST, PORT))
    return s

def getPath(url):
    path = url.split(':')

    if len(path) == 1 or len(path) == 2:
        return path
    else:
        print("Invalid, now exiting!!")
        exit()  


def GET(url, port):
    s = config(url)
    path = urlparse(url).path
    msg = "GET %s HTTP/1.0%s" % (path, CRLF)
    s.send(msg.encode())
    data = (s.recv(10000000))
    if not data:
        exit()

    s.shutdown(1)
    s.close()
    print(data.decode('UTF-8'))

def HEAD(url, port):
    s = config(url)
    path = urlparse(url).path
    msg = "HEAD %s HTTP/1.0%s" % (path, CRLF)
    s.send(msg.encode())
    data = (s.recv(10000000))
    if not data:
        exit()
        
    s.shutdown(1)
    s.close()


def main():
    path = ""
    method = ""

    if len(sys.argv) == 2:
        path = sys.argv[1]
        method = default
        GET(path, method)

    elif len(sys.argv) == 3:
        path = sys.argv[1]
        method = sys.argv[2].upper()
        HEAD(path,method)
main()
    
