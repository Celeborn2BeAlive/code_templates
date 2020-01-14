import argparse

# This parser will not throw when an argument is not recognized
class MyArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        pass