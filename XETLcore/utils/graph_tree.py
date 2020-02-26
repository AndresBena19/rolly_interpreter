from anytree import Node
from anytree.dotexport import RenderTreeGraph
from XETLast.ast import StringAexp, IntAexp, FloatAexp
from collections import deque
import uuid


class Tree_XETLtree:

    def __init__(self, ast, filename=None):
        self.root_node = None
        self.keys = {}
        self.nodes = deque([])
        self.nodes_keys = {}
        self.built(ast)
        RenderTreeGraph(self.nodes[0]).to_picture(filename=filename)

    def built(self, root):
        stack = deque([])
        pre_order = [root.key]
        stack.append(root.key)
        self.keys[root.key] = root

        node_count = 0

        node_parent = Node('Node({}) : {}'.format(root.__class__.__name__, node_count))
        self.nodes.append(node_parent)
        self.nodes_keys[root.key] = node_parent

        while len(stack) > 0:

            parent = self.keys.get(stack[len(stack) - 1])

            if isinstance(parent, (StringAexp, FloatAexp, IntAexp)):
                stack.pop()
            else:
                node_parent = self.nodes_keys.get(parent.key)
                branches = list(filter(lambda node: False if isinstance(node, uuid.UUID) else True,
                                       list(parent.__dict__.values())))
                if len(branches) == 0:
                    stack.pop()
                else:
                    self.keys[parent.key] = parent

                for node in branches:
                    node_count += 1
                    if isinstance(node, (str, int, float, bool)):
                        node_operator = Node('Node({}) : {}'.format(node, node_count),
                                             parent=node_parent)
                        node_parent = node_operator
                        self.nodes.append(node_operator)

                    elif node.key not in pre_order:
                        node_operator = Node('Node({}) : {}'.format(node, node_count),
                                             parent=node_parent)
                        self.nodes.append(node_operator)
                        self.nodes_keys[node.key] = node_operator
                        stack.append(node.key)
                        pre_order.append(node.key)
                        self.keys[node.key] = node

                if len(stack) == 1:
                    stack.popleft()
                else:
                    len_branches = list(filter(lambda node: False if isinstance(node, (uuid.UUID, str)) else True,
                                               list(parent.__dict__.values())))
                    del stack[(len(stack) - len(len_branches)) - 1]

        print(pre_order)
        print(self.keys)
        return node_parent
