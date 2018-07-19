"""Usage: main.py  <target> [<pages>]

Arguments:
  target    The target organization name you want to collect intel
  pageNb    The number of Google results pages you want to scrap

"""
from docopt import docopt
from schema import Schema, And, Use, SchemaError
from modules.core.Utils import Oss117
from modules.scenarios.Scenario1 import Scenario1

arguments = docopt(__doc__)
schema = Schema(
    {
        '<target>': And(str, lambda s: len(s) >= 3, Use(str.lower)),
        '<pages>': And(Use(int), lambda n: 1 <= n <= 10)
    }
)
try:
    args = schema.validate(arguments)
except SchemaError as e:
    exit(e)
arg_target = args['<target>']
arg_pages = args['<pages>']

Oss117.print_banner()


s = Scenario1()
s.run(arg_target, arg_pages)
