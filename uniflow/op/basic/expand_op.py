"""Linear operation."""
import copy
from typing import Any, Mapping, Sequence

from uniflow.node import Node
from uniflow.op.op import Op


class ExpandOp(Op):
    def __init__(self, root_node, split_func=None):
        super().__init__(root_node.value_dict)
        self.split_func = split_func if split_func else self.default_split
        self.expand_1, self.expand_2 = self.split_func()


    def default_split(self):
        n = len(self.value_dict)
        half = n // 2
        return {k: self.value_dict[k] for k in list(self.value_dict.keys())[:half]}, \
               {k: self.value_dict[k] for k in list(self.value_dict.keys())[half:]}

    def split_func(self):
        # Custom split logic can be implemented here
        return self.default_split()