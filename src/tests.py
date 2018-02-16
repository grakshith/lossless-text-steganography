from RSA import *
from secret_message import *

messages = ["Hello world", "This is a test message to test the RSA encryption",
            "This test message is huffman encoded and the codewords are prefix free",
            "Encryption and decryption of this test message happens with the modular exponentiation algorithm for faster results"]

def encrypt(message, key):

    obj = SecretMessage(message)
    print "Encrypting message with RSA..."
    obj.symbol_list = RSA.encrypt(key[0], obj.message)
    encoded =  obj.encode()
    print "\n"
    print "Huffman encoded message: {}".format(encoded)
    decoded = obj.decode()
    print "\n"
    print "Huffman decoded message: {}".format(decoded)
    print "\n"
    print "Decrypting decoded message with RSA..."
    decrypted = ''.join(map(chr,RSA.decrypt(key[1], decoded)))
    print decrypted
    print "\n\n"
    assert obj.symbol_list == decoded
    assert message == decrypted

print "Tests for key size: 20bits"
key = RSA.generate_key_pair(20)
for message in messages:
    encrypt(message, key)
print "----------------------------------------"
print "\n\n"

print "Tests for key size: 30bits"
key = RSA.generate_key_pair(30)
for message in messages:
    encrypt(message, key)
print "----------------------------------------"
print "\n\n"

print "Tests for key size: 40bits"
key = RSA.generate_key_pair(40)
for message in messages:
    encrypt(message, key)
print "----------------------------------------"
print "\n\n"
