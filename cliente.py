import socket
import threading

class NO_Cliente:
    def __init__(self, IP, porta, nome):
        self.IP = IP
        self.porta = porta
        self.nomes = nome
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conexoes = []
                
    def conectar_servidor(self, servidor_IP, servidor_porta):
        try:
            conexao = self.socket.connect((servidor_IP, servidor_porta))
            self.conexoes.append(conexao)
            print(f'Conexão bem-sucedida com IP: {servidor_IP} | porta: {servidor_porta}')
        except socket.error as e:
            print(f'Conexão mal-sucedida com IP: {servidor_IP} | porta: {servidor_porta}')
            print(f'Erro encontrado: {e}')
            
    def desconectar_servidor():
        print('Fazer')
            
    def conectar_cliente(self, NO_IP, NO_porta):
        try:
            conexao = self.socket.connect((NO_IP, NO_porta))
            self.conexoes.append(conexao)
            print(f'Conexão bem-sucedida com IP: {NO_IP} | porta: {NO_porta}')
        except socket.error as e:
            print(f'Conexão mal-sucedida com IP: {NO_IP} | porta: {NO_porta}')
            print(f'Erro encontrado: {e}')
            
    def desconectar_cliente():
        print('Fazer')
        
    def search_portas(self,cliente_nome):
        print('Fazer')
        
    def desvincular_cliente():
        print('Fazer')