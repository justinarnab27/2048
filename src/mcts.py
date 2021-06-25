import numpy as np

'''
we have 4 steps selection, expansion, simulation, backup
'''

c = 2

class node:
	board = []
	value = 50
	n = 9
	children = []

	def ugb(self,N):
		if self.n == 0 or N == 0:
			return 1e9
		return self.value/self.n + c*np.sqrt(np.log(N)/self.n) 

	def choose_a_node(self,N):
		arr = np.zeros(len(self.children))
		for i in range(len(self.children)):
			arr[i] = self.children[i].ugb(N)
		print(self.children[np.argmax(arr)])
		print(arr)
#def selection(current_node,tree_path):
#	tree_path.append(current_node)
#	if current_node.children:
#		choose_a_node()	
#	else:
#		return

ob = node()
ch1 = node()
ch2 = node()
ch3 = node()
ch1.value = 40
ch1.n = 4
ch2.value =32
ch2.n = 3
ch3.value = 80
ch3.n = 8
ob.children.append(ch1)
ob.children.append(ch2)
ob.children.append(ch3)
N = 5

ob.choose_a_node(N)