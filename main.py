import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        cards = [
            {'title': 'Service 1', 'description': 'This is service 1'},
            {'title': 'Service 2', 'description': 'This is service 2'},
            {'title': 'Service 3', 'description': 'This is service 3'}
        ]
        html = '''
        <html>
            <head>
                <title>Services</title>
                <style>
                    .card {
                        width: 200px;
                        height: 200px;
                        border: 1px solid black;
                        margin: 10px;
                        padding: 10px;
                        display: inline-block;
                    }
                </style>
            </head>
            <body>
                <h1>Services</h1>
                '''
        for card in cards:
            html += '''
                <div class="card">
                    <h2>{}</h2>
                    <p>{}</p>
                </div>
                '''.format(card['title'], card['description'])
        html += '''
            </body>
        </html>
        '''
        self.wfile.write(html.encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = parse_qs(body.decode())
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'message': 'Received POST request'}).encode())

port = int(os.environ.get('PORT', 8080))
server_address = ('', port)
httpd = HTTPServer(server_address, RequestHandler)
print('Starting httpd on port %d...' % port)
httpd.serve_forever()