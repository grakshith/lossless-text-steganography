
# README

In this project, we have implemented the papers
1. Highly Imperceptible and Reversible Text Steganography Using Invisible Character based Codeword
2. Increasing Robustness of LSB Audio Steganography Using a Novel Embedding Method

As a part of Module 3, we have also implemented Image steganography.

## Files in this module:

The files are modularized into sender and receiver sections. The communication between the sender and the receiver happens over the network through a socket.


1. priority_queue.py : This is our implementation of the priority queue data structure, which is required for Huffman Encoding.

2. huffman.py : This contains the implementation of Huffman Encoding for secret text.

3. RSA.py : This contains the implementation of the RSA Algorithm, which we have used to encrypt the secret text.

4. secret_message.py : This is wrapper class, which combines all the three above mentioned classes and encripts and encodes the secret message using the mentioned techniques.

5.
  * test_text.sh : This contains a few test cases to demonstrate text steganography.
  * test_audio.sh :  This contains a few test cases to demonstrate audio steganography.

6. embed.py : This file contains functions to embed secret message in a cover text file and writes to new stego text file.

7. deembed_text.py : This contains functions to retrieve the secret message from the stego text file.

8. read_wavfile.py : This file reads a cover audio wav file and embeds the secret message in the kth LSB of the audio.

9. retrieve_message.py : This file reads the stego audio file and recovers the secret message from it.

10. embed_image.py : This file reads a cover image and embeds the secret image in the LSB of the cover image

11. deembed_image.py : This file reads the stego image and recovers the secret image from the stego image.

12. client.py : This file is used to send any file to the receiver. Used on the sender end.

13. server.py : This file is used to receive files from the sender. Used on the receiver end.

## System Requirements:

1. Python 2.7 installed
2. No external libraries required as all functionality has been implemented.


## Pipeline:

1. First, the file RSA.py is run, to generate the public and private keys. This gets serialized in pickled/RSA_Keys
  * These keys are then transferred to the receiver using the client and server scripts.
2. The user enters a secret message which he wishes to send to the receiver, by executing the file `secret_message.py`.
3. This message is then encrypted using RSA Algorithm, by making use of the public key generated above.  
  * The input messages are segemented into units of two characters. These bi-grams are then RSA encrypted.
4. Then, this encrypted message is encoded using Huffman Encoding to reduce bit length. The Huffman Keywords are serialised in pickled/keys.
  * These keys are then transferred to the receiver using the client and server scripts.
5. The user is given a choice to choose between text and audio steganography.
6. If text steganography is chosen:
	a. The user is asked to enter the path of cover text
	b. A random seed is generated and a pseudo-random sequence is generated using this seed.
	This sequence is used to embed the secret message randomly in the cover text.
	c. A stego text is obtained and written to stego_text/filename
	d. To recover the message: The receiver runs deembed_text.py and specifies the stego text file path.
	e. Using the keys that were pickled previously, the secret message is recovered.
7. If audio steganography is chosen:
	* The user is asked to enter the path of cover audio.
	* Depending on the length of the audio and length of the secret message, a spread factor is calculated as :
		(length of audio/length of secret message)
	* Each bit of the secret message is embedded in the kth LSB(set to 4) of the cover audio sample. The other bits are modified as 	   		   mentioned in the paper to reduce the error induced because of embedding.
	* The message is distributed over the whole length of the cover audio file using the spread factor.
	* The adjacent samples of the changed sample are modified as mentioned in the paper to shape the noise and reduce the hissing sounds, 		   which may occur.
	* The stego audio is written to stego_audio/filename.wav
	* To recover the message: The receiver runs `retrieve_message.py` and specifies the stego audio file path.
	* Using the keys that were pickled previously, the secret message is recovered from the audio.   
8. Sender: Huffman(RSA(PlainText))
9. receiver: RSA_D(Huffman_D(CipherText))
10. For image steganography, the message to be embedded is an image. Therefore, this embeds the image into a cover image. This is done by modifying the LSBs of the
cover image.


## Usage:

1. Run the command `python secret_message.py` in the project `src/sender` directory
2. Enter the secret message
3. Choose 1 or 2 for text/audio steganography
4. Enter path of file
5. Run `deembed_text.py` / `retrieve_message.py` in `src/receiver` to recover the message
6. Run `embed_image.py` in `src/sender` for image steganography
7. Run `deembed_image.py` in `src/receiver` to recover the secret message.
