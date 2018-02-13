

class PriorityQueue:

	def __init__(self, array):

		self.heap = array
		self.heap_size = len(array)
	
	def get_minimum(self):

		return self.heap[0]

	def extract_minimum(self):
		if self.heap_size < 0:
			return -1
		
		heap_min = self.heap[0]
		self.heap[0] = self.heap[self.heap_size-1]
		self.heap_size = self.heap_size-1
		self.min_heapify(0)
		return heap_min

	def min_heapify(self, i):
		l = 2*i+1
		r = 2*i+2
		if l<self.heap_size and self.heap[l] < self.heap[i]:
			largest = l
		else:
			largest = i

		if r<self.heap_size and self.heap[r] < self.heap[largest]:
			largest = r

		if largest != i:
			temp = self.heap[i]
			self.heap[i] = self.heap[largest]
			self.heap[largest] = temp
			self.min_heapify(largest)

	def build_min_heap(self):
		for i in range((self.heap_size-1)/2, -1, -1):
			print i
			self.min_heapify( i)


	def insert_min_heap(self, key):
		self.heap_size = self.heap_size+1
		if(len(self.heap) == self.heap_size-1):
			self.heap.append(key)
		else:	
			self.heap[self.heap_size-1] = key
		i = self.heap_size-1;
		while i>=1 and self.heap[(i+1)/2-1] > self.heap[i]:
			temp = self.heap[i]
			self.heap[i] = self.heap[(i+1)/2-1]
			self.heap[(i+1)/2-1] = temp
			i = (i+1)/2-1



if __name__ == '__main__':
	obj = PriorityQueue([8, 9, 12, 10, 13, 15, 17])
	obj.build_min_heap()
	# obj.insert_min_heap(6)
	print obj.heap
	print obj.extract_minimum()
	print obj.heap
	print obj.extract_minimum()
	print obj.heap
	print obj.extract_minimum()
	print obj.heap
	obj.insert_min_heap(6)
	print obj.heap	
	
	