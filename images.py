#!/usr/bin/env python

import PIL.Image, PIL.ExifTags

class Image(object):

    def __init__(self, filename):
        self.filename = filename

    @property
    def exif(self):
        '''Open image with PIL
           Return exif data as a dict with human tag names

           Uses lazyloading
        '''
        if '_exif' not in self.__dict__:
            img = PIL.Image.open(self.filename)
            meta = img._getexif()
            if meta:
                self._exif = {PIL.ExifTags.TAGS[k]: v \
                                  for k, v in meta.items() \
                                  if k in PIL.ExifTags.TAGS }
            else:
                self._exif = {}
        return self._exif

    @property
    def width(self):
        return self.exif.get('ExifImageWidth', None)
    @property
    def height(self):
        return self.exif.get('ExifImageHeight', None)
    @property
    def orientation(self):
        return 'portrait' if self.width < self.height else 'landscape'

if __name__ == '__main__':

    # pass a filename on command line - show some stats
    import sys
    if len(sys.argv) < 2:
        print 'Must specify image filename'
        sys.exit(1)
    filename = sys.argv[1]
    image = Image(filename)
    print image.filename, 'w:', image.width, 'h:', image.height, \
        'o:', image.orientation
