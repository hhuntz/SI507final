import rent_and_restaurants
import plotly.graph_objects as go 
from time import sleep
import json

class BinarySearchTree:

    def __init__(self):
        self.root = None
        self.size = 0

    def length(self):
        return self.size

    def __len__(self):
        return self.size

    def __iter__(self):
        return self.root.__iter__()

    def put(self,key,val):
        if self.root:
            self._put(key,val, self.root)
        else: 
            self.root = TreeNode(key,val)
        self.size = self.size + 1
    
    def _put(self,key,val,currentNode):
        if key < currentNode.key:
            if currentNode.hasLeftChild():
                self._put(key,val,currentNode.leftChild)
            else:
                currentNode.leftChild = TreeNode(key,val,parent=currentNode)
        else:
            if currentNode.hasRightChild():
                self._put(key,val,currentNode.rightChild)
            else:
                currentNode.rightChild = TreeNode(key,val,parent=currentNode)

    def get(self,key):
        if self.root:
            res = self._get(key,self.root)
            if res:
                return res.payload
            else:
                return None
        else:
            return None
        
    def _get(self,key,currentNode):
        if not currentNode:
            return None
        elif currentNode.key == key:
            return currentNode
        elif key < currentNode.key:
            return self._get(key,currentNode.leftChild)
        else:
            return self._get(key,currentNode.rightChild)
        
    def __getitem__(self,key):
        return self.get(key)  

class TreeNode:
    def __init__(self,key,val,left=None,right=None,parent=None):
        self.key = key
        self.payload = val
        self.leftChild = left
        self.rightChild = right
        self.parent = parent

    def hasLeftChild(self):
        return self.leftChild

    def hasRightChild(self):
        return self.rightChild

    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self

    def isRightChild(self):
        return self.parent and self.parent.rightChild == self

    def isRoot(self):
        return not self.parent

    def isLeaf(self):
        return not (self.rightChild or self.leftChild)

    def hasAnyChildren(self):
        return self.rightChild or self.leftChild

    def hasBothChildren(self):
        return self.rightChild and self.leftChild

    def replaceNodeData(self,key,value,lc,rc):
        self.key = key
        self.payload = value
        self.leftChild = lc
        self.rightChild = rc
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self

def tree():
    '''Creates a tree mapping avg. restaurant distance and rent data
    Really only exists to prove I know how to build a tree
    Wish I knew how to make this actually be useful, but it doesn't
    seem like storing restaurants this way would make anything easier or better.'''
    bst = BinarySearchTree()
    address_dict = rent_and_restaurants.get_cache('address_cache.txt')
    for address in address_dict.values(): # create lists of distances and rents to compare
        try:
            if address['rent'] != 'unknown':
                distance = 0
                for cuisine in address.values():
                    try:
                        distance += int(cuisine['distance'])
                    except:
                        pass
                avg_distance = (distance/3)*0.000621371 # average and convert meters to miles
                avg_distance = round(avg_distance, 2)
                bst.put(int(address['rent']),avg_distance)
        except: # if rent key doesn't exist for some reason - seems to happen in only 1 of the calls with normal cache
            pass
    return bst

def print_tree(root):
    if root is None:
        return
    print_tree(root.leftChild)
    print(f'rent: {root.key} / distance:{root.payload}')
    print_tree(root.rightChild)

rents = []
distances = []
def make_list_from_tree(root):
    if root is None:
        return
    make_list_from_tree(root.leftChild)
    rents.append(root.key)
    distances.append(root.payload)
    make_list_from_tree(root.rightChild)
    combined_list = zip(rents, distances)
    return combined_list

def analyze(tree):
    print("Here's a scatter plot that shows the relationship between the average distance to a restaurant and the avg rent near an apartment.")
    print('One moment while we load your visualization...')
    zipped_list = list(make_list_from_tree(tree.root))
    dists = [x[1] for x in zipped_list if x[0] != -666666666]
    rents = [x[0] for x in zipped_list if x[0] != -666666666]
    print(dists)
    print(rents)

    scatter_data = go.Scatter(
        x=dists, 
        y=rents, 
        marker={'symbol':'circle', 'size':20, 'color': 'blue'},
        mode='markers', 
        textposition="top center")
    basic_layout = go.Layout(title="Rent vs. Avg. Distance from Closest Restaurants")
    fig = go.Figure(data=scatter_data, layout=basic_layout)

    fig.write_html("rentsdistance.html", auto_open=True)

    sleep(10)

if __name__ == '__main__':
    #analyze()
    bst = tree()
    analyze(bst)
    #print_tree(bst.root)

            

