Nesta etapa, deve ser implementada a lógica do serviço.

O socket cliente deve:
Solicitar a videochamada a um par IP:porta de destino utilizando uma mensagem específica, como se fosse a mensagem de INVITE do protocolo SIP. Assim, o receptor pode negar ou aceitar o pedido;
A reprodução da mídia deve ser iniciada assim que a chamada é aceita;
Conter métodos para encerrar a transmissão.



O socket servidor deve: 
Aceitar ou rejeitar a chamada;
Se a chamada for aceita, informar na resposta o número das portas para receber os fluxos de áudio e vídeo.