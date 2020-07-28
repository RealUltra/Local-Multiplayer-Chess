import pickle, password, network

servers = {}
clients = {}

def handle_client(connection, address):
    while 1:
        try:
            message = pickle.loads(connection.recv(4096))

            if message != "":
                print(f"[{address}] {message}")

                if message.startswith("[MOVE]"):
                    for conn in servers[clients[connection]]:
                        if conn != connection:
                            server.send(message, conn)
                            break

                elif message.startswith("[JOIN]"):
                    code = message.replace("[JOIN]", "").strip()

                    if code not in servers:
                        server.send("[JOIN WITH CODE FAILED]", connection)

                    elif len(servers[code]) == 2:
                        server.send("[JOIN WITH CODE FULL]", connection)

                    else:
                        servers[code].append(connection)
                        clients[connection] = code

                        if len(servers[code]) == 2:
                            f = 0
                            for conn in servers[code]:
                                server.send("[STARTED] " + str(f), conn)
                                f += 1

                        else:
                            server.send("[WAITING] " + str(code), connection)

                elif message.strip() == "[JOIN RANDOM]":
                    serverFound = False

                    for s in servers:
                        if len(servers[s]) < 2:
                            serverFound = True
                            servers[s].append(connection)
                            clients[connection] = s

                            if len(servers[s]) == 2:
                                f = 0
                                for conn in servers[s]:
                                    server.send("[STARTED] " + str(f), conn)
                                    f += 1

                            else:
                                server.send("[WAITING] " + str(s), connection)

                            break

                    if not serverFound:
                        code = password.passwordCreator()
                        servers[code] = [connection]
                        clients[connection] = code
                        server.send("[WAITING] " + str(code), connection)

                elif message.strip() == "[LEAVING WAIT]" or message.strip() == "[GAME OVER]":
                    code = clients[connection]

                    if code in servers:
                        servers[code].remove(connection)

                    clients.pop(connection)

                    if message.strip() != "[GAME OVER]":
                        for conn in servers[code]:
                            servers.send("[OPPONENT LEFT]", conn)
                            clients.pop(conn)

                    servers.pop(code)

                elif message.strip() == "[QUIT]":
                    if connection in clients:
                        code = clients[connection]
                        servers[code].remove(connection)
                        clients.pop(connection)

                        for conn in servers[code]:
                            servers.send("[OPPONENT LEFT]", conn)
                            clients.pop(conn)

                        servers.pop(code)

                    server.clients -= 1
                    server.CLIENTS.remove(connection)
                    print(f"\n[CLIENT DISCONNECTED] [{address}] Just Disconnected!")
                    print(f"[ACTIVE CONNECTIONS] {server.clients}\n")
                    break

        except:
            if connection in clients:
                clients.pop(connection)

            for code in servers:
                if connection in servers[code]:
                    servers[code].remove(connection)

                    if servers[code] != []:
                        for conn in servers[code]:
                            server.send("[OPPONENT LEFT]", conn)
                            clients.pop(conn)

                    servers.pop(code)
                    break

            server.clients -= 1
            server.CLIENTS.remove(connection)
            print(f"\n[CLIENT DISCONNECTED] [{address}] Just Disconnected!")
            print(f"[ACTIVE CONNECTIONS] {server.clients}\n")
            break

    connection.close()

server = network.Server(handle_client, 5555)
