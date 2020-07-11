import socket
import sys
import os
import datetime

HOST = 'localhost' # Address
PORT = 8080 # Port
MAXLISTEN = 100000


def splitData(data):
    start = data.find('username') + 9
    end = start
    _userName = ''
    for i in data[start:]:
        if i == '&':
            break
        _userName += i
        end += 1
    _passWord = data[end + 10:]
    return _userName, _passWord
    
def readFi(filename):
    try:
        file_open = open(filename, 'rb')
        data = file_open.read()
        file_open.close()
        response_code = 200
    except FileNotFoundError:
        print('File Not Found')
        response_code = 404
        data = ""
    return response_code, data

def getFiPath(req_pack):
    filepath = req_pack.split(' ')[1]      
    filepath = filepath[1:]         
    if filepath == '':
        filepath = 'index.html'
    return os.path.join(os.path.dirname(__file__), filepath)

def CrtResp(status, data):
    if status == 200:
        status_code = 'HTTP/1.1 200 OK\r\n'
    elif status == 404:
        status_code = 'HTTP/1.1 404 NOT FOUND\r\n'
    header = 'Connection: close\r\n'
    header += 'Accept: text/html\r\n'
    header += 'Accept-Language: en_US\r\n'
    header += 'Content-Type: text/html\r\n\r\n'
    res_header = status_code + header
    return res_header, data

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Connection configuration
    s.bind((HOST, PORT)) #Listening
    s.listen(MAXLISTEN) # Setup 10 connection at the same time
    print('Server is listening on PORT: ', PORT)
    cur_path = os.path.dirname(__file__)
    while True:
        (client, adr) = s.accept()	 
        currentDT = datetime.datetime.now()
        data = client.recv(2048)
        print('Client connected:', client, ' Time:' ,str(currentDT))
        requests = data.decode()
        req_method = requests.split(' ')[0]     
        res_path = os.path.join(cur_path, 'index.html')     
        (status_code, data) = readFi(res_path)      
        if req_method == 'GET' or req_method == 'POST':
            if req_method == 'POST':
                (userName, passWord) = splitData(requests)
                if userName == 'admin' and passWord == 'admin':
                    res_path = os.path.join(cur_path, 'info.html')
                    currentDT = datetime.datetime.now()
                    print('\nValid Username and password, redirecting.... Time:' ,str(currentDT),'\n')
                else:
                    status_code = 404
                    res_path = os.path.join(cur_path, '404.html')
                    currentDT = datetime.datetime.now()
                    print('\nInvalid Username and password, error.... Time:' ,str(currentDT), '\n')
            elif req_method == 'GET':
                file_path = getFiPath(requests)
                if file_path.find('.html') == -1:
                    res_path = os.path.join(cur_path, file_path)
            file_open = open(res_path, 'rb')
            data = file_open.read()
            (res_header, res_body) = CrtResp(status_code, data)
            client.send(res_header.encode())
            client.send(res_body)
            client.close()
    
main()
