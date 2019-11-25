import socket,select
import sys

def prompt(self) :
        sys.stdout.write('<You>: ')
        sys.stdout.flush()
    

if __name__ == "__main__":
     
     
    host = "127.0.0.1"
    port = 5555
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     
    try :
        s.connect((host, port))
    except :
        print '###Unable to connect to specified server(host,port).###'
        sys.exit()
     
    print '##Connected to remote host. Please choose a username:'
    name=raw_input(" ")
    s.send(name)
    sys.stdout.write('<You>:')
    sys.stdout.flush()
     
    while 1:
        socket_list = [sys.stdin, s]
         
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
        for sock in read_sockets:
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print '\n####Disconnected from chat server####'
                    sys.exit()
                else :
                    sys.stdout.write(data)
                    sys.stdout.write('<You>: ')
        	    sys.stdout.flush()
             

            else :
                msg = sys.stdin.readline()
                s.send("<"+name+">"+msg)
		sys.stdout.write('<You>: ')
	        sys.stdout.flush()
