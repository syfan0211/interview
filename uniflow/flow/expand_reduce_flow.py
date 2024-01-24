"""Flow class."""
import copy
import logging
from typing import Any, Mapping, Sequence

from uniflow import constants
from uniflow.flow.flow_factory import FlowFactory
from uniflow.node import Node

logger = logging.getLogger(__name__)


class ExpandReduceFlow(Flow):
    """Flow class."""

    def __init__(self, root_node):
        self.expand_op = ExpandOp(root_node)
        self.reduce_op = ReduceOp(self.expand_op.expand_1, self.expand_op.expand_2)





