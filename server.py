'''
Created on Oct 23, 2016

@author: sarik
'''
from socket import *
import sys
import threading
import io
import time
from sys import getsizeof

global ssoc

'''Refrence for threading: https://www.tutorialspoint.com/python/python_multithreading.htm'''

class myThread(threading.Thread):
    def __init__(self,threadID,name,ssoc):
        threading.Thread.__init__(self)
        self.thredID=threadID
        self.name=name
        self.ssoc=ssoc
    
    def run(self):
        
        #Accept call from client
        connsoc,addr=self.ssoc.accept()
        start_time=time.time()
        data=connsoc.recv(1024)
        
        '''Reference:http://stackoverflow.com/questions/2757887/file-mode-for-creatingreadingappendingbinary'''
        #Create log file
        global log
        log=open("log.txt","a")
        print("----------------------------------------------------------\n")
        print("           Request from client to proxy server:           \n")
        print("Client Host address: "+str(addr[0])+"\n")
        print("Local port: "+str(addr[1])+"\n")
        print("CLient host name: localhost\n")
        
        log.write("----------------------------------------------------------\n")
        log.write("           Request from client to proxy server:           \n")
        log.write("Client Host address: "+str(addr[0])+"\n")
        log.write("Local port: "+str(addr[1])+"\n")
        log.write("CLient host name: localhost\n")
        
        '''Reference for request format: https://www.w3.org/Protocols/rfc2616/rfc2616-sec5.html'''
        try:
            request=data.decode().split('\n')[0]
        except:
            print("----------------------------------------------------------\n")
            log.write("----------------------------------------------------------\n")
            print("Received blank data")
            log.write("Received blank data\n")
            print("Make new request")
            create_thread(self.ssoc)
            
        print("Request: "+request+"\n")
        '''Refrence: http://stackoverflow.com/questions/449560/how-do-i-determine-the-size-of-an-object-in-python'''
        print("Request length: "+str(getsizeof(data))+" bytes\n")    
        log.write("Request: "+request+"\n")
        log.write("Request length: "+str(getsizeof(data))+" bytes\n")
        
        #parsing data to get url
        fl=data.decode().split('\n')[0]
        try:
            url=fl.split(' ')[1]
            #print("URL: ",url)
            url=url.split('//')[1]
            url=url.split('/')[0]
            
        except: 
            print("----------------------------------------------------------\n")
            log.write("----------------------------------------------------------\n")
            connsoc.send(b"ERROR 403 FORBIDDEN")
            print("ERROR 403 FORBIDDEN") #incase not a GET request
            log.write("ERROR 403 FORBIDDEN\n")
            connsoc.close()
            print("Closed client connection\n")
            log.write("Closed client connection\n")
            print("Make new request")
            create_thread(self.ssoc) #to keep serversoc monitoring for new requests
        
        print("----------------------------------------------------------\n")
        print("                         Socket Details                   \n")
        log.write("----------------------------------------------------------\n")
        log.write("                         Socket Details                   \n")
        
        '''Reference: https://docs.python.org/3.3/library/socket.html'''
        try:
            socfam=str(getaddrinfo(url, 80)).split(',')[0] #parse socket family
        except:
            print("----------------------------------------------------------\n")
            log.write("----------------------------------------------------------\n")
            connsoc.send(b"ERROR 400 BAD REQUEST")
            print("ERROR 400 BAD REQUEST\n")
            log.write("ERROR 400 BAD REQUEST\n")
            connsoc.close()
            print("Make new request")
            create_thread(self.ssoc)
            return
        socfam=socfam.split(":")[1]
        socfam=socfam.split(">")[0]
        print("Socket family: "+str(socfam)+"\n")
        log.write("Socket family: "+str(socfam)+"\n")
        
        #parse socket type
        soctype=str(getaddrinfo(url, 80)).split(',')[1]
        print("Socket type: "+str(soctype)+"\n")
        log.write("Socket type: "+str(soctype)+"\n")
        
        #parse socket protocol
        socprot=str(getaddrinfo(url, 80)).split(',')[2]
        print("Socket protocol: "+str(socprot)+"\n")
        log.write("Socket protocol: "+str(socprot)+"\n")
        
        #cache the response for new request
        cache(data,url,connsoc,self.ssoc,start_time)
        create_thread(self.ssoc) #to keep serversoc monitoring for new requests

        

def start_server():

    #create a socket
    ssoc=socket(AF_INET,SOCK_STREAM)
    
    #associate socket with a port
    shost=''
    sport=8080
    
    #Initialize and bind socket
    ssoc.bind((shost,sport))
    ssoc.listen(5)
    
    create_thread(ssoc)#to keep serversoc monitoring for new requests
    
