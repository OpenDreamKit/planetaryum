"""Usage: planetaryum [--help] [<command>] [<args>...]

Options:
   -h, --help  Print this help message

Commands:
   help    show help on a command
   static  generate static website
"""

from docopt import docopt
from subprocess import call

def run_sub(cmd, args):
    if cmd == 'static':
        from .apps import static_gen
        return static_gen.cli(docopt(static_gen.cli.__doc__, argv=args))
    else:
        raise ValueError('Unknown command')

def main():
    args = docopt(__doc__, help=False, options_first=True)
    
    if args['<command>'] == 'help':
        args['--help'] = True
        args['<command>'] = args['<args>'][0] if args['<args>'] else None
        
    if args['--help']:
        if args['<command>']:
            run_sub(args['<command>'], ['--help'])
        else:
            exit(__doc__)
    else:
        argv = [args['<command>']] + args['<args>']
        try:
            run_sub(args['<command>'], argv)
        except ValueError:
            exit("%r is not a planetaryum command. See 'planetaryum help'." % args['<command>'])
