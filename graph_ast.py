from anytree import Node
from anytree.dotexport import RenderTreeGraph
from ast import *


class Tree_Program:

    def __init__(self, ast, parent=None, cont=None):
        self.cont = 0

        if cont:
            self.cont = cont

        name = ''
        if hasattr(ast, 'name'):
            name = ast.name

        name_node = '{}->{} '.format(ast.__class__.__name__, name) if name else '{}'.format(ast.__class__.__name__)

        if not parent:
            self.root = Node('Node({1}) \n {0}'.format(name_node, self.cont))
        else:
            self.root = parent

        self.nodes = []
        self.built(ast, self.root)

        RenderTreeGraph(self.root).to_picture("tree.png")

    def built(self, ast, parent=None):

        if hasattr(ast, 'first'):
            self.cont = self.cont + 1

            name = ''
            if hasattr(ast.first, 'name'):
                name = ast.first.name

            name_first = '{} -> {}'.format(ast.first.__class__.__name__, name) if name else '{}'.format(
                ast.first.__class__.__name__)
            first = Node('Node({1}) \n {0}'.format(name_first, self.cont), parent=parent)
            self.nodes.append(first)
            self.built(ast.first, first)

            if hasattr(ast, 'second'):
                self.cont = self.cont + 1

                name = ''
                if hasattr(ast.second, 'name'):
                    name = ast.second.name

                name_second = '{}  -> {}'.format(ast.second.__class__.__name__, name) if name else '{}'.format(
                    ast.second.__class__.__name__)
                second = Node('Node({1}) \n {0}'.format(name_second, self.cont), parent=parent)
                self.nodes.append(second)
                self.built(ast.second, second)
            else:
                self.cont = self.cont + 1
                new_cont = self.cont
                if isinstance(ast, Aexp) or isinstance(ast, AssignStatement):
                    new_cont = Aritmetic_Exp(ast, parent, self.cont).cont
                elif isinstance(ast, IfStatement):
                    new_cont = IfExp(ast, parent, self.cont).cont
                self.cont = new_cont
        else:
            self.cont = self.cont + 1
            new_cont = self.cont
            if isinstance(ast, Aexp) or isinstance(ast, AssignStatement):
                new_cont = Aritmetic_Exp(ast, parent, self.cont).cont
            elif isinstance(ast, IfStatement):
                new_cont = IfExp(ast, parent, self.cont).cont

            self.cont = new_cont



class IfExp:
    def __init__(self, ast, parent=None, cont=None):
        self.cont = 0
        self.nodes = []
        if cont:
            self.cont = cont

        name = ast.__class__.__name__

        if not parent:
            self.root = Node('Node({1}) \n {0}'.format(name, self.cont), parent=parent)
        else:
            self.root = parent

        condition = Node('Node({1}) \n {0}'.format("condition", self.cont), parent=parent)
        relexp = Relexp(ast.condition, condition, self.cont)
        self.cont = relexp.cont

        self.built(ast, parent)

    def built(self, ast, parent=None):

        if hasattr(ast, 'true_stmt'):
            name = ''
            if hasattr(ast.true_stmt, 'name'):
                name = ast.true_stmt.name

            self.cont = self.cont + 1
            true_stmt = Node('Node({1}) \n {0}'.format("true_stmt", self.cont), parent=parent)
            name_right = '{}->{}'.format(ast.true_stmt.__class__.__name__, name) if not hasattr(ast.true_stmt,
                                                                                                'op') else ast.true_stmt.op
            self.cont = self.cont + 1

            right = Node('Node({1}) \n {0}'.format(name_right, self.cont), parent=true_stmt)
            self.nodes.append(right)
            self.built(ast.true_stmt, right)

            if hasattr(ast, 'false_stmt'):
                name = ''
                if hasattr(ast.false_stmt, 'name'):
                    name = ast.false_stmt.name

                self.cont = self.cont + 1
                false_stmt = Node('Node({1}) \n {0}'.format("false_stmt", self.cont), parent=parent)
                name_left = '{} -> {}'.format(ast.false_stmt.__class__.__name__, name) if not hasattr(ast.false_stmt,
                                                                                                      'op') else ast.false_stmt.op
                self.cont = self.cont + 1

                left = Node('Node({1}) \n {0}'.format(name_left, self.cont), parent=false_stmt)
                self.nodes.append(left)
                self.built(ast.false_stmt, left)
            else:
                self.cont = self.cont + 1
                new_cont = Tree_Program(ast, parent, self.cont).cont
                self.cont = new_cont
        else:
            self.cont = self.cont + 1
            new_cont = Tree_Program(ast, parent, self.cont).cont
            self.cont = new_cont

