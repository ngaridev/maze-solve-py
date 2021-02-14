
from os import getcwd, path
if __name__ == '__main__':
    t = path.join(getcwd() + "Mazes")
    print(path.exists(t))
    print(t)