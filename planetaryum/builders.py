import json
from distutils.dir_util import copy_tree
from pathlib import Path
from . import extractors as ex

class Builder():
    '''
    Builders perform a build step to construct an App.
    
    They may be simple steps, such as copying the contents of a folder,
    or arbitrarily complex ones.

    Builders can be chained via the >> operator. 

    They are run by the run() method. run() takes an optional state argument (a dict),
    and is expect to return a state dict to pass to the next builder in the chain.
    '''
    def __rshift__(self, other):
        if isinstance(other, BuilderChain):
            return BuilderChain(self, *other.steps)
        elif isinstance(other, Builder):
            return BuilderChain(self, other)
        else:
            raise ValueError('Expected object of type Builder, found %s' % type(other))

class BuilderChain(Builder):
    '''
    A sequence of builder steps, executed sequentially.
    '''
    
    def __init__(self, *steps):
        self.steps = steps

    def run(self, state={}):
        for s in self.steps:
            state = s.run(state)
        return state

    def __rshift__(self, other):
        if isinstance(other, BuilderChain):
            return BuilderChain(*self.steps, *other.steps)
        elif isinstance(other, Builder):
            return BuilderChain(*self.steps, other)
        else:
            raise ValueError('Expected object of type Builder, found %s' % type(other))

class CopyTreeBuilder(Builder):
    '''
    Copies a filesystem tree from src to dst.
    '''
    
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    def run(self, state={}):
        copy_tree(self.src, self.dst)
        return state

class StaticHTMLBuilder(Builder):
    '''
    Build static HTML files from Jupyter notebooks
    '''

    def __init__(self, reader, out_dir, template_file=None):
        self.reader = reader
        self.out = Path(out_dir)
        self.extractors = [
            ex.MetadataExtractor('meta'),
            ex.HTMLExtractor('html', template_file=template_file),
            ]

    def run(self, state={}):
        # Write static notebooks
        nbs = self.out / 'notebooks'
        nbs.mkdir(parents=True, exist_ok=True)
        meta = []
        
        for i, data in enumerate(ex.extract(self.reader, self.extractors)):
            path = nbs / (data['name'] + '.html')
            path.write_text(data['html']['html'])
            
            meta.append({
                '_id' : 'notebook/%d/%s' % (i, data['name']),
                'name': data['name'],
                'path': str(path.relative_to(self.out)),
                'meta': data['meta'],
                })

        # Write metadata
        with (self.out / 'meta.json').open('w') as f:
            json.dump(meta, f)

        return state
    
