# Your task is to compute the number of disk accesses for searching on a B-tree thru experiments with the following assumptions:

#     Keys are positive integers.
#     A page can hold 1K keys (with default size for integers), where K = 1,024, and the associated data, with the minimum degree t = 512.  
#     Available RAM for storing B-tree nodes: 64K nodes, where each node is a page (a node may not be full, but that still takes a page).
#     Ignore how a page is addressed on disk. In other words, you may simply assume that retrieving one page takes 1 DISK-READ which is 1 disk access (with associated data), 
#     and storing one page to disk takes 1 DISK-WRITE, which is 1 disk acess. Moreover, each disk-read only reads one page and each disk-write only writes one page.
#     Disk storage is sufficiently large that can hold 100K keys and the data associated with them (which pages contain which keys depend on the construction of the B-tree).
#     The root note is in RAM.

# In each round of experiment, use a random permutation to permute 1, 2, ..., 100,000 to be used as keys. Construct a B-tree for these keys in the permuted order and store the tree on the disk (imaginary). 
# At the beginning, only the root node of the B-tree is in RAM. Then generate a randome sequence of 100 numbers using a pseudo-random number generator between the range of 1 and 100,000, which is the sequence of keys to search for data. 
# Count the number of disk accesses that actually happens for this search sequence. For example, suppose a key k is at level 2 in the tree, where the root is at the level 0, 
# then you will first need to read in the parent node of the node that contains k by checking with the root node, from the parent node, you read in the node (page) that contains k and get the data associated with k. 
# This incurs 2 DISK-READ. When the allocated space of 64K in RAM is full, you will need to release one page back to the disk, first in first out. 
# For simplicity, assume that when you release a page you need to write this page back to disk since the data associated with a key may be changed, which incurs 1 disk access. 
# If the node containing key k is already in RAM, then there is no need of disk access.

# Run the experiment for 10 rounds, compute the minimum, maximum, and the average numbers of disk accesses. What conclusions can you draw?

import collections
import numpy as np
import random

# Create a node
class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.children = []
        
# BTree
class BTree:
    def __init__(self, t): # t is the minimum degree
        self.root = BTreeNode(True)
        self.t = t
        self.disk_accesses = 0
        self.cache = collections.OrderedDict()
        self.cache_capacity = 64 * 1024 // (t * 2 + 1)

    # Search key k starting from node
    # If node is not specified, search k starting from the root
    def search_key(self, k, node=None):
        if node is None:
            return self.search_key(k, self.root)
        else: # node is a current node
            i = 0
            while i < len(node.keys) and k > node.keys[i][0]:
                i += 1
            if i < len(node.keys) and k == node.keys[i][0]:
                return (node, i) # found k
            elif node.leaf: # if k is not in node and node has no children
                return None
            else:
                if node.children[i] in self.cache:
                    child = self.cache[node.children[i]]
                else:
                    child = self._read_node(node.children[i])
                    self.cache[node.children[i]] = child
                self.disk_accesses += 1
                return self.search_key(k, node.children[i])
               
    # Insert key k, which is in th form of a pair key and content
    def insert(self, k):
        root = self.root
        if len(root.keys) == 2 * self.t - 1: # full--no keys are available
            temp = BTreeNode()
            self.root = temp
            temp.children.insert(0, root) 
            #list insert: at location 0, insert root; that is, temp points to root
            self.split_child(temp, 0)
            self.insert_non_full(temp, k)
        else:
            self.insert_non_full(root, k)
            
    # Split the children node at location i
    def split_child(self, node, i): 
        t = self.t # minimum degree
        y = node.children[i]
        z = BTreeNode(y.leaf)
        node.children.insert(i + 1, z) # list insert
        node.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t: (2 * t) - 1]
        y.keys = y.keys[0: t - 1]
        if not y.leaf:
            z.children = y.children[t: 2 * t]
            y.children = y.children[0: t - 1]

    # Insert nonfull
    def insert_non_full(self, node, k):
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append((None, None)) # add a new key pair holder (None, None)
            while i >= 0 and k[0] < node.keys[i][0]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = k # insert k
        else:
            while i >= 0 and k[0] < node.keys[i][0]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == (2 * self.t) - 1:
                self.split_child(node, i)
                if k[0] > node.keys[i][0]:
                    i += 1
            self.insert_non_full(node.children[i], k)

    # Print the tree
    def print_tree(self, node, l=0):
        print("Level ", l, " ", len(node.keys), end=":")
        # for i in node.keys:
            # print(i, end=" ")
            
        # print()
        l += 1
        if len(node.children) > 0:
            for i in node.children:
                self.print_tree(i, l)

    def _read_node(self, node_id):
        # Here, we simulate reading a node from disk by generating a new node
        # with randomly generated keys and children.
        node = BTreeNode(self.t)
        node.keys = [k + 1 for k in np.random.permutation(1000000)[:2 * self.t - 1]]
        node.children = [i for i in range(len(node.keys) + 1)]
        return node   


# driver code

B = BTree(512)
num_elements = 100000
key_list = [k + 1 for k in np.random.permutation(num_elements)]
for i in range(num_elements):
    B.insert((i, key_list[i]))


B.print_tree(B.root)


all_disk_accesses = []
for _ in range(10):
    search_list = random.sample(range(1, num_elements), 100)
    disk_accesses = []
    for key in search_list:
        try:
            if B.search_key(key) is not None:
                disk_accesses.append(B.disk_accesses)
            B.disk_accesses = 0
        except:
            continue
    all_disk_accesses.append(disk_accesses)

print("\n\n")
for i in range(len(all_disk_accesses)):
    print(f"Round {i+1}")
    print(f"Max accesses: {max(all_disk_accesses[i])}", end = " | ")
    print(f"Min accesses: {min(all_disk_accesses[i])}", end = " | ")
    print(f"Average accesses: {sum(all_disk_accesses[i])//len(all_disk_accesses[i])}")
    print()

# We can see that the maximum number of disk accesses needed is at most 1, using t=512. 
# This is because all of the keys are getting stored in the first layer of the B-Tree and so it never has to go
# travel more than one node deep. Since it accesses an element in node in the first layer, it also loads that particular node
# into the cache. If an element is present in the cache, the number of disk accesses drops to 0 as it gets searched in the cache first
# before moving to search in memory.
# We can see different and varying results if we lower the value of t, as the tree will expand upwards and the search will have to 
# descent lower, thus increasing memory accesses.