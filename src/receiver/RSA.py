import math
import random
import cPickle as pickle
import json
def get_primes(lower, upper):
	primes = []
	for i in xrange(lower, upper):
		if is_prime(i):
			# print i
			primes.append(i)

	return primes


def gcd(a, b):
	while b!=0:
		a, b = b, a%b
	return a

def is_prime(n):
	flag=0
	for i in xrange(2, int(math.sqrt(n))+1):
		if n%i == 0:
			flag=1
			break

	return not flag


def relative_prime(a, b):
	for i in xrange(2, min(a, b)+1):
		if a%i == b%i == 0:
			return False

	return True


def ext_euc(e, tot_n):
	t,s, t_1,s_1 = 0,1, 1,0
	print "q\tr\ts\tt"
	phi = tot_n
	init_e = e
	while e != 0:
		q, r = tot_n//e, tot_n%e

		m, n = t-t_1*q, s-s_1*q
		tot_n,e, t,s, t_1,s_1 = e,r, t_1,s_1, m,n
		# print q, r, s, t
		print "{}\t{}\t{}\t{}".format(q,r,t,s)
	gcd = tot_n
	# print "GCD({},{}) is {}".format(init_e,phi,gcd)
	if t<0:
		t = t+phi
	return t


def generate_key_pair(size):
	print "Generating Keys of size {} bits".format(size)
	print "Extended Eucledian Algorithm"
	min_n = 1 << (size-1)
	max_n = (1 << size) -1
	start_range = 1 << (size//2 - 1)
	end_range = 1 << (size//2 + 1)
	primes = get_primes(start_range, end_range)

	while primes:
		p = random.choice(primes)
		primes.remove(p)
		q_cand = [q for q in primes if min_n<=p*q<=max_n]
		if q_cand:
			q = random.choice(q_cand)
			break


	else:
		print "Cannot find primes!"

	tot_n = (p-1)*(q-1)
	e = random.randrange(1, tot_n)
	g = gcd(e, tot_n)
	while g!=1:
		e = random.randrange(1, tot_n)
		g = gcd(e, tot_n)

	d = ext_euc(e, tot_n)
	print "--------------------------------------------------------------------------"
	print "p and q are {} {}".format(p, q)
	n = p*q
	print "Public Key : (e,n) = ({} ,{})".format(e, n)
	print "Private Key : (d,n) = ({} ,{})".format(d, n)
	print "--------------------------------------------------------------------------"
	return ((e,p*q),(d,p*q))


def string_to_decimal(text):
	return (''.join(format(ord(c)) for c in text))

def power(x, y, p) :
    res = 1
    x = x % p
    while (y > 0) :
        if ((y & 1) == 1) :
            res = (res * x) % p
        y = y >> 1
        x = (x * x) % p

    return res

def encrypt(key, pt):
	e, n = key
	# pt_decimal = string_to_decimal(pt)

	# if(pt_decimal > n):
	# 	print "Choose a larger n"
	# 	return
	print "Before RSA encryption:"
	print pt+"\n"
	message_list = list(pt)
	bigram_list = []
	while len(message_list)>1:
		a = message_list.pop(0)
		b = message_list.pop(0)
		bigram_list.append("{}{}".format(ord(a),ord(b)))
	if len(message_list)>0:
		bigram_list.append(ord(message_list.pop()))
	# bigram_list = ['{}{}'.format(pt[i],pt[i+1]) for i in range(0,len(pt)+offset,2)]
	print bigram_list
	# cipher_text = [int(power(ord(char), e, n)) for char in pt]
	bigram_cipher_text = [int(power(int(char), e, n)) for char in bigram_list]
	print "After RSA encryption:"
	# print cipher_text
	print bigram_cipher_text
	print ""
	print "---------------------------------------------------------------------------"
	# return cipher_text
	return bigram_cipher_text
# print get_primes(1, 100)
# print string_to_decimal("AB")


def decrypt(key, ct):
	d,n = key
	plain_text = [int(power(c,d,n)) for c in ct]
	print plain_text
	plain_text = map(str,plain_text)
	decrypted = []
	for number in plain_text:
		# print number
		if len(number)<4:
			decrypted.append(number)
			continue
		if len(number) == 4:
			first = number[0:2]
			second = number[2:4]
		elif len(number) == 6:
			first = number[0:3]
			second = number[3:6]
		elif len(number) == 5:
			if(number[0]=='1'):
				first = number[0:3]
				second = number[3:5]
			else:
				first = number[0:2]
				second = number[2:5]
		decrypted.append(first)
		decrypted.append(second)
	return map(int,decrypted)


if __name__ == '__main__':
	print "Enter the key length required in bits"
	length = int(raw_input())
	key = generate_key_pair(length)
	with open('pickled/RSA_Keys', 'wb') as file:
		pickle.dump(key, file)
	with open('pickled/RSA_Key_Pub', 'w') as file:
		file.write(json.dumps(key[0]))
	# print "Public Key : (e,n) = {}".format(key[0])
	# print "Cipher text is {}".format(decrypt(key[1],encrypt(key[0], "aba")))
