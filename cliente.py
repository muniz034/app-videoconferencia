import socket
import threading

class NO_Cliente:
    def __init__(self, IP, porta, nome):
        self.IP = IP
        self.portas = []
        self.add_porta(porta)
        self.nome = nome
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(180.0)
        #self.socket.listen()
        self.conexoes = []
        self.servidor = None
    
    def add_porta(self, porta):
        self.portas.append(porta)
        print(f'Porta {porta} adicionada com sucesso!')  
        
    def remover_porta(self, porta):
        self.portas.remove(porta)
        print(f'Porta {porta} removida com sucesso!')         
    
    def conectar_servidor(self, servidor_IP, servidor_porta):
        try:
            conexao = self.socket.dup()
            conexao.bind((self.IP, self.portas.pop()))
            conexao.connect((servidor_IP, servidor_porta))
            self.servidor =  conexao
            print(f'Conexão bem-sucedida com IP: {servidor_IP} | porta: {servidor_porta}')
        except socket.error as e:
            print(f'Conexão mal-sucedida com IP: {servidor_IP} | porta: {servidor_porta}')
            print(f'Erro encontrado: {e}')
        except IndexError as e:
            print(f'Conexão mal-sucedida com IP: {servidor_IP} | porta: {servidor_porta}')
            print(f'Erro encontrado: Nenhuma porta disponível')
            
    def conectar_cliente(self, NO_IP, NO_porta):
        try:
            conexao = self.socket.dup()
            conexao.bind((self.IP, self.portas.pop()))
            conexao.connect((NO_IP, NO_porta))
            self.conexoes.append(conexao)
            print(f'Conexão bem-sucedida com IP: {NO_IP} | porta: {NO_porta}')
        except socket.error as e:
            print(f'Conexão mal-sucedida com IP: {NO_IP} | porta: {NO_porta}')
            print(f'Erro encontrado: {e}')
        except IndexError as e:
            print(f'Conexão mal-sucedida com IP: {NO_IP} | porta: {NO_porta}')
            print(f'Erro encontrado: Nenhuma porta disponível')
     
    #fecha 1 socket de cliente       
    def desconectar_cliente(self, nome):
        if(self.servidor == None):
            #recebe IP e porta como parâmetro,talvez vire uma função diferente
            x = 0
            while(x < self.conexoes.__len__()):
                conexao = self.conexoes[x]
                if(conexao.getpeername[0] == IP):
                     y = 0
                     while(y < porta.__len__()):
                         if(conexao.getpeername()[1] == porta[y]):
                             conexao.shutdown(socket.SHUT_RDWR)
                             conexao.close()
                             self.add_porta(conexao.getsockname()[1])
                         y += 1
        else:
            #pergunta para o server passando o nome do cliente em questão e retorna as portas e IP da conexão
            msg = f'Desejo os dados do cliente {nome}'
            self.enviar_msg(msg,self.servidor)
            resposta = self.receber_msg(self.servidor)
            #tratar msg oque é IP e oque são as portas
            IP = 0
            porta = [0,1]
            x = 0
            while(x < self.conexoes.__len__()):
                conexao = self.conexoes[x]
                if(conexao.getpeername[0] == IP):
                     y = 0
                     while(y < porta.__len__()):
                         if(conexao.getpeername()[1] == porta[y]):
                             conexao.shutdown(socket.SHUT_RDWR)
                             conexao.close()
                             self.add_porta(conexao.getsockname()[1])
                         y += 1
        
    #Desconectar do servidor
    def desconectar_servidor(self):
        if(self.servidor != None):
            self.shutdown(socket.SHUT_RDWR)
            self.servidor.close()
            self.add_porta(self.servidor.getsockname()[1])
            self.servidor = None
    
    #fecha todos os sockets de cliente 
    def desconectar(self):
        while(self.conexoes != []):
            conexao = self.conexoes.pop()
            conexao.shutdown(socket.SHUT_RDWR)
            conexao.close()
            self.add_porta(conexao.getsockname()[1])
        self.shutdown(socket.SHUT_RDWR)
        self.socket.close()
    
    #envia nome para o servidor e retorna com IP e lista de portas.
    def search_portas(self,cliente_nome):
        if(self.servidor == None):
            print('Erro,aplicação não está conectadaa com o servidor,tente novamente.')
            return None
        #mudar msg depois com padrão
        msg = f'Desejo as informações de {cliente_nome}'
        self.enviar_msg(msg, self.servidor)
        resposta = self.receber_msg(self.servidor)
        print(f'{resposta}')
    
    #remover cliente da tabela do servidor    
    def desvincular_cliente(self):
        if(self.servidor == None):
            print('Erro,aplicação não está conectada com o servidor,tente novamente.')
            return None
        #mudar msg depois com padrão
        msg = 'Desejo me desvincular'
        self.enviar_msg(msg, self.servidor)
        self.desconectar_servidor()
        
    #Ainda pode ser melhorado e deve ser testado
    def enviar_msg(self, msg, conexao):
        totalEnviado = 0
        try:
            while totalEnviado < msg.__len__():
                msgEnviada = conexao.send(msg[totalenviado:])
                if msgEnviada == 0:
                    raise RuntimeError(f"Ocorreu um erro com a conexão do socket {conexao.getpeername}")
                totalenviado = totalenviado + msgEnviada
        except RuntimeError as e:
            print(f'{e}')
            
    #peguei exemplo do python,devo mudar isso depois.
    def receber_msg(self, conexao):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = conexao.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)
        
        
cliente = NO_Cliente('192.168.1.9', 31045, 'Liam')
p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
p.settimeout(180.0)
p.bind(('192.168.1.9', 30045))
p.listen()

cliente.conectar_servidor('192.168.1.9', 30045)
cliente.desconectar()
p.shutdown(socket.SHUT_RDWR)
p.close()

