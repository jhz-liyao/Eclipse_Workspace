import socket 
import time

camera_connect = {}

def establish_camera_connect(name,IP,PORT):
    try:        
        ADDR = (IP, PORT)  
        camera_connect[name] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       

        camera_connect[name].settimeout(3)        
        camera_connect[name].connect(ADDR)
        return 2,camera_connect[name]
    except :
        print 'establish_camera_connect:error'        
        return 3,{}
    
         

