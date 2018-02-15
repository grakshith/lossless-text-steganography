import math
import random
def get_primes(lower, upper):
	primes = []
	for i in range(lower, upper):
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
	for i in range(2, int(math.sqrt(n))+1):
		if n%i == 0:
			flag=1
			break

	return not flag


def relative_prime(a, b):
	for i in range(2, min(a, b)+1):
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
	print "GCD({},{}) is {}".format(init_e,phi,gcd)
	if t<0:
		t = t+phi
	return t


def generate_key_pair(size):
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
	print "p and q are {} {}".format(p, q)
	return ((e,p*q),(d,p*q))


def string_to_decimal(text):
	return (''.join(format(ord(c)) for c in text))

def encrypt(key, pt):
	e, n = key
	# pt_decimal = string_to_decimal(pt)
	
	# if(pt_decimal > n):
	# 	print "Choose a larger n"
	# 	return
	cipher_text = [int((pow(ord(char), e))%n) for char in pt]
	return cipher_text
# print get_primes(1, 100)
# print string_to_decimal("AB")


def decrypt(key, ct):
	d,n = key
	plain_text = [int((pow(c,d))%n) for c in ct]
	return plain_text


if __name__ == '__main__':
	key = generate_key_pair(10)	
	print "Public Key : (e,n) = {}".format(key[0])											
	print "Cipher text is {}".format(decrypt(key[1],encrypt(key[0], "aba")))
