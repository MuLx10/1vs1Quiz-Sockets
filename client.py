import socket
import sys
# import StringIO


class Client:
    def __init__(self, ip_addr = "127.0.0.1",port = 6262):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((ip_addr, port))
        # self.data = StringIO.StringIO()
    def parse(self,data):
        data = data.replace(":s:","").replace(":e:","")
        data = data.split(":")
        print data[0]+'\r'
        print "a. "+data[1],"b. "+data[2]
        print "c. "+data[3],"d. "+data[4]

    def parse_result(self,data):
        # print data
        data = data.replace(":res:","")
        data = data.split("|")
        print "\nYour Score : "+data[0]+" Your opponent score : "+data[1]
        print data[2]

    def connect(self,port):
        data = ''
        change = ''
        while True:
            data = self.client_socket.recv(8096)
            if ":res:" in data:
                self.parse_result(data)
                break
            if ":s:" in data and ":e:" in data:
                if 'y' in change:
                    self.parse(data)
                    response = raw_input('\nResponse : ')
                    self.client_socket.send(response)
                    change = ''
                else:
                    change = raw_input('\nChange  (y/n) : ')
                    print

                if 'y' in change:
                    self.client_socket.send("x")
                else:
	                self.parse(data)
	                response = raw_input('\nResponse : ')
	                self.client_socket.send(response)
                

if __name__ == "__main__":
    ip_addr = "127.0.0.1"
    port = 6000
    if len(sys.argv)> 2:
        ip_addr = sys.argv[1]
        port = int(sys.argv[2])

    print "Connecting to " + ip_addr + "...."+str(port)+'.....'
    client = Client(ip_addr,port)
    client.connect(port)
