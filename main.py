#A atividade prática da disciplina consiste em desenvolver uma aplicação de videoconferência descentralizada. Para isso, deve ser #utilizada comunicação por sockets, permitindo que os usuários primeiro se registrem em um servidor e consultem a lista de nós #cadastrados, para depois de conectarem aos seus pares utilizando o modelo Peer-to-Peer (P2P).

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

import socketserver

s = socketserver
print(s.TCPServer.__qualname__)