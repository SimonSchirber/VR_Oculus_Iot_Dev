# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import asyncio
from kasa import SmartPlug
from urllib import parse

hostName = "localhost"
serverPort = 8080
p = SmartPlug("192.168.10.21")
p2 = SmartPlug("192.168.10.120")

class MyServer(BaseHTTPRequestHandler):
    

    def do_GET(self):
        
        
        self.send_response(200)
        if("/lamp1" in self.path):
            if("ON" in self.path):
                asyncio.run(lamp1(True))
            if("OFF" in self.path):
                asyncio.run(lamp1(False))
        
        if("/lamp2" in self.path):
            if("ON" in self.path):
                asyncio.run(lamp2(True))
            if("OFF" in self.path):
                asyncio.run(lamp2(False))
        
        if("/status" in self.path):
            asyncio.run(p.update())
            asyncio.run(p2.update())
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>IoT Lamp</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes(f"<p>Lamp 1 is ON: {p.is_on}</p>", "utf-8"))
        self.wfile.write(bytes(f"<p>Lamp 2 is ON: {p2.is_on}</p>", "utf-8"))
        self.wfile.write(bytes("<form action=\"/lamp1/ON\" method=\"get\" id=\"lamp1formON\"></form>", "utf-8"))
        self.wfile.write(bytes("<form action=\"/lamp2/ON\" method=\"get\" id=\"lamp2formON\"></form>", "utf-8"))
        self.wfile.write(bytes("<form action=\"/lamp1/OFF\" method=\"get\" id=\"lamp1formOFF\"></form>", "utf-8"))
        self.wfile.write(bytes("<form action=\"/lamp2/OFF\" method=\"get\" id=\"lamp2formOFF\"></form>", "utf-8"))
        self.wfile.write(bytes("<form action=\"/status\" method=\"get\" id=\"status\"></form>", "utf-8"))
        self.wfile.write(bytes("", "utf-8"))
        self.wfile.write(bytes("<button type=\"submit\" form=\"lamp1formON\" value=\"Submit\">Turn On Lamp 1</button>", "utf-8"))
        self.wfile.write(bytes("<button type=\"submit\" form=\"lamp1formOFF\" value=\"Submit\">Turn Off Lamp 1</button>", "utf-8"))
        self.wfile.write(bytes("<button type=\"submit\" form=\"lamp2formON\" value=\"Submit\">Turn On Lamp 2</button>", "utf-8"))
        self.wfile.write(bytes("<button type=\"submit\" form=\"lamp2formOFF\" value=\"Submit\">Turn Off Lamp 2</button>", "utf-8"))
        self.wfile.write(bytes("<button type=\"submit\" form=\"status\" value=\"Submit\">Status</button>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))



async def lamp1(lamp_on):
    if lamp_on:
        await p.turn_on()
    else:
        await p.turn_off()
    await p.update()

async def lamp2(lamp_on):
    if lamp_on:
        await p2.turn_on()
    else:
        await p2.turn_off()
    await p2.update()

def main():
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    ## asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(p.update())
    asyncio.run(p2.update())
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")


if __name__ == "__main__":        
    main()