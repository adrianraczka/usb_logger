import os
import datetime
import threading
import serial

from args.args import ArgsParser

class SerialLoggerException(Exception):
    pass

class SerialLogger(threading.Thread):
    def __init__(self, port: str, baudrate: str, file_prefix: str, file_path: str, debug: bool):
        self.debug = debug
        self.port = port
        self.baudrate = baudrate
        self.serial = None
        
        self.file_prefix = file_prefix
        self.file_path = file_path
        self.file = None
    
        self.started = False
        
        self.init()
        super().__init__(daemon=True)

    def _create_filename_nt(self) -> str:
        if self.file_prefix == None:
            return f"//_{self.port}.log"
        return f"//{self.file_prefix}_{self.port}.log"

    def _create_filename_posix(self) -> str:
        if self.file_prefix == None:
            return f"/_{self.port[5:]}.log"
        return f"/{self.file_prefix}_{self.port[5:]}.log"

    def _create_filename(self) -> None:
        if os.name == "nt": #win32
            self.file_path += self._create_filename_nt()
        elif os.name == "posix":
            self.file_path += self._create_filename_posix()
        else:
            date = datetime.datetime.now()
            self.file_path += f"/{self.file_prefix}_{date.day}_{date.month}_{date.year}.log"
            
    def _open_file(self) -> None:
        try:
            self._create_filename()
            print("Opeing file:", self.file_path)
            self.file = open(file=self.file_path, mode="a")
        except Exception as err:
            raise SerialLoggerException(f"Opeing file failed: {self.file_path}, {err}")
    
    def _open_serial(self) -> None:
        print("Serial initializing on port:", self.port)
        try:
            self.serial = serial.Serial(port=self.port, baudrate=self.baudrate)
        except (Exception) as err:
            raise SerialLoggerException(f"ERROR: Serial initializing failed on port: {self.port}, {err}")

    def init(self) -> None:
        self._open_serial()
        self._open_file()
        
    def serial_read(self) -> bytes:
        return self.serial.readline()
    
    def serial_write(self, data: bytearray) -> (int | None):
        return self.serial.write(data)
    
    def file_write(self, data: bytes) -> int:
        try:
            date = datetime.datetime.now()
            return self.file.write(f"{date}: {data.decode()}")
            # self.file.flush()
        except (Exception) as err:
            raise SerialLoggerException(f"Can not write to file!, {err}")
            
    def start(self) -> None:
        self.started = True
        return super().start()
    
    def is_alive(self) -> bool:
        return super().is_alive() == self.started
    
    def run(self):
        while True:
            try:    
                serial_data = self.serial_read()
                self.file_write(serial_data)
                if self.debug:
                    print(f"{self.port}: {serial_data.decode().rstrip()}")
            except SerialLoggerException as err:
                print(f"{err}")

def create_loggers(args_parser: ArgsParser) -> list:
    serial_loggers = list()

    file_prefix = args_parser.get_file_prefix()
    file_path = args_parser.get_file_path()
    ports = args_parser.get_ports()

    for (idx, port) in enumerate(ports):
        idx: int
        port: str
        try:
            baudrate =  args_parser.get_baudrates()[idx]
        except (IndexError, TypeError):
            baudrate = args_parser.get_default_baudrate()
        
        serial_logger = SerialLogger(port=port, baudrate=baudrate, file_prefix=file_prefix, file_path=file_path, debug=args_parser.get_debug())
        serial_loggers.append(serial_logger)

    return serial_loggers

def start_loggers(serial_loggers: list) -> None:

    for logger in serial_loggers:
        logger.start()