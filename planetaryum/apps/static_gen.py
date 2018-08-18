from ..builders import StaticHTMLBuilder
from ..readers import DirReader
from ..builders import CopyTreeBuilder
from pathlib import Path

class StaticGen():
    def __init__(self, reader, out_dir, builder, template_file=None):
        self.builder = StaticHTMLBuilder(reader, out_dir, template_file,
                                             thumbnails=True, write_css=True) >> builder
        
    def build(self):
        self.builder.run()

def cli(args):
    """Usage: planetaryum static [options]

Options:
   -h, --help                  Show this help message
   -i <uri>, --input=<uri>     URI containing the Jupyter notebooks
                               to process [default: .].
   -o <path>, --output=<path>  path to a folder where to write the
                               built website [default: _site]
"""
    indir, outdir = args['--input'], args['--output']
    reader = DirReader(indir)
    builder = CopyTreeBuilder(Path(__file__).parent.parent / 'front_ends/static_gen',
                                  outdir)
    StaticGen(reader, outdir, builder).build()
