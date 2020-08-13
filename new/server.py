import pickle
import socket
import password
import network
import board

servers = {}
clients = {}

def handle_client(connection, address):
    data = b''
    while 1:
        try:
            while 1:
                packet = connection.recv(4096)
                data += packet
                try:
                    message = pickle.loads(data)
                    data = b''
                    break
                except:
                    pass

            if message != "":
                print(f"[{address}]",  message)

                if message[0] == 'BOARD':
                    for conn in servers[clients[connection]]:
                        if conn != connection:
                            server.send(message, conn)
                            print(f"[SERVER][{conn.getpeername()}]", message, "\n")
                            break

                elif message[0] == 'MODS':
                    code = clients[connection]
                    b = board.Board(mods=message[1])
                    for conn in servers[code]:
                        server.send(["BOARD", b], conn)
                        print(f"[SERVER][{conn.getpeername()}]", ['BOARD', b], "\n")

                elif message[0] == "JOIN":
                    code = message[1]

                    if code not in servers:
                        server.send(["JOIN WITH CODE FAILED"], connection)
                        print(f"[SERVER][{address}]", ["JOIN WITH CODE FAILED"], "\n")

                    elif len(servers[code]) == 2:
                        server.send(["JOIN WITH CODE FULL"], connection)
                        print(f"[SERVER][{address}]", ["JOIN WITH CODE FULL"], "\n")

                    else:
                        servers[code].append(connection)
                        clients[connection] = code

                        if len(servers[code]) == 2:
                            f = 0
                            for conn in servers[code]:
                                server.send(["STARTED", f], conn)
                                print(f"[SERVER][{conn.getpeername()}]", ['STARTED', f], "\n")
                                print(f"[SERVER] Number Of Games: {len(servers)}\n")
                                f += 1

                        else:
                            server.send(["WAITING", code], connection)
                            print(f"[SERVER][{address}]", ['WAITING', code], "\n")

                elif message[0] == "JOIN RANDOM" and connection not in clients:
                    serverFound = False

                    for s in servers:
                        if len(servers[s]) < 2:
                            serverFound = True
                            servers[s].append(connection)
                            clients[connection] = s

                            if len(servers[s]) == 2:
                                f = 0
                                for conn in servers[s]:
                                    server.send(['STARTED', f], conn)
                                    print(f"[SERVER][{conn.getpeername()}]", ['STARTED', f], "\n")
                                    print(f"[SERVER] Number Of Games: {len(servers)}\n")
                                    f += 1

                            else:
                                server.send(["WAITING", s], connection)
                                print(f"[SERVER][{address}]", ['WAITING', s], "\n")

                            break

                    if not serverFound:
                        code = password.passwordCreator()
                        servers[code] = [connection]
                        clients[connection] = code
                        server.send(["WAITING", code], connection)
                        print(f"[SERVER][{address}]", ['WAITING', code], "\n")

                elif message[0] == "LEAVING WAIT" or message[0] == "GAME OVER":
                    code = clients[connection]

                    if code in servers:
                        servers[code].remove(connection)

                    clients.pop(connection)

                    if message[0] != "GAME OVER":
                        for conn in servers[code]:
                            server.send(["OPPONENT LEFT"], conn)
                            print(f"[SERVER][{conn.getpeername()}]", ['OPPONENT LEFT'], "\n")
                            print(f"[SERVER] Number Of Games: {len(servers)}\n")
                            clients.pop(conn)

                    if code in servers:
                      servers.pop(code)

                elif message[0] == "QUIT":
                    if connection in clients:
                        code = clients[connection]
                        servers[code].remove(connection)
                        clients.pop(connection)

                        for conn in servers[code]:
                            server.send(["OPPONENT LEFT"], conn)
                            print(f"[SERVER][{conn.getpeername()}]", ["OPPONENT LEFT"], "\n")
                            clients.pop(conn)

                        servers.pop(code)

                    server.clients -= 1
                    server.CLIENTS.remove(connection)
                    print(f"\n[CLIENT DISCONNECTED] [{address}] Just Disconnected!")
                    print(f"[ACTIVE CONNECTIONS] {server.clients}\n")
                    break

        except Exception as e:
            print('Error:', e)
            if connection in clients:
                code = clients[connection]
                servers[code].remove(connection)
                clients.pop(connection)

                for conn in servers[code]:
                    server.send(["OPPONENT LEFT"], conn)
                    print(f"[SERVER][{conn.getpeername()}]", ['OPPONENT LEFT'], "\n")
                    clients.pop(conn)

                servers.pop(code)

            server.clients -= 1
            server.CLIENTS.remove(connection)
            print(f"\n[CLIENT DISCONNECTED] [{address}] Just Disconnected!")
            print(f"[ACTIVE CONNECTIONS] {server.clients}\n")
            break

    connection.close()

print('\n')
server = network.Server(handle_client, 5555, socket.gethostbyname(''))
