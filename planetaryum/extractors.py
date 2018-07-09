import json
from nbconvert import HTMLExporter

class Extractor():
    '''
    Extractors are callable objects that take a notebook in 
    (as a readable object) and return processed data.

    All extractors have a name by which they can be recognized
    in an aggregated output. If the name is omitted or None, the
    class name will be used as default.
    '''
    def __init__(self, name=None):
        self.name = self.__class__.__name__ if name is None else name

class JSONExtractor(Extractor):
    '''
    Parse the notebook as JSON data and return a Python object.
    '''
    
    def __call__(self, nb, name):
        return json.load(nb)

class MetadataExtractor(JSONExtractor):
    '''
    Parse the notebook and return the metadata.
    Optionally extract images from notebook and make 
    thumbnails.
    '''
    def __init__(self, name=None, thumbnails=False):
        super().__init__(name)
        self.thumbnails = thumbnails

    def __call__(self, nb, name):
        # TODO: extract thumbnails
        return super().__call__(nb, name)['metadata']
    
class BlobExtractor(Extractor):
    '''
    Return the notebook as raw bytes.
    '''

    def __call__(self, nb, name):
        return nb.read()
    
class HTMLExtractor(Extractor):
    '''
    Passes the notebook through nbconvert.HTMLExporter
    and yields the produced HTML
    plus metadata.
    '''
    
    def __init__(self, name=None, template_file=None):
        super().__init__(name)
        self.exporter = HTMLExporter()
        self.exporter.template_file = template_file or 'basic.tpl'
    
    def __call__(self, nb, name):
        html, meta = self.exporter.from_file(nb, resources={
            'filename': name,
            })
        meta['filename'] = name
        return {
            'meta': meta,
            'html': html,
            }


def extract(reader, extractors):
    '''
    An iterator that takes in a Reader and a list of extractors,
    applies each extractor to the notebooks in Reader, and returns
    the extracted data as a Python object, using the extractor names
    as keys.

    >>> list(extract(FolderReader('/home/jupyter'), [MetadataExtractor()]))
    [{'MetadataExtractor': {'kernelspec': {'display_name': 'Python 3',
        'language': 'python',
        'name': 'python3'},
       'language_info': {'codemirror_mode': {'name': 'ipython', 'version': 3},
        'file_extension': '.py',
        'mimetype': 'text/x-python',
        'name': 'python',
        'nbconvert_exporter': 'python',
        'pygments_lexer': 'ipython3',
        'version': '3.6.4'}},
      'name': 'example1'},
     {'MetadataExtractor': {'kernelspec': {'display_name': 'SageMath 8.2.beta5',
        'language': '',
        'name': 'sagemath'},
       'language_info': {'codemirror_mode': {'name': 'ipython', 'version': 2},
        'file_extension': '.py',
        'mimetype': 'text/x-python',
        'name': 'python',
        'nbconvert_exporter': 'python',
        'pygments_lexer': 'ipython2',
        'version': '2.7.14'}},
      'name': 'example2'}]
    '''
    for nb, name in reader:
        d = {}
        for e in extractors:
            with nb.open() as f:
                d[e.name] = e(f, name) 
        d['name'] = name
        yield d