class Relexp:
    def __init__(self, ast, parent=None, cont=None):
        self.cont = 0
        self.nodes = []
        if cont:
            self.cont = cont

        name = ast.__class__.__name__ if not hasattr(ast, 'op') else ast.op

        self.cont = self.cont + 1

        if parent:
            self.root = Node('Node({1}) \n {0}'.format(name, self.cont), parent=parent)
        else:
            self.root = Node('Node({1}) \n {0}'.format(name, self.cont))

        self.built(ast, self.root)

    def built(self, ast, parent=None):

        if hasattr(ast, 'left'):
            self.cont = self.cont + 1

            name_left = '{}'.format(ast.left.__class__.__name__) if not hasattr(ast.left, 'op') else ast.left.op
            left = Node('Node({1}) \n {0}'.format(name_left, self.cont), parent=parent)
            self.nodes.append(left)
            self.built(ast.left, left)

            if hasattr(ast, 'right'):
                self.cont = self.cont + 1

                name_right = '{}'.format(ast.right.__class__.__name__) if not hasattr(ast.right, 'op') else ast.right.op
                right = Node('Node({1}) \n {0}'.format(name_right, self.cont), parent=parent)
                self.nodes.append(right)
                self.built(ast.right, right)
            else:
                self.cont = self.cont + 1
                if isinstance(ast, NotBexp):
                    new_cont = Relexp(ast.exp, parent, self.cont).cont
                    self.cont = new_cont
                else:
                    self.cont = self.cont + 1
                    self.nodes.append(Node('Node({1}) \n {0}'.format(ast.__dict__, self.cont), parent=parent))
        else:
            self.cont = self.cont + 1

            if isinstance(ast, NotBexp):
                new_cont = Relexp(ast.exp, parent, self.cont).cont
                self.cont = new_cont
            else:
                self.cont = self.cont + 1
                self.nodes.append(Node('Node({1}) \n {0}'.format(ast.__dict__, self.cont), parent=parent))


class Aritmetic_Exp:
    def __init__(self, ast, parent=None, cont=None):
        self.cont = 0
        if cont:
            self.cont = cont

        name = ast.__dict__.values()[0].__class__.__name__ if not hasattr(ast.__dict__.values()[0], 'op') else \
            ast.__dict__.values()[0].op

        if parent:
            self.root = Node('Node({1}) \n {0}'.format(name, self.cont), parent=parent)
        else:
            self.root = Node('Node({1}) \n {0}'.format(name, self.cont))

        self.nodes = []
        self.built(ast.__dict__.values()[0], self.root)

    def built(self, ast, parent=None):

        if hasattr(ast, 'left'):
            self.cont = self.cont + 1

            name_left = '{}'.format(ast.left.__class__.__name__) if not hasattr(ast.left, 'op') else ast.left.op
            left = Node('Node({1}) \n {0}'.format(name_left, self.cont), parent=parent)
            self.nodes.append(left)
            self.built(ast.left, left)

            if hasattr(ast, 'right'):
                self.cont = self.cont + 1

                name_right = '{}'.format(ast.right.__class__.__name__) if not hasattr(ast.right, 'op') else ast.right.op
                right = Node('Node({1}) \n {0}'.format(name_right, self.cont), parent=parent)
                self.nodes.append(right)
                self.built(ast.right, right)
            else:
                self.cont = self.cont + 1

                if isinstance(ast, NotBexp):
                    new_cont = Relexp(ast.exp, parent, self.cont).cont
                    self.cont = new_cont
                else:
                    self.cont = self.cont + 1
                    self.nodes.append(Node('Node({1}) \n {0}'.format(ast.__dict__, self.cont), parent=parent))
        else:
            self.cont = self.cont + 1

            if isinstance(ast, NotBexp):
                new_cont = Relexp(ast.exp, parent, self.cont).cont
                self.cont = new_cont
            else:
                self.cont = self.cont + 1
                self.nodes.append(Node('Node({1}) \n {0}'.format(ast.__dict__, self.cont), parent=parent))
        return self.cont
