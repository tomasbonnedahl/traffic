from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 8080

class TrafficHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        if self.path == '/':
            self.path = 'index.html'
        if self.path.endswith('.js') or self.path.endswith('.txt'):
            self.path = self.path[1:]

        if not self.path.endswith('.ico'):
            with open(self.path) as f:
                self.wfile.write(f.read())

def startHTTPServer():
    ''' Creates HTTPServer instance and starts listening '''
    httpd = HTTPServer((SERVER_ADDRESS, SERVER_PORT), TrafficHTTPRequestHandler)

    print "Serving at port: {}".format(SERVER_PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print "Ctrl+C received, shutting down"
        httpd.shutdown()

startHTTPServer()