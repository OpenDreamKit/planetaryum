from ..builders import StaticHTMLBuilder
from ..readers import DirReader
from ..builders import CopyTreeBuilder, CopyIPynbBuilder
from pathlib import Path

class StaticGen():
    def __init__(self, reader, out_dir, builder, cmdargs={}, template_file=None):
        self.builder = StaticHTMLBuilder(reader, out_dir, cmdargs, template_file,
                                             thumbnails=True, write_css=True) >> builder
        
    def build(self):
        self.builder.run()

def cli(args):
    """Usage: planetaryum static [options] [--] [<front-end-args>...]

Options:
   -h, --help                  Show this help message
   -i <uri>, --input=<uri>     URI containing the Jupyter notebooks
                               to process [default: .].
   -o <path>, --output=<path>  path to a folder where to write the
                               built website [default: _site]

Front end arguments are passed as is to the front-end.
"""
    indir, outdir = args['--input'], args['--output']
    reader1 = DirReader(indir)
    reader2 = DirReader(indir)
    builder = (CopyTreeBuilder(Path(__file__).parent.parent / 'front_ends/static_gen', outdir)
                   >> CopyIPynbBuilder(reader1, Path(outdir) / 'ipynbs'))
    StaticGen(reader2, outdir, builder, cmdargs=args['<front-end-args>']).build()
