import socket
import threading
            
class NO_Servidor:
    def __init__(self, IP, porta):
        self.IP = IP
        self.porta = porta
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conexoes = []
        self.clientes = []
        #tabela que armazena clientes
        
    def registrar_cliente(self):
        print('Fazer')
        
    def desvincular_cliente(self):
        print('fazer')
    
    def conectar(self, NO_IP, NO_port):
        try:
            conexao = self.socket.connect((NO_IP, NO_port))
            self.conexoes.append(conexao)
            print(f'Conexão bem-sucedida com IP: {NO_IP} | porta: {NO_port}')
        except socket.error as e:
            print(f'Conexão mal-sucedida com IP: {NO_IP} | porta: {NO_port}')
            print(f'Erro encontrado: {e}')

    def desconectar(self):
        print('Fazer')
        
    def get_cliente(self):
        print('Fazer')
        
    def print_clientes(self):
        print('Fazer')