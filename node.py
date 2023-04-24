from gate import Gate, make_gate


class TreeNode:
    def __init__(self, value, input_bits: list, children=None):
        # value is index: int or Gate
        self.value = value
        self.input = input_bits
        if not children:
            self.children = []
        else:
            self.children = children

    def is_leaf(self):
        return not self.children

    def output(self):
        if self.is_leaf():
            if type(self.value) != int:
                raise ValueError("Leaf node should be an input index.")
            if len(self.input) <= self.value:
                raise IndexError(f"Input index exceeds input size. Got: {self.value}; Max: {len(self.input)}.")

            # return value from input
            return self.input[self.value]
        else:
            if type(self.value) != Gate:
                raise ValueError("Parent node should be a gate.")

            # execute gate
            children_values = [c.output() for c in self.children]
            return self.value(*children_values)


input_bits = [1, 0]
leaf_node_1 = TreeNode(1, input_bits)
leaf_node_2 = TreeNode(0, input_bits)
not_node = TreeNode(make_gate('not'), input_bits, children=[leaf_node_1])
and_node = TreeNode(make_gate('and'), input_bits, children=[not_node, leaf_node_2])

print(and_node.output())
