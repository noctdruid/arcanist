import os
import sys
sys.path.append(os.path.abspath('../src/'))

from arc.operations import Operations


if __name__ == '__main__':
    Operations().special().show()
