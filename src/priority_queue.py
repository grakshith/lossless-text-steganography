class TreeNode:
    def __init__(self, data):
        self.parent = None
        self.left = None
        self.right = None
        self.data = data

class PriorityQueue:

	def __init__(self, array):

		self.heap = array
		self.heap_size = len(array)

	def get_minimum(self):

		return self.heap[0]

	def extract_minimum(self):
		if self.heap_size <= 0:
			return -1

		heap_min = self.heap[0]
		self.heap[0] = self.heap[self.heap_size-1]
		self.heap_size = self.heap_size-1
		self.min_heapify(0)
		return heap_min

	def min_heapify(self, i):
		l = 2*i+1
		r = 2*i+2
		if l<self.heap_size and self.heap[l].data[0] < self.heap[i].data[0]:
			largest = l
		else:
			largest = i

		if r<self.heap_size and self.heap[r].data[0] < self.heap[largest].data[0]:
			largest = r

		if largest != i:
			temp = self.heap[i]
			self.heap[i] = self.heap[largest]
			self.heap[largest] = temp
			self.min_heapify(largest)

	def build_min_heap(self):
		for i in range((self.heap_size-1)/2, -1, -1):
			self.min_heapify( i)

	def get_heap(self):
		return [x.data for x in self.heap[0:self.heap_size]]

	def insert_min_heap(self, key):
		self.heap_size = self.heap_size+1
		if(len(self.heap) == self.heap_size-1):
			self.heap.append(key)
		else:
			self.heap[self.heap_size-1] = key
		i = self.heap_size-1;
		while i>=1 and self.heap[(i+1)/2-1].data[0] > self.heap[i].data[0]:
			temp = self.heap[i]
			self.heap[i] = self.heap[(i+1)/2-1]
			self.heap[(i+1)/2-1] = temp
			i = (i+1)/2-1



if __name__ == '__main__':
	obj = PriorityQueue([TreeNode((8,'0110')), TreeNode((9,'1111')), TreeNode((12,'0000')),
						TreeNode((10,'1101')), TreeNode((13,'1100')), TreeNode((15,'1011')),
						TreeNode((17,'1111'))])
	obj.build_min_heap()
	print obj.get_heap()
	print obj.extract_minimum().data
	print obj.get_heap()
	print obj.extract_minimum().data
	print obj.get_heap()
	print obj.extract_minimum()
	print obj.get_heap()
	obj.insert_min_heap(TreeNode((6,'1110')))
	print obj.get_heap()
