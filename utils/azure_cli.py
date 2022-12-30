from azure.cli.core import get_default_cli
from pprint import PrettyPrinter

class Azure_CLI(object):
    def __init__(self) -> None:
        self.cli = get_default_cli()
        self.pp = PrettyPrinter(2)
    
    def cli (self, args_rec: str):
        args = (args_rec + " --output none").split()
        self.cli.invoke(args)
        if self.cli.result.result:
            return self.cli.result.result
        elif self.cli.result.error:
            raise self.cli.result.error
        return True

    def print_cli (self, args_rec: str):
        args = (args_rec + " --output none").split()
        self.cli.invoke(args)
        if self.cli.result.result:
            self.pp.pprint(self.cli.result.result)
            return self.cli.result.result
        elif self.cli.result.error:
            raise self.cli.result.error
        return True