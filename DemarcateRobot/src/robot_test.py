#!/usr/bin/env python
import time
import socket
host="192.168.1.100"
port=10011
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((host,port))
s.listen(10000)

print 'listen'
i=0
t_last = time.time()
sum_t = 0
ddo='HTTP/1.1 200 OK\r\n\
Content-type:text/html\r\n\
Content-Length:%d\r\n\r\n'
strt='{"robot_id":"0900","robot_state":{"process":"1","step":"1"},\
"message":{"process_state":{"process":"1",\
"step":{"step_name":"a,b,c,d,e", "step_state":"0,0,0,0,0" } } },\
"state":"success"}'
content = ddo%len(strt)
content += strt
dd1='HTTP/1.1 200 OK\r\nContent-type:text/html\r\n\r\n{"robot_id":"0900","robot_state":{"process":"1","step":"1"},\
"message":{"process_state":{"process":"1",\
"step":{"step_name":"a,b,c,d,e", "step_state":"1,1,1,1,1" } } },\
"state":"success"}'
dd2='HTTP/1.1 200 OK\nContent-type:text/html\r\n\r\n{"robot_id":"0900","robot_state":{"process":"1","step":"1"},\
"message":{"process_state":{"process":"1",\
"step":{"step_name":"a,b,c,d,e", "step_state":"0,0,0,0,0" } } },\
"state":"success"}'
import base64
while 1:
    i+=1
    print i
    t=time.time()
    d = t - t_last
    sum_t += d
    av = sum_t/i
    t_last = t
    #print d
    if not i%10:
        print av
    sock,addr=s.accept()
    #print "got connection form ",sock.getpeername()
    data=sock.recv(1024)
    import urllib
    print urllib.unquote(data)
    if not i%2:        
        sock.sendall(dd1)
    else:
        sock.sendall(dd2)
    
    sock.close()

    #sock.send(data)
    #time.sleep(1)
