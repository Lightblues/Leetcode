import ast

s = open("./hello.py").read()
print(
    ast.dump(ast.parse(s), indent=4)
)