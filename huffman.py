from priority_queue import PriorityQueue, TreeNode

class HuffmanTree:
    def __init__(self,sym_freq_list):
        """sym_freq_list is a list that contains the symbols and their associated
        frequencies, where each list item is a tuple in the form (freq,symbol)
        """
        self.sym_freq_list = sym_freq_list
        self.codewords = {}


    def get_codewords(self):
        self.tree_nodes_list = [TreeNode(x) for x in self.sym_freq_list]
        self.pq = PriorityQueue(self.tree_nodes_list)
        self.pq.build_min_heap()
        self.tree_ptr = None
        while self.pq.heap_size>1:
            first = self.pq.extract_minimum()
            second = self.pq.extract_minimum()
            third = TreeNode((first.data[0]+second.data[0], ''))
            third.left = first
            third.right = second
            self.tree_ptr = third
            print third.left, third.right
            first.parent = third
            second.parent = third
            self.pq.insert_min_heap(third)
        print self.tree_ptr.data
        print self.tree_ptr.left.data
        print self.tree_ptr.right.data
        # self.walk_huffman_tree(self.tree_ptr)

    def walk_huffman_tree(self, root, arr=[]):
        if root.left:
            arr.append(0)
            self.walk_huffman_tree(root.left, arr)

        if root.right:
            arr.append(1)
            self.walk_huffman_tree(root.right, arr)

        if not (root.left and root.right):
            self.codewords[root.data[1]] = ''.join(map(str,arr))




if __name__ == '__main__':
    obj = HuffmanTree([(8,'0110'), (9,'1111'), (12,'0000'), (10,'1101'), (13,'1100'), (15,'1011'), (17,'1111')])
    obj.get_codewords()
    obj.walk_huffman_tree(obj.tree_ptr)
    print obj.codewords