def create_thread(ssoc):
    
    #if receive new request from client then create a thread   
    if(ssoc.accept()):
        #print("NEw Request")
        thread1=myThread(1,"Thread-new",ssoc)
        thread1.start()
        


    
def cache(data,url,connsoc,ssoc,start_time):
    
    try:
        cachedresp=b""
        filename=url.replace(".","")
        '''Reference:https://www.tutorialspoint.com/python/python_date_time.htm'''
        start_time_cache=time.time()
        '''Reference:http://stackoverflow.com/questions/1035340/reading-binary-file-in-python-and-looping-over-each-byte'''
        f1=open(filename,"rb")
        print("----------------------------------------------------------\n")
        print("                      Cache Hit Occured                   \n")
        log.write("----------------------------------------------------------\n")
        log.write("                      Cache Hit Occured                   \n")
        for i in f1:
            cachedresp+=i
            
        print("Response length: "+str(getsizeof(cachedresp))+"\n")
        log.write("Response length: "+str(getsizeof(cachedresp))+"\n")
        connsoc.send(cachedresp)
        end_time_cache=time.time()
        print("RTT is:"+ str(end_time_cache-start_time_cache)+"\n")
        log.write("RTT is:"+ str(end_time_cache-start_time_cache)+"\n")
        print("Make new request")
        return
        
    except IOError:
        print("----------------------------------------------------------\n")
        print("                    Cache Miss Occured                    \n")
        print("Request from web proxy server to server\n")
        log.write("----------------------------------------------------------\n")
        log.write("                    Cache Miss Occured                    \n")
        log.write("Request from web proxy server to server\n")
        filename=url.replace(".","")  #filename to cache response
        f2=open(filename,"wb")
        proxysoc=socket(AF_INET,SOCK_STREAM) #socket between proxy server and web server
        try:
            proxysoc.connect((url,80))
        except:
            print("----------------------------------------------------------\n")
            log.write("----------------------------------------------------------\n")
            connsoc.send(b"ERROR 404 NOT FOUND")
            print("ERROR 404 NOT FOUND\n")
            log.write("ERROR 404 NOT FOUND\n")
            connsoc.close()
            proxysoc.close()
            print("Make new request")
            create_thread(ssoc)#to keep serversoc monitoring for new requests
            
        '''reference: https://recalll.co/app/?q=python%20-%20Use%20HTTP/1.1%20with%20SimpleHTTPRequestHandler'''    
        req="GET / HTTP/1.1\nHost: " + url + "\n\n"
        print("Request: "+req+"\n")
        print("Request length: "+str(len(req))+" bytes\n")
        log.write("Request: "+req+"\n")
        log.write("Request length: "+str(len(req))+" bytes\n")
        try:
            proxysoc.send(req.encode())
        except:
            print("----------------------------------------------------------\n")
            log.write("----------------------------------------------------------\n")
            connsoc.send(b"ERROR 404 NOT FOUND")
            print("ERROR 404 NOT FOUND\n")
            log.write("ERROR 404 NOT FOUND\n")
            connsoc.close()
            proxysoc.close()
            print("Make new request")
            create_thread(ssoc)#to keep serversoc monitoring for new requests
        res=proxysoc.recv(1024) #receive response from web server
        fresp=res #fresp will contain the final complete response to be cached. Initializing fresp to res
        connsoc.send(res)
        #continue receiving the response
        while(len(res)!=0):
            try:
                res=proxysoc.recv(1024) #receive response from web server
            except:
                print("----------------------------------------------------------\n")
                log.write("----------------------------------------------------------\n")
                connsoc.send(b"Error 403 Forbidden")
                print("Error 403 Forbidden\n")
                log.write("Error 403 Forbidden\n")
                print("Make new request")
                connsoc.close()
                proxysoc.close()
                print("Make new request")
                create_thread(ssoc)#to keep serversoc monitoring for new requests
            connsoc.send(res) #send response to client
            fresp+=res
        print("Response length: "+str(getsizeof(fresp))+" bytes\n")
        log.write("Response length: "+str(getsizeof(fresp))+" bytes\n")
        end_time=time.time()
        print("Time Elapse i.e. RTT: "+str(end_time-start_time)+"\n")
        log.write("Time Elapse i.e. RTT: "+str(end_time-start_time)+"\n")
        f2.write(fresp)
        print("Cached response")
        connsoc.close()
        proxysoc.close()
        print("Connection closed\n")
        log.write("Connection closed\n")
        print("Make new request")
        return
        

class WebProxy:
            
    start_server() 


