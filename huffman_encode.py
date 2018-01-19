import huffman

def string_to_binary(string):
	return ''.join(format(ord(x), 'b') for x in string)

# print string_to_binary("ABC")

def make_list(bin_str, n):
	symbol_list = []
	symbol_list = [bin_str[i:i+n] for i in range(0, len(bin_str), n)]
	return symbol_list

# print make_list("101000111", 4)
print huffman.codebook([('A', 2), ('B', 4), ('C', 1), ('D', 1)])	
