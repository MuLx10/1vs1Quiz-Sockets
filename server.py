import socket
import sys
import thread
from question import Question
class Server:
    def __init__(self,host,port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.score = {}
        self.quiz_over = False
        self.quiz_over_n = 0
        self.MAX_SCORE = 3
        self.ques_n = 3
        self.res = {}
        # self.data = ''
        print "TCP AServer Waiting for client on port "+str(port)

    def socket_handler(self,client_socket,address):
        flag = True
        response_n = 0
        string = "abcd"
        ans = []
        self.score[address] = 0
        self.ques = Question('questions/question.psv')
        # data = ":s:gfguygvhg:vbh:hgh:bbh:bhb:e:|1"
        while True:

            data = self.ques.next_question()
            print data,address

            d_ = data.split('|')

            client_socket.send(d_[0]) 

            response = client_socket.recv(1024)

            # print response
            if response in string:
                if response == string[int(d_[1])]:
                    self.score[address] += 1
                response_n += 1
            
            # print response_n,self.score[address],response,string

            keys = self.score.keys()
            keys.remove(address)
            sc1 = self.score[address]
            sc2 = self.score[keys[0]]            

            if len(self.res)>1:
                result = ":res:"+str(self.res[address])+"|"+str(self.res[keys[0]])+'|You Lose'
                client_socket.send(result)
                break

            elif sc1 == self.MAX_SCORE:
                result = ":res:"+str(self.score[address])+"|"+str(self.score[keys[0]])+'|You Win'
                self.quiz_over = True
                self.res[address] = sc1
                self.res[keys[0]] = sc2
                client_socket.send(result)
                break

            elif response_n >= self.ques_n and flag:
                self.quiz_over_n += 1
                flag = False
                if self.quiz_over_n == 1:
                    while self.quiz_over_n<2:
                        pass

            sc1 = self.score[address]
            sc2 = self.score[keys[0]]
            if self.quiz_over_n>1:
                print (self.score[address],self.score[keys[0]],address,sc1,sc2)
                if sc2>sc1:
                    self.result = ":res:"+str(self.score[address])+"|"+str(self.score[keys[0]])+'|You Lose'
                if sc1>sc2:
                    self.result = ":res:"+str(self.score[address])+"|"+str(self.score[keys[0]])+'|You Win'
                else:
                    self.result = ":res:"+str(self.score[address])+"|"+str(self.score[keys[0]])+'|Draw'

                temp = map(int,self.result.replace(":res:","").split("|")[:-1])

                if temp[0]>temp[1]:
                    self.result = ":res:"+str(temp[0])+"|"+str(temp[1])+'|You Win'                
                if temp[0]<temp[1]:
                    self.result = ":res:"+str(temp[0])+"|"+str(temp[1])+'|You Lose'



                client_socket.send(self.result)
                break
                
        
    def start(self,port):
        
        print "Starting  Server  : "+str(port)
        index = -1
        while 1:
            if index%2 == 0 and index:
                self.score.clear()
                self.res.clear()
                self.quiz_over_n = 0
                self.quiz_over = False
            # print index
            client_socket, address = self.server_socket.accept()
            
            print "I got a connection from ", address,index
            thread.start_new_thread(self.socket_handler, (client_socket,address,))
            index += 1
            # print index

if __name__ == "__main__":
    ip_addr = "127.0.0.1"
    port = 6000
    if len(sys.argv) > 2:
        ip_addr = sys.argv[1]
        port = int(sys.argv[2])


    server = Server(ip_addr,port)
    server.start(port)
