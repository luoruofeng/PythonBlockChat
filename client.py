import threading,socket,sys

class Client(object):

    def recv_message(self,socket):
        while(True):
            data = socket.recv(1024)
            print(data.decode("utf-8"))

    def handle(self, username):
        s = socket.socket()
        s.setblocking
        s.connect(("0.0.0.0", 8492))
        s.send(sys.argv[1].encode("utf-8"))
        # s.setblocking(0)

        recv_thread = threading.Thread(target=self.recv_message, args=[s.dup()])
        recv_thread.start()

        while(True):
            data = input("请输入:")
            s.send(data.encode("utf-8"))

        print("end")

    def __init__(self):
        pass


Client().handle(sys.argv[1])


    
