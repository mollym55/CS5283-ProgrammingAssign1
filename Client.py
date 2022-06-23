# Import socket module
import socket
import re
import os
import sys
from urllib.parse import urlparse

os.environ['no_proxy'] = '127.0.0.1,localhost'
linkRegex = re.compile('<a\s*href=[\'|"](.*?)[\'"].*?>')
CRLF = "\r\n\r\n"
# default method
default = 'GET'  

def configClientTCP(url):
    socket.setdefaulttimeout(0.50)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.30)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if 'localhost' in url:
        path = getPath(url)

        HOST = 'localhost'
        if len(path) == 2:
            # drop any trailing paths to file. For example 8080/index.html --> 8080
            path = path[1].split('/')[0]
            PORT = int(path) if path.isdigit() else 80

    else:
        # break apart url to get what we need
        url = urlparse(url)
        path = getPath(url.netloc)

        HOST = path[0]  # The remote host
        PORT = int(path[1]) if len(path) == 2 else 80  # grab port from path else default to 80

    # connect to host
    s.connect((HOST, PORT))
    return s

def getPath(url):
    path = url.split(':')

    if len(path) == 1 or len(path) == 2:
        return path
    else:
        print("Invalid URL structure. You can only have at most one ':' in your URL.")
        exit()  # get out!


def GET(url, port):
    s = configClientTCP(url)
    path = urlparse(url).path
    msg = "GET %s HTTP/1.0%s" % (path, CRLF)
    s.send(msg.encode())
    data = (s.recv(10000000))
    if not data:
        exit()

    # shutdown and close tcp connection and socket
    s.shutdown(1)
    s.close()
    print(data.decode('UTF-8'))

def HEAD(url, port):
    s = configClientTCP(url)
    path = urlparse(url).path
    msg = "HEAD %s HTTP/1.0%s" % (path, CRLF)
    s.send(msg.encode())
    data = (s.recv(10000000))
    if not data:
        exit()

    # shutdown and close tcp connection and socket
    s.shutdown(1)
    s.close()


def main():
    url = ''
    method = ''

    if len(sys.argv) == 2:
        # grab command-line value
        url = sys.argv[1]

        # assign default
        method = default
        GET(url, method)

    elif len(sys.argv) == 3:
        # grab command-line values
        url = sys.argv[1]
        method = sys.argv[2].upper()
        HEAD(url,method)
main()
    
