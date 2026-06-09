import socket

def iniciar_servidor(host='0.0.0.0', port=5003):
    # Cria o socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Permite reutilizar a porta imediatamente caso o script reinicie
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"[*] Aguardando conexões na porta {port}...")

    conn, addr = server_socket.accept()
    print(f"[+] Conexão estabelecida com {addr[0]}:{addr[1]}")

    while True:
        comando = input("Shell> ")
        
        if comando.lower() in ['exit', 'quit']:
            conn.send(comando.encode('utf-8'))
            conn.close()
            break
        
        if comando.strip() == "":
            continue

        # Envia o comando para o cliente
        conn.send(comando.encode('utf-8'))
        
        # Recebe a resposta (buffer de 4096 bytes para fluidez)
        resposta = conn.recv(4096).decode('utf-8')
        print(resposta, end="")

if __name__ == "__main__":
    iniciar_servidor()