import socket
import sys
import datetime
import locale
locale.setlocale(locale.LC_TIME, 'en_US')


class server():
    def __init__(self, port, directory, host='localhost'):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(1)
        print('Listening on:', port)
        self.sock = sock

    def serve(self):
        while True:
            con, address = self.sock.accept()
            print('Connection from', address)
            request = con.recv(1024)
            request = request.decode()
            print('Request:', request)
            self.handle(request, con)
            con.close()


    def handle(self, request, con):
        request = request.split(" ")
        if request[0] == "GET":
            self.get(request[1], con)
        elif request[0] == "HEAD":
            self.head(request[1], con)
        else:
            self.error(con)

    def default_headers(self, status_code=200, content_len=None):
        headers = "HTTP/1.1 " + str(status_code) + " OK\r\n"
        headers += "Date: " + datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT') + "\r\n"
        headers += "Server: Molly's Server\r\n"
        headers += "Content-Length: " + str(content_len) +"\r\n"
        headers += "Connection: close\r\n"
        headers += "Content-Type: text/html; charset=UTF-8\r\n"
        return headers

    def head(self, path, con):
        if path == "/":
            path = "/index.html"
        try:
            with open(path[1:], "rb") as file:
                data = file.read()
                size = len(data)
                con.send(self.default_headers(content_len=size).encode())
        except:
            con.send((self.default_headers(status_code=404) + "Error 404: Not Found").encode())


    def get(self, path, con):
        if path == "/":
            path = "/index.html"
        try:
            with open(path[1:], "rb") as file:
                data = file.read()
                size = len(data)
                con.send(self.default_headers(content_len=size).encode())
                con.send(data)
        except:
            con.send((self.default_headers(status_code=404) + "Error 404: Not Found").encode())
            
    def error(self, con):
        con.send((self.default_headers(status_code=501) + "Error 501: Not Implemented").encode())
        

if __name__ == "__main__":
    """python Server.py PORT DIRECTORY"""
    if len(sys.argv) != 3:
        print("Usage: python Server.py PORT DIRECTORY")
        sys.exit(1)
    else:
        port = int(sys.argv[1])
        directory = sys.argv[2]
        server(port, directory).serve()
