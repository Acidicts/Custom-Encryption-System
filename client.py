import socket
import threading
from encrypt import encrypt
from decrypt import decrypt



def listen_for_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(4096).decode()
            if message:
                print(f"\n\nEncrypted message: {message}")
                decrypted_message = decrypt(message)
                print(f"New message: {decrypted_message}")
                print("\nPress Enter to continue...")
        except Exception as e:
            print(f"\nError receiving message: {e}")
            if str(e) == "Invalid base64-encoded string: number of data characters (5) cannot be 1 more than a multiple of 4":
                print("Potential MIM Broadcast Recommend to exit.")
            print("Any Errors are incorrect encoding or decoding.")
            print("AKA MIM\n")
            break


def send_messages(client_socket):
    while True:
        message = input("Enter your message: ")
        if message == "/exit":
            break
        encrypted_message = encrypt(message).encode()
        try:
            client_socket.send(encrypted_message)
        except OSError as e:
            print(f"Socket error: {e}")
            break


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(("127.0.0.1", 5500))
        threading.Thread(target=listen_for_messages, args=(client_socket,)).start()
        send_messages(client_socket)
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
