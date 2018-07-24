import socket,threading,select,os,random,pickle

UNCONNECT = "未链接"
CONNECT = "链接"

friends = {"a":"b","b":"a","c":"d","d":"c"}
class User(object):
    def __init__(self,ip_port,name,status,client_socket):
        self.ip_port = ip_port
        self.name = name
        self.status = status
        self.client_socket = client_socket

    def __eq__(self,other):
        return other.name == self.name


class UserManager(object):
    users_online = []

    def get_friends(self,current_user_name):
        for user in self.users_online:
            if(user.name == friends[current_user_name]):
                return user
        return None
    
    def get_socket(self,qq):
        for socket_u in self.users_online:
            if(socket_u.client_socket ==qq):
                return socket_u
        return None

    def login(self, address,user_name,socket):
        online_users=User(ip_port=address[0]+":"+str(address[1]), status=CONNECT,name = user_name,client_socket = socket)
        self.users_online.append(online_users)
        return online_users

    def is_online(self,current_user):
        for user in users_online:
            if(user == current_user):
                return True
        return False


user_manager_instance = UserManager()
sockets=[]

class Server(object):

    def manage_user_connection(self):

        s = socket.socket()
        s.bind(("0.0.0.0", 8493))
        s.listen(11)

        while True:
            user_socket, address = s.accept()
            user_name = None
            user_name = user_socket.recv(1024)
            if(user_name):
                print(user_name)
                

            if(user_name):
                current_user = user_manager_instance.login(address, user_name.decode("utf-8"), user_socket)
            else:
                pass
            
            message_transport = threading.Thread(target=self.recv_message, args=[user_socket, address, current_user])
            message_transport.start()
            print("main")
        a=raw_input()
        print('end')
            
    def recv_message(self, socket, address,current_user):
        sockets.append(socket)
        while True:
            message = None
            message = socket.recv(1024)
            if(message):
                print(message)
                if message.decode("utf-8")=="exit":
                    socket.close()
                    us_socket = user_manager_instance.get_socket(socket)
                    user_manager_instance.users_online.remove(us_socket)
                    print("----------------用户退出")
                    for i in sockets:
                        print(i)
                    return


            friend = user_manager_instance.get_friends(current_user.name)
            if(friend):
                friend.client_socket.send(message)
            else:
                socket.send("你的朋友不在".encode("utf-8"))
            

Server().manage_user_connection()
