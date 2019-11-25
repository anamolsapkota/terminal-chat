import socket,select
import threading

s=threading.Semaphore()

class ThreadedServer():
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 5555
        self.connections=[]
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.connections.append(self.sock)

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            self.connections.append(client)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        size = 1024
        global s
        data=client.recv(1024)
        self.broadcast(client,data+" just entered the chatroom \n")
        client.send("Start Chatting.. \n")
        while True:
            self.read_sockets,write_sockets,error_sockets = select.select(self.connections,[],[])
            for sock in self.read_sockets:
                try:
                    data = sock.recv(4096)
                    if data:
                        self.broadcast(sock, "\r" + data)
                except:
                    self.broadcast(sock, data+" is offline \n")
                    print (data+" is offline \n")
                    continue
            
    def broadcast(self,ssocket,msg):
        for clients in self.connections:
            if clients!=ssocket and clients!=self.sock:
                try:
                    clients.send(msg)
                except:
                    clients.close()
                    self.connections.remove(clients)
                
if __name__ == "__main__":
    ThreadedServer().listen()
