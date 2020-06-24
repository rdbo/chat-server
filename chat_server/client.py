import socket
import argparse
import threading
import time
import sys

max_bufsize = 1024

def message_handler(conn : socket.socket):
    global max_bufsize
    while(not conn._closed):
        data = conn.recv(max_bufsize)
        if(len(str(data.decode())) > 0):
            print(str(data.decode()))

def usage():
    print("usage")

def run_client(host : str, port : int, username : str):
    delay = 0.4
    max_username = 64
    print("<< chat-server by rdbo >>")
    time.sleep(delay)

    if(len(host) <= 0 or port <= 0 or len(username) <= 0 or len(username) > max_username):
        usage()
        return -1

    print("[*] Initializing client...")
    print(f"[i] Host: {host}")
    print(f"[i] Port: {port}")
    print(f"[i] Username: {username}")

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
    except KeyboardInterrupt:
        print()
        print("[!] Interrupted")
        return -1
    except:
        print("[!] Unable to connect to server")
        return -1

    print("[*] Initialized")
    
    client.send(username.encode())
    threading._start_new_thread(message_handler, (client,))

    while(True):
        try:
            if(client._closed):
                break
            
            msg = input()
            if(len(msg) > 0 and len(msg) < max_bufsize):
                try:
                    client.send(msg.encode())
                except:
                    print("[!] Unable to send message")
                    break
            time.sleep(0.5)
            
        except KeyboardInterrupt:
            print()
            print("[!] Interrupted")
            break
        except:
            print("[!] Exception raised")
            break
    
    client.close()
    

if(__name__ == "__main__"):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h", "--host", type=str, action="store", dest="host", default="")
    parser.add_argument("-p", "--port", type=int, action="store", dest="port", default="4444")
    parser.add_argument("-u", "--username", type=str, action="store", dest="username", default="")
    args = parser.parse_args()

    host = args.host
    port = args.port
    username = args.username
    
    try:
        run_client(host, port, username)
    except KeyboardInterrupt:
        print()
        print("[!] Interrupted")
        exit(-1)
    except:
        print(f"[!] Unhandled exception caught: {sys.exc_info()[0]}")
        exit(-1)