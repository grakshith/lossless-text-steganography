from huffman import HuffmanTree
import RSA
import cPickle as pickle
import read_wavfile
import embed

class SecretMessage:
	def __init__(self, message):
		self.codewords = {}
		self.d_codewords = {}
		self.message = message

	def string_to_binary(self):
		return ''.join(format(ord(c), 'b') for c in self.message)

	def make_symbol_list(self, bin_str, n):
		self.symbol_list = [bin_str[i:i+n] for i in range(0, len(bin_str), n)]
		return self.symbol_list

	def encode(self):
		# binary = self.string_to_binary()
		# binary = '010000010111010101110100011010000110111101110010001000000100100101000100001110100010000000110001001100000011000000110001'
		# self.symbol_list = self.make_symbol_list(binary, 7)
		# print "Symbol List : {}".format(self.symbol_list)
		freq_table = {}
		for symbol in self.symbol_list:
			if freq_table.get(symbol):
				freq_table[symbol] = freq_table[symbol]+1
			else:
				freq_table[symbol] = 1
		symbol_tup_list = []
		for symbol in freq_table:
			symbol_tup_list.append((freq_table[symbol], symbol))
		print "Symbol list with frequencies:"
		print symbol_tup_list
		huff_tree = HuffmanTree(symbol_tup_list)
		self.codewords = huff_tree.get_codewords()
		print "Huffman codewords:"
		print self.codewords
		self.d_codewords = {self.codewords[key]:key for key in self.codewords}
		self.message = ''.join(self.codewords[symbol] for symbol in self.symbol_list)
		with open('pickled/keys','wb') as fp:
			pickle.dump(self.d_codewords,fp)
			pickle.dump(len(self.message),fp)
		return self.message

	def decode(self):
		i=0
		j=0
		decoded = []
		while i < len(self.message):
			if self.d_codewords.get(self.message[i:i+j]):
				decoded.append(self.d_codewords.get(self.message[i:i+j]))
				i=i+j
				j=0
			else:
				j = j+1
		self.message = decoded
		return self.message


if __name__ == '__main__':
	message = raw_input("Enter the secret text:")
	obj = SecretMessage(message)
	with open('pickled/RSA_Keys', 'rb') as file:
		key = pickle.load(file)
	print "Encrypting message with RSA..."
	obj.symbol_list = RSA.encrypt(key[0], obj.message)
	encoded =  obj.encode()
	print "Encoded = "+encoded
	inp_file = raw_input("Enter audio filename path:")
	embed.embed_in_text_file(inp_file, encoded)
	# read_wavfile.embed_to_file(inp_file, encoded)
	print "Huffman encoded message: {}".format(encoded)
	# decoded =  obj.decode()
	# print "Huffman decoded message: {}".format(decoded)
	# print "Decrypting decoded message with RSA..."
	# print ''.join(map(chr,RSA.decrypt(key[1], decoded)))
