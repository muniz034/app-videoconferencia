import socket
import threading

DEST_IP = "26.248.40.162"  # Change to the destination IP address (Client B)
DEST_PORT = 12346  # Change to the destination port for Client B
LISTEN_PORT = 12345  # Port to listen for incoming audio from Client B

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

udp_socket.bind(("127.0.0.1", LISTEN_PORT))

def receive_audio():
    while True:
        data, _ = udp_socket.recvfrom(1024)
        print("Mensagem de Pedro: " + data.decode())

# Start a thread to receive audio from Client B
receive_thread = threading.Thread(target=receive_audio)
receive_thread.start()

try:
    while True:
        data = input("Write message: ")
        udp_socket.sendto(data.encode(), (DEST_IP, DEST_PORT))
except KeyboardInterrupt:
    print("Stopping...")
finally:
    udp_socket.close()
