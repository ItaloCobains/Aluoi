import threading
import socketserver
import time
import platform
import os
import subprocess
import sys

from subprocess import Popen
from dotenv import load_dotenv, find_dotenv


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def getOs(self) -> str:
       system = platform.system()
       rel = platform.release()
       name = os.name
       return "{}, {}, {}".format(system, rel, name)

    def cmd(self, data) :
        if (data[0] == 'os'):
            res: str = self.getOs()
            return res
        if (data[0] == 'cmd'):
            del data[0]
            p = Popen(data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, erros = p.communicate()
            if (output):
                p.kill()
                return output
            if (erros):
                p.kill()
                return erros
            p.kill()
            return 0

                
    
    def handle(self):
        data = str(self.request.recv(1024), 'ascii') # dado que vem na requisição
        data = data.split()
        data = self.cmd(data)
        cur_thread = threading.current_thread()
        response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
        self.request.sendall(response)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":

    load_dotenv(find_dotenv())

    HOST = str(os.getenv('HOST'))
    PORT = int(os.getenv('PORT'))

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    with server:
        ip, port = server.server_address

        server_thread = threading.Thread(target=server.serve_forever)

        server_thread.daemon = True

        server_thread.start()
        print("Server loop running in thread", server_thread.name)


        time.sleep(5000)

        server.shutdown()
