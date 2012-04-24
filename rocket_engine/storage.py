from django.core.urlresolvers import reverse
from django.core.files.storage import Storage

from google.appengine.ext import blobstore
from google.appengine.api import files
import urllib

class BlobstoreStorage(Storage):

    def save(self, name, content):
        file_name = files.blobstore.create(
            mime_type='application/octet-stream',
            _blobinfo_uploaded_filename=name
        )
        with files.open(file_name, 'a') as f:
            f.write(content.read())
        files.finalize(file_name)
        return files.blobstore.get_blob_key(file_name)

    def _open(self, blobstore_key, mode='rb'):
        blobstore_file = blobstore.BlobReader(blobstore_key)
        blobstore_info = blobstore.BlobInfo.get(blobstore_key)
        blobstore_file.name = blobstore_info.filename.split('/')[-1]
        return blobstore_file

    def exists(self, blobstore_key):
        return True if blobstore.BlobInfo.get(blobstore_key) else False

    def size(self, blobstore_key):
        blobstore_key = str(urllib.unquote(blobstore_key))
        blob_info = blobstore.BlobInfo.get(blobstore_key)
        return blob_info.size

    def url(self, blobstore_key):
        return reverse(
            'rocket_engine.views.file_serve',
            kwargs={'blobstore_key': blobstore_key}
        )
