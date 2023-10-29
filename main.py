#O socket cliente deve:
#Registrar-se no servidor utilizando um nome e um IP exclusivos e indicando a porta apta para receber o pedido de chamada;
#Realizar consultas de endereços de portas por nomes específicos dos usuários;
#Caso o cliente deseje se desvincular do servidor de registro, ele deve enviar uma mensagem com esta solicitação.

#O socket servidor deve:
#Armazenar e imprimir uma tabela dinâmica contendo informações dos clientes;
#Imprimir mensagem de confirmação de registro de novo usuário;
#Caso o usuário já esteja cadastrado, imprimir mensagem informando esta condição;
#Responder aos clientes o nome de um nó conectado e seus respectivos endereços e números de porta, quando assim solicitado;
#Caso o cliente solicite o fim da conexão, o servidor deve responder com mensagem de encerramento e, depois, fechar o socket.

import socket
import threading

class NO_Cliente:
    def __init__(self, IP, porta, nome):
        self.IP = IP
        self.porta = porta
        self.nome = nome
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