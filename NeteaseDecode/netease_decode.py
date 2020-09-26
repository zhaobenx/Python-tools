# -*- coding: utf-8 -*-
"""
Created on 2020-07-03 01:16:16
@Author: ZHAO Lingfeng
@Version : 0.0.1
"""
import sys

import numpy as np

def main():
    key = 0xa3
    with open(sys.argv[1], 'rb') as f:
        buf = f.read()

    with open(sys.argv[1] + '.mp3', 'wb') as fw:
        array = np.frombuffer(buf, np.uint8)
        array = array ^ key
        fw.write(array.tobytes())


if __name__ == "__main__":
    main()