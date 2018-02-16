
# README 

In this project, we have implemented the first module of the paper "Highly Imperceptible and Reversible Text Steganography Using Invisible Character based Codeword" 

## Files in this module:

1. priority_queue.py : This is our implementation of the priority queue data structure, which is required for Huffman Encoding.

2. huffman.py : This contains the implementation of Huffman Encoding for secret text. 

3. RSA.py : This contains the implementation of the RSA Algorithm, which we have used to encrypt the secret text. 

4. secret_message.py : This is wrapper class, which combines all the three above mentioned classes and encrupts and encodes the secret message using the mentioned techniques. 

5. tests.py : This contains a few test cases to demonstrate the project. Assert sttements have been inserted in suitable places to verify the encryption, decryption, decoding and encoding. 

## System Requirements:

1. Python 2.7 installed
2. No external libraries required as all functionality has been implemented. 


## Pipeline:

1. First, the user enters a secret message which he wishes to send to the receiver. 
2. This message is then encrypted using RSA Algorithm. It is assumed that the public key is available to the sender. A key-pair is generated in RSA.py.
3. Then, this encrypted message is encoded using Huffman Encoding to reduce bit length.
4. This is transmitted to the receiver using text steganoraphy, which will be implemented in the next module. 
5. The receiver then decodes the message and then decrypts it using his private key.
6. The encryption and decryption happens in the same file as of now, but will be changed accordingly during the implementation of the next module. 
7. Sender: Huffman(RSA(PlainText))
8. receiver: RSA_D(Huffman_D(CipherText))

## Usage: 

1. Run the command 'python secret_message.py' in the project root directory
2. Enter the secret message
3. Enter the key length (10-40)
