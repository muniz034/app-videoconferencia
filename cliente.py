import socket
import threading

class NO_Cliente:
    def __init__(self, IP, porta, nome):
        self.IP = IP
        self.porta = porta
        self.nome = nome
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(180.0)
        self.socket.bind((self.IP, self.porta))
        #self.socket.listen()
        self.conexoes = []
                
    def conectar_servidor(self, servidor_IP, servidor_porta):
        try:
            conexao = self.socket.dup()
            conexao.connect((servidor_IP, servidor_porta))
            self.conexoes.append(conexao)
            print(f'Conexão bem-sucedida com IP: {servidor_IP} | porta: {servidor_porta}')
        except socket.error as e:
            print(f'Conexão mal-sucedida com IP: {servidor_IP} | porta: {servidor_porta}')
            print(f'Erro encontrado: {e}')
            
    def conectar_cliente(self, NO_IP, NO_porta):
        try:
            conexao = self.socket.connect((NO_IP, NO_porta))
            self.conexoes.append(conexao)
            print(f'Conexão bem-sucedida com IP: {NO_IP} | porta: {NO_porta}')
        except socket.error as e:
            print(f'Conexão mal-sucedida com IP: {NO_IP} | porta: {NO_porta}')
            print(f'Erro encontrado: {e}')
            
    def desconectar_conexao(self):
        print('Fazer')
            
    def desconectar(self):
        while(self.conexoes.__sizeof__() > 0):
            print(f'{1}')
            conexao = self.conexoes.pop()
            conexao.close()
        self.socket.close()
    
    def search_portas(self,cliente_nome):
        print('Fazer')
        
    def desvincular_cliente():
        print('Fazer')
        
        
cliente = NO_Cliente('192.168.1.9', 31045, 'Liam')
p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
p.settimeout(180.0)
p.bind(('192.168.1.9', 30045))
p.listen()

cliente.conectar_servidor('192.168.1.9', 30045)
p.close()
cliente.desconectar()

