#!/usr/bin/env python3

import time

from segen.cli import main

if __name__ == "__main__":

    seconds_start = time.time()
    main()
    # exit()
    seconds_end = time.time()
    print(f'#@time')
    print(f'time used(s):{seconds_end-seconds_start}')

