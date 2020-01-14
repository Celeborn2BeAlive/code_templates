import argparse

# This parser will not throw when an argument is not recognized
class MyArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        pass

parser = argparse.ArgumentParser()
# This method allows to parse declared argurmants in args and to keep the remainings in unknown instead of raising an error
args, unknown = parser.parse_known_args()