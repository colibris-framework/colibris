
import argparse


class BaseCommand:
    def __init__(self, args):
        self.args = args
        self.parser = argparse.ArgumentParser()
        self.add_arguments(self.parser)

    def initialize(self):
        pass

    def run(self):
        self.initialize()
        options = self.parser.parse_args(self.args)
        self.execute(options)

    def add_arguments(self, parser):
        pass

    def execute(self, options):
        raise NotImplementedError

    @classmethod
    def get_name(cls):
        return cls.__name__[0:-7].lower()
