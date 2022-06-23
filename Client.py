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


def GET(host, port, path):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.50)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((host, port))
    msg = "GET %s HTTP/1.0%s" % (path, CRLF)
    s.send(msg.encode())
    dataAppend = ''
    while 1:
        data = (s.recv(10000000))
        if not data: break
        else:
            dataAppend = dataAppend, repr(data)
    s.shutdown(1)
    s.close()
    print_result(dataAppend)

def HEAD(host, port, path):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.50)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((host, port))
    msg = "HEAD %s HTTP/1.0%s" % (path, CRLF)
    s.send(msg.encode())
    dataAppend = ''
    while 1:
        data = (s.recv(10000000))
        if not data: break
        else:
            dataAppend = dataAppend, repr(data)
    s.shutdown(1)
    s.close()
    print_result(dataAppend)

def print_result(data):
    if len(data[1]) > 0:
        data = data[1]
    else:
        data = data[0]
    data = data.replace("\\n", "\n")
    data = data.replace("\\r", "\r")
    data = data.replace("\\t", "\t")
    data = data.replace("b'", "")
    data = data.replace("'", "")
    print("\n", data)


if __name__ == "__main__":
    """python Client.py host:port/path [METHOD]"""
    usage = "python Client.py host:port/path [METHOD]"
    if len(sys.argv) < 3:
        print(usage)
        sys.exit(1)
        
    
    if "http://" in sys.argv[1]:
        url = sys.argv[2].replace("http://", "")
    host = sys.argv[2]
    port = int(url.split(":")[2].split("/")[1])
    path = url.find("/")
    if path == -1:
        path = "/"
    else:
        path = url[path:]
    #print("host: %s, port: %d, path: %s" % (host, port, path))
    if sys.argv[2] == "GET":
        GET(host, port, path)
    elif sys.argv[2] == "HEAD":
        HEAD(host, port, path)
    
    
