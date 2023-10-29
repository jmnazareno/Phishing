import http.server
import socketserver
import sqlite3
from urllib.parse import urlparse

def get_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

def scan_url(url):
    # Your scanning logic goes here
    # Replace this example logic with your actual URL scanning code
    domain = get_domain(url)
    if "example" in domain:
        return "Phishing"
    else:
        return "Safe"

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("index.html", "rb") as file:
                self.wfile.write(file.read())
        else:
            super(MyHandler, self).do_GET()

    def do_POST(self):
        if self.path == '/scan':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode("utf-8")
            url = post_data.split('=')[1]
            result = scan_url(url)
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(result.encode())

with socketserver.TCPServer(("", 8080), MyHandler) as httpd:
    print("URL Scanner is running at http://localhost:8080/")
    httpd.serve_forever()
