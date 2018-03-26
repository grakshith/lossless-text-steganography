
import cv2
import numpy as np

# exit(0)
def deembed(imname):
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
				
				if ctr==60000:
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
	image = np.reshape(image, (50, 50, 3))
	print image.shape
	cv2.imwrite('cover_video/secret_image.png', image)

if __name__ == '__main__':
	deembed('cover_video/stego_bird1.png')