#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import socket
import threading
from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad

# DES Encryption - same as client - added up top for clarity
des_key = b'password'
cipher = DES.new(des_key, DES.MODE_ECB)

# Server setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 43210))  # Bind the server to localhost on port 43210
server.listen()  # Listen for incoming connections

clients = []  # List to keep track of clients
nicknames = []  # List to keep track of client nicknames

def broadcast(message, encrypted = False):
    """Send a message to all connected clients."""
    prefix = b"[ENC]" if encrypted else b""
    for client in clients:
        try:
            client.send(prefix + message)
        except:
            # Handle the case where sending message fails
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('utf-8'), encrypted=False)
            nicknames.remove(nickname)

def handle(client):
    """Handle messages from clients."""
    while True:
        try:
            encrypted_message = client.recv(1024)
            if encrypted_message:
                if len(encrypted_message) % DES.block_size == 0:
                    decrypted_message = unpad(cipher.decrypt(encrypted_message), DES.block_size).decode()
                    nickname = nicknames[clients.index(client)]
                    print(f"Encrypted message from {nickname}: {encrypted_message}")
                    print(f"Unencrypted message from {nickname}: {decrypted_message}")
                    broadcast(encrypted_message, encrypted=True) 
                else:
                    print("Received misaligned data")
        except Exception as e:
            print(f"An error occurred: {e}")
            break

def receive():
    """Accept new connections and start a new thread for each client."""
    while True:
        try:
            client, address = server.accept()
            print(f"Connected with {str(address)}")

            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            nicknames.append(nickname)
            clients.append(client)

            print(f'Nickname of the client is {nickname}!')
            broadcast(f'{nickname} joined the chat!'.encode('utf-8'), encrypted=False)
            client.send('Connected to the server!'.encode('utf-8'))

            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        except KeyboardInterrupt:
            print("Server is shutting down...")
            for client in clients:
                client.close()
            server.close()
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            server.close()
            break

try:
    print("Server is listening...")
    receive()
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    server.close()

