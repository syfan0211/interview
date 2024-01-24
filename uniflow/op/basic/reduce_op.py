"""Linear operation."""
import copy
from typing import Any, Mapping, Sequence

from uniflow.node import Node
from uniflow.op.op import Op


class ReduceOp(Op):
    def __init__(self, expand_1, expand_2, merge_func=None):
        super().__init__({})
        self.merge_func = merge_func if merge_func else self.default_merge
        self.merge_func(expand_1, expand_2)

    def default_merge(self, expand_1, expand_2):
        for k1, v1 in expand_1.value_dict.items():
            for k2, v2 in expand_2.value_dict.items():
                self.value_dict[f"{k1} {k2}"] = f"{v1} {v2}"
        return self.value_dict

    def merge_func(self, expand_1, expand_2):
        # Custom merge logic can be implemented here
        self.default_merge(expand_1, expand_2)
        return self.default_merge(expand_1, expand_2)