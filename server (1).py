import socket,os,datetime
from socket import *
from datetime import datetime, timezone
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

def get_current_date():
    """
    Returns the current date and time in UTC formatted as:
    "Day, DD Mon YYYY HH:MM:SS GMT"
    """
    return datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")

def construct_headers(status, content_length, last_modified=None):
    headers = [
        f"HTTP/1.1 {status}",
        f"Date: {get_current_date()}",
        "Connection: keep-alive",
        "Server: Tom's Server",
        f"Content-Length: {content_length}"
    ]
    if last_modified:
        headers.append(f"Last-Modified: {last_modified}")
    headers.append("\r\n")  # End of headers
    return "\r\n".join(headers)

def constructResponse(method,version,request,filename):
    if(method == "GET"):
        try:
            filetime = os.path.getmtime(filename)
            timeObj = datetime.fromtimestamp(filetime, tz=timezone.utc)
            timeObj = timeObj.strftime("%a, %d %b %Y %H:%M:%S GMT")
            file_size = os.path.getsize(filename)

            # Check for If-Modified-Since header
            for line in request.split("\n"):
                if("If-Modified-Since:" in line):
                    ims = line.split(":",1)[1].strip()#value for the If-Modified-Since request header
                    if timeObj == ims: #If file hasn't been modified
                        response = construct_headers("304 Not Modified", 0)
                        connectionSocket.send(response.encode())
                        return response
        
            # If no If-Modified-Since header or file has been modified
            response = construct_headers("200 OK", file_size, timeObj)
            connectionSocket.send(response.encode())

            with open(filename, "rb") as file:
                while chunk := file.read(1024):
                    connectionSocket.send(chunk)

            return response
        
        except FileNotFoundError:
            response = construct_headers("404 Not Found", 0)
            connectionSocket.send(response.encode())
            return response
        
    elif (method == "HEAD"):
        try:
            filetime = os.path.getmtime(filename)
            timeObj = datetime.fromtimestamp(filetime, tz=timezone.utc)
            timeObj = timeObj.strftime("%a, %d %b %Y %H:%M:%S GMT")
            file_size = os.path.getsize(filename)

            # Check for If-Modified-Since header
            for line in request.split("\n"):
                if("If-Modified-Since:" in line): 
                    ims = line.split(":",1)[1].strip()#value for the If-Modified-Since request header
                    if timeObj == ims: #If file hasn't been modified
                        response = construct_headers("304 Not Modified", 0)
                        connectionSocket.send(response.encode())
                        return response
        
            # If no If-Modified-Since header or file has been modified
            response = construct_headers("200 OK", file_size, timeObj)
            connectionSocket.send(response.encode())
            return response
        
        except FileNotFoundError:
            response = construct_headers("404 Not Found", 0)
            connectionSocket.send(response.encode())
            return response
    else:
        response = construct_headers("501 Not Implemented",0)
        connectionSocket.send(response.encode())
        return response
    
while(True):

    connectionSocket, addr = serverSocket.accept()
    request = connectionSocket.recv(1024).decode()

    method = request.split(" ")[0]
    filename = request.split(" ")[1].strip("/")
    version = request.split(" ")[2]
    response = constructResponse(method,version,request,filename)
    print(response)
    connectionSocket.close()
