import os
import sys
sys.path.append(os.path.abspath('../../src/arc/'))

from operations import Operations


if __name__ == '__main__':
    Operations().special()._board()
