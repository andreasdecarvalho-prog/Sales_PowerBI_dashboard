import os

def print_tree(startpath, prefix=""):
    entries = [e for e in os.listdir(startpath) 
               if e != ".git" and "__pycache__" not in e]
    entries.sort()
    for i, name in enumerate(entries):
        path = os.path.join(startpath, name)
        connector = "├── " if i < len(entries) - 1 else "└── "
        print(prefix + connector + name)
        if os.path.isdir(path):
            new_prefix = prefix + ("│   " if i < len(entries) - 1 else "    ")
            print_tree(path, new_prefix)

# Run it for the current folder
print_tree(".")
