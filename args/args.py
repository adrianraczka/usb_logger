import argparse

class ArgsParser():
    def __init__(self):
        self.default_baudrate = 115200
        
        self.parser = argparse.ArgumentParser(description="descripton")
        self.parser.add_argument("-p", type=str, nargs='+', help='<Required> Set port', required=True)
        self.parser.add_argument("-b", type=int, nargs='+', help='<Optional> Set baudrate, default=115200', default=115200, required=False)
        self.parser.add_argument("-f", type=str, help='<Required> Set file path', required=True)
        self.parser.add_argument("-pr", "--prefix", type=str, help='<Optional> Set file prefix', required=False)
        self.parser.add_argument("-d", "--debug", action='store_true', help='<Optional> Debug option', required=False)

        self.args = self.parser.parse_args()
    
    def get_args(self):
        return self.args._get_kwargs()

    def get_ports(self) -> list:
        return self.args.p
    
    def get_baudrates(self) -> int:
        return self.args.b
    
    def get_default_baudrate(self) -> int:
        return self.default_baudrate
        
    def get_file_path(self) -> str:
        return self.args.f
    
    def get_file_prefix(self) -> str:
        return self.args.prefix

    def get_debug(self) -> bool:
        return self.args.debug
        
    def print_args(self) -> None:
        for flag, value in self.get_args():
            print(f"{flag}: {value}")