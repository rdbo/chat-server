import socket
import argparse
import time
import threading

conn_list = []

def usage():
    print("usage")

def connection_handler(server : socket.socket, conn : socket.socket, addr):
    global conn_list
    max_bufsize = 1024
    max_username = 64
    conn.send("Welcome to the server".encode())
    username = ""

    while(not server._closed and not conn._closed):
        try:
            data = conn.recv(max_bufsize)
            msg = str(data.decode())
            if(len(msg) > 0):
                if(username == ""):
                    username = msg[0:max_username]
                else:
                    print(f"{username}@{addr[0]} > {msg}")
                    for c in conn_list:
                        if(c != conn and c != server):
                            c.send(msg.encode())

        except:
            if(not conn._closed):
                print(f"[*] {addr[0]} disconnected")
                conn.close()
    print(f"[!] Connection from {addr[0]} closed")
    conn.close()


def run_server(host : str, port : int, output : str):
    global conn_list
    max_connections = 10
    delay = 0.4

    print("<< chat-server by rdbo >>")
    time.sleep(delay)

    if(len(host) <= 0 or port <= 0):
        usage()
        return -1

    print("[*] Initializing server...")
    print(f"[i] Host: {host}")
    print(f"[i] Port: {port}")
    if(len(output) > 0):
        print(f"[i] Logs: {output}")

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(max_connections)
        conn_list.append(server)
    except KeyboardInterrupt:
        print()
        print("[!] Interrupted")
        return -1
    except:
        print("[!] Unable to initialize server")
        return -1
    
    print("[*] Initialized")

    while(True):
        try:
            conn, addr = server.accept()
            if(conn not in conn_list):
                print(f"[*] Connection from: {addr[0]}")
                threading._start_new_thread(connection_handler, (server, conn, addr))
        except KeyboardInterrupt:
            print()
            print("[!] Interrupted")
            break
        except:
            print("[!] Exception raised")
            break

    server.close()
    return 0

    

if(__name__ == "__main__"):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h", "--host", type=str, action="store", dest="host", default="127.0.0.1")
    parser.add_argument("-p", "--port", type=int, action="store", dest="port", default="4444")
    parser.add_argument("-o", "--output", type=str, action="store", dest="output", default="")
    args = parser.parse_args()

    host = args.host
    port = args.port
    output = args.output
    
    try:
        run_server(host, port, output)
    except KeyboardInterrupt:
        print()
        print("[!] Interrupted")
        exit(-1)
    except:
        print("[!] Unhandled exception caught")
        exit(-1)