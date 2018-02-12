import huffman


codewords = {}
d_codewords = {}

def string_to_binary(string):
	return ''.join(format(ord(x), 'b') for x in string)

# print string_to_binary("A")

def make_list(bin_str, n):
	symbol_list = []
	symbol_list = [bin_str[i:i+n] for i in range(0, len(bin_str), n)]
	return symbol_list


def encode(text):
	binary = string_to_binary(text)
	symbol_list = make_list(binary, 4)
	print symbol_list
	freq_table = {}
	for symbol in symbol_list:
		if freq_table.get(symbol):
			freq_table[symbol] = freq_table[symbol]+1

		else:
			freq_table[symbol] = 1
	symbol_tup_list = []
	for symbol in freq_table:
		symbol_tup_list.append((symbol,freq_table[symbol]))

	print symbol_tup_list
	# global codewords, d_codewords
	codewords = huffman.codebook(symbol_tup_list)
	print codewords
	d_codewords = {codewords[key]:key for key in codewords}
	# print ''.join(symbol for symbol in symbol_list)
	# print ''.join(codewords[symbol] for symbol in symbol_list)
	return ''.join(codewords[symbol] for symbol in symbol_list)

encode("AAA")
# print make_list("101000111", 4)
# print huffman.codebook([('A', 2), ('B', 4), ('C', 1), ('D', 1)])	

print codewords
def decode(text):
	i=0
	j=0
	decoded = []
	while i < len(text):
		if d_codewords.get(text[i:i+j]):
			decoded.append(d_codewords.get(text[i:i+j]))
			i=i+j
			j=0
		else:
			j = j+1
	print ''.join(decoded)

decode('10000111011101')