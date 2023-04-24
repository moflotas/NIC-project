from gate import Gate

class IndividualNode:
    def __init__(self, gate, individual, parent = None, children = None):
        # gate is index (int) or Gate()
        self.gate = gate
        self.individual = individual
        self.parent = parent
        if not children:
            self.children = []
        else:
            self.children = children

    def is_leaf(self):
        return not self.children
    
    def output(self):
        if self.is_leaf:
            if type(self.gate) != int:
                raise Exception("Leaf node should be an input index.")
        else:
            if type(self.gate) != Gate:
                raise Exception("Not a leaf node should be a gate.")
            pass 

