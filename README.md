# Planetaryum

A Jupyter notebook gallery framework

## Design

- Readers: Storage -> notebooks

- Extractors: ipynb -> metadata + [html] + [ipynb]

- Back ends: extractor -> CouchDB

- Front ends: Gallery + search + notebooks + execute links + ...
  - JSON data + static html + SPA (PouchDB + Preact?)
  - CouchDB frontend

- Apps:
  - Folder/Git -> Extractor -> Static Website bundle
  - Serverless CouchDB website (no users)
  - Flask app + CouchDB back end
