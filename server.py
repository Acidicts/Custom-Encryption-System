import socket
import threading
from encrypt import encrypt
from decrypt import decrypt
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

clients = {}
dict_lock = threading.Lock()


def handle_client(client_socket, addr):
    global clients
    try:
        logging.info(f"Client {addr} connected.")
        with dict_lock:
            clients[addr] = client_socket
        while True:
            encrypted_message = client_socket.recv(4096).decode()
            if encrypted_message:
                logging.debug(f"Message received from {addr}. Encrypted message: {encrypted_message}")
                broadcast_message(encrypted_message, addr)
    except Exception as e:
        logging.error(f"Error with {addr}: {e}")
    finally:
        cleanup_connection(addr)


def broadcast_message(message, sender_addr):
    global clients
    with dict_lock:
        for addr, client_socket in clients.items():
            if addr != sender_addr:
                try:
                    client_socket.send(message.encode())
                    logging.debug(f"Message broadcast sent to {addr}.")
                except Exception as e:
                    logging.error(f"Error broadcasting message to {addr}: {e}")
                    cleanup_connection(addr)
    logging.debug("Broadcast complete.")


def cleanup_connection(addr):
    with dict_lock:
        if addr in clients:
            clients[addr].close()
            del clients[addr]
            logging.info(f"Connection with {addr} cleaned up.")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 5500))
    server.listen(5)
    logging.info("Server listening on 127.0.0.1:5500")
    while True:
        client_socket, addr = server.accept()
        logging.info(f"Accepted connection from: {addr}")
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

if __name__ == "__main__":
    main()
