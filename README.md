# SecureChatApp

A multi-client secure chat application built in Python using TCP sockets
and symmetric encryption (DES).

This project demonstrates:

-   Client/server networking
-   Thread-based concurrency
-   Symmetric encryption
-   Basic protocol design

DES is used for educational purposes only and is not secure for
production systems.

------------------------------------------------------------------------

## Requirements

-   Python 3.x
-   pycryptodome

Install dependency:

    pip install pycryptodome

------------------------------------------------------------------------

## How to Run

### 1. Start the Server

From the project directory:

    python SecureChatApp_Server_CLI.py

You should see:

    Server is listening...

------------------------------------------------------------------------

### 2. Start the Client

Open a new terminal window and run:

    python SecureChatApp_Client_CLI.py

You will be prompted to enter a nickname.

Note: The client immediately sends the nickname to the server upon
connection. The server also sends a "NICK" prompt, but the client does
not wait for it before sending the nickname.

------------------------------------------------------------------------

## Multiple Clients

To connect multiple users:

-   Open additional terminal windows
-   Run the client script again
-   Enter different nicknames

Each client runs in a separate process.

------------------------------------------------------------------------

## Architecture

### Server

-   Listens for incoming TCP connections on localhost:43210
-   Sends a "NICK" command to prompt for a nickname
-   Stores client sockets and nicknames in lists
-   Handles each client in a separate thread
-   Decrypts incoming encrypted messages
-   Broadcasts the received encrypted message (prefixed with "\[ENC\]")
    to all connected clients
-   Logs encrypted and decrypted messages to the server console
-   Sends join/leave notifications in plaintext

### Client

-   Establishes TCP connection to localhost:43210
-   Sends nickname immediately after connecting
-   Encrypts outgoing messages using DES
-   Decrypts incoming encrypted messages
-   Uses threading to send and receive concurrently

------------------------------------------------------------------------

## Encryption Workflow

### Client Side

1.  User enters a message
2.  Message is padded to match DES block size (8 bytes)
3.  Message is encrypted using a shared DES key (ECB mode)
4.  Encrypted bytes are sent to the server

### Server Side

1.  Server receives encrypted bytes
2.  Server decrypts using the same DES key
3.  Padding is removed
4.  Encrypted and decrypted versions are logged to the console
5.  The original encrypted bytes are rebroadcast to all clients (with a
    "\[ENC\]" prefix)

------------------------------------------------------------------------

## Technical Concepts Demonstrated

-   TCP socket programming
-   Client/server architecture
-   Thread-based concurrency
-   Symmetric encryption (DES in ECB mode)
-   Block cipher padding
-   Broadcast messaging
-   Basic application-level protocol design

------------------------------------------------------------------------

## Network Configuration

-   Host: localhost
-   Port: 43210
-   Protocol: TCP

------------------------------------------------------------------------

## Potential Improvements

-   Replace DES with AES
-   Implement secure key exchange
-   Add authentication
-   Add GUI interface
-   Improve message protocol structure
