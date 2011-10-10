#!/usr/bin/env python

class Node(object):
    """A node for our tree"""

    def __init__(self, data = None, line=1, type=None):
        self.data = data
        self.children = []
        self.parent = None
        self.type = type
        self.preorderList = []
        self.preorderCurrent = -1
        self.postorderList = []
        self.postorderCurrent = -1
        self.line = line

    def addChild(self, node):
        self.children.append(node)
        node.parent = self
        return node

    def addParent(self, node):
        if self.parent == None:
            self.parent = node
            node.children.append(self)
        else:
            oldParent = self.parent
            self.parent = node
            node.parent = oldParent
            node.children.append(self)
            oldParent.children.remove(self)
            oldParent.children.append(node)
        return node

    def inPlaceRemove(self):
        if len(self.children) == 1:
            if self.parent:
                pos = self.parent.children.index(self)
                self.parent.children[pos] = self.children[0] 
                self.children[0].parent = self.parent
            else:
                self.children[0].parent = None     

    def remove(self):
        '''Deletes a node and it's subtrees'''
        self.parent.children.remove(self)
        return self

    def preorder(self, root=None):
        if not root:
            root = self
        root.preorderList.append(self)
        
        for child in self.children:
            child.preorder(root)        

    def getPreorderNode(self):
        if not self.preorderList:
            self.preorder()
        self.preorderCurrent += 1
        if self.preorderCurrent >= len(self.preorderList):
            return None
        return self.preorderList[self.preorderCurrent]            
        
    def postorder(self, root=None):
        if not root:
            root = self
        for child in self.children:
            child.postorder(root)
        
        root.postorderList.append(self)

    def getPostorderNode(self):
        if not self.postorderList:
            self.postorder()
        self.postorderCurrent +=1
        if self.postorderCurrent >= len(self.postorderList):
            return None
        return self.postorderList[self.postorderCurrent]

    def __str__(self, space=0):
        space += 1
        alldata = '(' + self.data + ')'
        for child in self.children:
            linestr = ''
            for i in range(space):
                linestr += str(i) 
            alldata += '\n' + str(linestr) + child.__str__(space)
        return alldata

if __name__ == "__main__":
    root = Node("a")
    rootchild1 = Node("b")
    rootchild2 = Node("c")
    root.addChild(rootchild1)
    root.addChild(rootchild2)
    child2child = Node("d")
    rootchild1.addChild(child2child)
    eNode = Node("e")
    child2child.addChild(eNode)
    child2child.addChild(Node("g"))
    child2child.addChild(Node("h"))
    root.addChild(Node("f"))

    print root

    print '*' * 10
    print 'add node i as e\'s parent'
    print '*' * 10

    iNode = Node('i')
    eNode.addParent(iNode)

    print root
    
    print '*' * 10
    print 'add node j as i\'s parent'
    print '*' * 10

    jNode = Node('j')
    iNode.addParent(jNode)

    print root
    
    print '*' * 10
    print 'remove a node with children'
    print '*' * 10

    #child2child.remove()

    print root
    
    print '*' * 10
    print 'a preorder traveral of the last tree'
    print '*' * 10
    currentNode = root.getPreorderNode()
    while currentNode:
        print currentNode.data
        currentNode = root.getPreorderNode()

    print '*' * 10
    print 'a postorder traveral of the last tree'
    print '*' * 10
    currentNode = root.getPostorderNode()
    while currentNode:
        print currentNode.data
        currentNode = root.getPostorderNode()
