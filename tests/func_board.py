import os
import sys
sys.path.append(os.path.abspath('../src/'))

from arctasks.operations import Operations


if __name__ == '__main__':
    Operations().special().board()
