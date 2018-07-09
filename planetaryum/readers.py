from pathlib import Path

class Reader():
    '''
    Readers are iterable objects yielding a collection
    of Jupyter notebooks as pairs (file-like-object, name).

    >>> list(FolderReader('/home/jupyter')
    [(PosixPath('/home/jupyter/example1.ipynb'), 'example1'),
     (PosixPath('/home/jupyter/example2.ipynb'), 'example2')]

    '''
    pass

class DirReader(Reader):
    '''
    Read all .ipynb from a directory
    '''
    
    def __init__(self, path):
        self.path = path
        self.nbs = Path(path).glob('*.ipynb')

    def __iter__(self):
        for nb in self.nbs:
            yield (nb, nb.stem)

class GitReader(Reader):
    '''
    Read all .ipynb from a git repo
    '''

    def __init__(self, repo):
        self.repo = repo

    def __iter__(self):
        pass
