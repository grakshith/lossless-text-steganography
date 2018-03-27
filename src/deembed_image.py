
import cv2
import numpy as np

# exit(0)
def deembed(imname, size):
	ctr=0
	flag=0
	message = ''
	# while(cap.isOpened()):
	frame = cv2.imread(imname)
	print frame[0][0][:]
	# ret,f2 = cap2.read()
	# print f2[0][0][:]
	# continue

		# print frame.shape	
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	# print frame

	flag=0
	# print ctr

	for i in range(frame.shape[0]):
		for j in range(frame.shape[1]):
			for k in range(frame.shape[2]):
				# if k==0:
				if frame[i][j][k] & (1<<0):
					print 'Reading ',frame[i][j][k]
					message+='1'
				else:
					print 'else Reading ',frame[i][j][k]
					message+='0'
				ctr+=1
				
				if ctr==size[0]*size[1]*size[2]*8:
					flag=1
					break
			if flag==1:
				break
		if flag==1:
			break	

	# print message[1:1000]	
	print len(message)
	image = []
	for i in range(0, len(message),8):
		# print i
		image.append(int(message[i:i+8], 2))
	print image[0:10]
	image = np.array(image)
	print image.shape
	image = np.reshape(image, size)
	print image.shape
	print "The secret image has been saved as cover_video/secret_image.png"
	cv2.imwrite('cover_video/secret_image.png', image)

if __name__ == '__main__':
	with open('pickled/keys_imsteg', 'r') as fp:
		# size = ()
		a = fp.read()
		a = a.split('\n')
		size = (int(a[0]) ,int(a[1]), int(a[2]))
		print size
		# exit(0)
		# fp.write(str(image.shape[1])+'\n')
		# fp.write(str(image.shape[2])+'\n')
	steg_im = raw_input("Enter the path of stego image: \n")
	deembed(steg_im, size)