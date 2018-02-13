from huffman import HuffmanTree

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
		binary = self.string_to_binary()
		self.symbol_list = self.make_symbol_list(binary, 4)
		freq_table = {}
		for symbol in self.symbol_list:
			if freq_table.get(symbol):
				freq_table[symbol] = freq_table[symbol]+1
			else:
				freq_table[symbol] = 1
		symbol_tup_list = []
		for symbol in freq_table:
			symbol_tup_list.append((freq_table[symbol], symbol))

		print symbol_tup_list
		huff_tree = HuffmanTree(symbol_tup_list)
		self.codewords = huff_tree.get_codewords()
		print self.codewords
		self.d_codewords = {self.codewords[key]:key for key in self.codewords}
		self.message = ''.join(self.codewords[symbol] for symbol in self.symbol_list)
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
		self.message = ''.join(decoded)
		return self.message


if __name__ == '__main__':
	obj = SecretMessage("AAA")
	print obj.string_to_binary()
	print obj.encode()
	print obj.decode()
