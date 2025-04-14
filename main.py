#!/usr/bin/env python3
import os
import sys
import time

from args.args import ArgsParser
from serial_logger.serial_logger import SerialLogger, create_loggers, start_loggers

MAIN_DELAY = 1 # 1 s
THREAD_DIED_ERR = -1

def main() -> int:
    print(f"os: {os.name}")
    args_parser = ArgsParser()
    serial_loggers = create_loggers(args_parser)
    start_loggers(serial_loggers)

    for serial_logger in serial_loggers:
        serial_logger.serial_write(b"reset\n")
    
    while True:
        for serial_logger in serial_loggers:
            serial_logger: SerialLogger
            if not serial_logger.is_alive():
                print("ERROR: Thread died!")
                return THREAD_DIED_ERR
        time.sleep(MAIN_DELAY)

if __name__ == '__main__':
    sys.exit(main())