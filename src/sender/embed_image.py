
import cv2
import numpy as np


def get_message_from_image(imname):
	image = cv2.imread(imname)
	print image.shape

	with open('pickled/keys_imsteg', 'w') as fp:
		fp.write(str(image.shape[0])+'\n')
		fp.write(str(image.shape[1])+'\n')
		fp.write(str(image.shape[2])+'\n')

	image = np.reshape(image, (image.shape[0]*image.shape[1]*image.shape[2]))
	print image.shape
	return image

def set_bit(value, bit):
	# print "Val is ",value | (1<<bit)
	return value | (1<<bit)

def clear_bit(value, bit):
	# print "Val is ", value & ~(1<<bit)
	return value & ~(1<<bit)

def embed_in_image(image, sec_image):
	ctr=0
	flag=0
	message = ''

	frame = cv2.imread(image)
	# print frame[0][0][:]
	image_bin = get_message_from_image(sec_image)
	print image_bin[0:10]
	# exit(0)
	message = ''
	for i in image_bin:
		message+='{0:08b}'.format(i)
	print len(message)


	flag=0
	# print ctr

	for i in range(frame.shape[0]):
		for j in range(frame.shape[1]):
			for k in range(frame.shape[2]):
				# if k==0:
				if message[ctr] == '1':
					print "changing ",frame[i][j][k], 'to 1' 
					frame[i][j][k] = set_bit(frame[i][j][k], 0)
					print frame[i][j][k], 'at ',i, j, k
				else:
					print "changing ",frame[i][j][k], 'to'
					frame[i][j][k] = clear_bit(frame[i][j][k], 0)
					print frame[i][j][k], 'at ',i, j, k
				ctr+=1
				
				if ctr==len(message):
					flag=1
					break
			if flag==1:
				break
		if flag==1:
			break	



	# print message[1:1000]	
	# image = []
	# for i in range(0, len(message),8):
	# 	image.append(int(message[i:i+8], 2))

	# image = np.array(image)
	# print image.shape
	# image = np.reshape(image, (50, 50, 3))
	print "The stego image saved as stego_images/"+image.split('/')[-1]
	cv2.imwrite('stego_images/'+image.split('/')[-1], frame)
# print '1001001001110101101'

if __name__ == '__main__':
	cov_im = raw_input("Enter the path of cover image: \n")
	sec_im = raw_input("Enter the path of secret image: \n")
	embed_in_image(cov_im, sec_im)