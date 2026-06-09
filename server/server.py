import struct

def enviar_msg(sock, mensagem_texto):
    """Codifica a string, calcula o tamanho e envia o cabeçalho + dados."""
    dados = mensagem_texto.encode('utf-8')
    tamanho = len(dados)
    # '!I' significa: formato de rede (Big-Endian), Inteiro Não-Sinalizado de 4 bytes
    cabecalho = struct.pack('!I', tamanho)
    sock.sendall(cabecalho + dados)

def receber_msg(sock):
    """Lê os 4 bytes do cabeçalho para saber o tamanho exato e depois lê o bloco completo."""
    # Recebe o cabeçalho de 4 bytes
    cabecalho = sock.recv(4)
    if not cabecalho:
        return None
    
    tamanho = struct.unpack('!I', cabecalho)[0]
    
    # Loop para garantir que recebemos TODOS os bytes da mensagem
    dados = b""
    while len(dados) < tamanho:
        pacote = sock.recv(tamanho - len(dados))
        if not pacote:
            return None
        dados += pacote
        
    return dados.decode('utf-8', errors='replace')
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
