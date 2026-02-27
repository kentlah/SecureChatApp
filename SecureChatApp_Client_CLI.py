#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import socket
import threading
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

des_key = b'password'
cipher = DES.new(des_key, DES.MODE_ECB)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 43210))

nickname = input("Enter your nickname: ")
client.send(nickname.encode('utf-8'))


def receive():
    """Handles receiving messages from the server."""
    while True:
        try:
            '''
            message = client.recv(1024)
            if message.decode().startswith('NICK'):
                # If it's the 'NICK' message, ignore it or handle it specially if needed
                continue
            elif message.startswith(b"[ENC]"):
                # Remove the prefix before decryption
                encrypted_message = message[5:] 
                if len(encrypted_message) % DES.block_size == 0:
                    decrypted_message = unpad(cipher.decrypt(encrypted_message), DES.block_size).decode()
                    print(decrypted_message)
                else:
                    print("Received misaligned data")
            '''
            '''Testing a fix for the above - client receives an error:
            Error receiving data: 'utf-8' codec can't decode byte 0xfa in position 0: invalid start byte
            Basically determing if encrypted, then decoding it.'''
            message = client.recv(1024)
            # Directly work with message bytes, avoid premature decoding
            if message.startswith(b"[ENC]"):
                try:
                    # Extract the encrypted portion after the marker
                    encrypted_message = message[5:] 
                    # Decrypt and then decode
                    decrypted_message = unpad(cipher.decrypt(encrypted_message), DES.block_size).decode('utf-8')
                    print(decrypted_message)
                except Exception as decryption_error:
                    print(f"Decryption error: {decryption_error}")
            elif b'NICK' in message:
                continue  # Ignore the 'NICK' message
            else:
                print(message.decode('utf-8'))
        except UnicodeDecodeError as e:
            print(f"Decoding error: {e}")
        except Exception as e:
            print(f"Error receiving data: {e}")
            client.close()
            break

def write():
    """Handles sending messages to the server."""
    while True:
        message = f'{nickname}: {input("")}'
        if message:
            padded_message = pad(message.encode(), DES.block_size)
            encrypted_message = cipher.encrypt(padded_message)
            try:
                client.send(encrypted_message)
            except Exception as e:
                print(f"Failed to send message: {e}")

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

