import re
import copy

# ------------ TOKENIZER ------------
def tokenize(expr):
    return re.findall(r'\d+|[a-zA-Z]+|[+*/()-]', expr)

# ------------ AST NODE ------------
class ASTNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __eq__(self, other):
        if not isinstance(other, ASTNode):
            return False
        return (self.value == other.value and
                self.left == other.left and
                self.right == other.right)

# ------------ PARSER ------------
def parse_expression(tokens):
    def parse_factor(i):
        token = tokens[i]
        if token.isdigit() or token.isalpha():
            return ASTNode(token), i+1
        elif token == '(':
            node, j = parse_sum(i+1)
            return node, j+1
        else:
            raise ValueError("Unexpected token: " + token)

    def parse_term(i):
        node, i = parse_factor(i)
        while i < len(tokens) and tokens[i] == '*':
            op = tokens[i]
            right, i = parse_factor(i+1)
            node = ASTNode(op, node, right)
        return node, i

    def parse_sum(i):
        node, i = parse_term(i)
        while i < len(tokens) and tokens[i] == '+':
            op = tokens[i]
            right, i = parse_term(i+1)
            node = ASTNode(op, node, right)
        return node, i

    node, _ = parse_sum(0)
    return node

# ------------ AST PRINTER ------------
def print_ast(node):
    if node.left is None:
        return str(node.value)
    return f"({print_ast(node.left)} {node.value} {print_ast(node.right)})"

# ------------ REWRITE RULES ------------
def rewrite(node):
    if node.left is None:
        return node

    node.left = rewrite(node.left)
    node.right = rewrite(node.right)

    # x + 0 → x
    if node.value == '+' and node.right.value == '0':
        return node.left
    if node.value == '+' and node.left.value == '0':
        return node.right

    # x * 1 → x
    if node.value == '*' and node.right.value == '1':
        return node.left
    if node.value == '*' and node.left.value == '1':
        return node.right

    # x * 0 → 0
    if node.value == '*' and ('0' in [node.left.value, node.right.value]):
        return ASTNode('0')

    # Constant folding
    if node.left.value.isdigit() and node.right.value.isdigit():
        if node.value == '+':
            return ASTNode(str(int(node.left.value) + int(node.right.value)))
        if node.value == '*':
            return ASTNode(str(int(node.left.value) * int(node.right.value)))

    # Distributive: a * (b + c) → a*b + a*c
    if node.value == '*' and node.right.value == '+':
        a = node.left
        b = node.right.left
        c = node.right.right
        return ASTNode('+', ASTNode('*', a, b), ASTNode('*', a, c))

    return node

# ------------ SATURATION ------------
def saturation(ast):
    prev = None
    current = copy.deepcopy(ast)
    while prev != current:
        prev = copy.deepcopy(current)
        current = rewrite(current)
    return current

# ------------ COST MODEL ------------
def cost(node):
    if node.left is None:
        return 1
    return 1 + cost(node.left) + cost(node.right)

# ------------ MAIN RUN ------------
if __name__ == "__main__":
    expr = input("Enter expression: ")
    tokens = tokenize(expr)
    ast = parse_expression(tokens)

    print("\nOriginal:", print_ast(ast))
    optimized = saturation(ast)
    print("Optimized:", print_ast(optimized))
    print("\nCost Before:", cost(ast))
    print("Cost After :", cost(optimized))
