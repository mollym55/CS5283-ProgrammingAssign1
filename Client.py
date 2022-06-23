# Import socket module
import socket
import re
import os
import sys

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


def main():
    url = ''
    method = ''

    if len(sys.argv) == 2:
        # grab command-line value
        url = sys.argv[1]

        # assign default
        method = default

    elif len(sys.argv) == 3:
        # grab command-line values
        url = sys.argv[1]
        method = sys.argv[2].upper()
        
    else:
        # too few or many arguments -- display error and exit
        Err.displayCountError()
        exit()
