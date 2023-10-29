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
     
    #fecha 1 socket de cliente       
    def desconectar_cliente(self, nome):
        if(self.servidor == None):
            print('Erro,aplicação não está conectadaa com o servidor,tente novamente.')
            return None
        #pergunta para o server passando o nome do cliente em questão e retorna as portas e IP da conexão
        IP = 0
        porta = 1
        lista = []
        while(self.conexoes != []):
            conexao = self.conexoes.pop()
            conexao = self.socket
            if(conexao.getpeername() == (IP,porta)):
                conexao.close()
                self.add_porta(conexao.getsockname()[1])
            else:
                lista.append(conexao)
        lista.reverse()
        self.conexoes = lista
        
    #Desconectar do servidor
    def desconectar_servidor(self):
        if(self.servidor != None):
            self.servidor.close()
            self.add_porta(self.servidor.getsockname()[1])
            self.servidor = None
    
    #fecha todos os sockets de cliente      como avisar aos outros?  
    def desconectar(self):
        while(self.conexoes != []):
            conexao = self.conexoes.pop()
            conexao = self.socket
            conexao.close()
            self.add_porta(conexao.getsockname()[1])
        self.socket.close()
    
    #envia nome para o servidor e retorna com IP e lista de portas.
    def search_portas(self,cliente_nome):
        if(self.servidor == None):
            print('Erro,aplicação não está conectadaa com o servidor,tente novamente.')
            return None
        print('Fazer')
    
    #remover cliente da tabela do servidor    
    def desvincular_cliente(self):
        if(self.servidor == None):
            print('Erro,aplicação não está conectadaa com o servidor,tente novamente.')
            return None
        print('Fazer')
        
        
cliente = NO_Cliente('192.168.1.9', 31045, 'Liam')
p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
p.settimeout(180.0)
p.bind(('192.168.1.9', 30045))
p.listen()

cliente.conectar_servidor('192.168.1.9', 30045)
cliente.desconectar()
p.close()

