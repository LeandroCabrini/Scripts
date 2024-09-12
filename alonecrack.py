import crypt,sys

#Verifica se foi passado wordlist como argumento
if(len(sys.argv) < 2):
        print("Modo de uso: python alonecrack.py /caminho/para/wordlist")
        sys.exit(1)

#Obtém caminho do arquivo wordlist
wordlist = sys.argv[1]

#Pergunta ao usuário qual o hash que ele deseja quebrar
hash = input("HASH= ")

#Pergunta o salt para o usuário
salt = input("SALT = ")

#Abre o arquivo em modo leitura
with open(wordlist, 'r') as wd:
        #intere sobre cada linha da wordlist
        for linha in wd:
                senha = linha.strip()
                #Encripita senha com base no salt passado 
                hashes = crypt.crypt(senha,salt)
                if(hash == hashes):
                        print("Senha encontrada: " + senha)
                        break
