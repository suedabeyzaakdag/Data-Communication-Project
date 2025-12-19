Data Transmission with Error Detection Methods
This project demonstrates a practical implementation of data communication and error detection using Python Socket Programming. The system consists of three main components: a Sender, an Intermediate Node (Corruptor), and a Receiver.

Project Architecture
1. Client 1 (Sender): Takes text input, calculates control information using a selected method, and sends a formatted packet: DATA|METHOD|CONTROL.
2. Server (Agent/Corruptor): Intercepts the packet and injects random errors (Bit Flip, Character Swap, Burst Error, etc.) to simulate network noise.
3. Client 2 (Receiver): Receives the potentially corrupted data, recalculates the control bits, and compares them with the original to detect errors.

Implemented Error Detection Methods
* Parity Bit: Checks the count of 1s in binary representation.
* 2D Parity: Matrix-based parity check for rows and columns.
* Internet Checksum: 16-bit summation of character values.
* CRC16 (Cyclic Redundancy Check): Polynomial division for robust error detection.

 How to Run
Follow this specific order to establish the socket connections:

1. Run the Receiver: python client2_receiver.py

2. Run the Server: python server_corruptor.py

3. Run the Sender: python client_sender.py
