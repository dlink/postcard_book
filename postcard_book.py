#!/usr/bin/env python

import os

from fpdf import FPDF

from odict import odict

IMAGE_DIR = '/data/afa_images'
SUPPORTED_EXTENSIONS = ['jpg', 'png']


class FilenameError(Exception): pass

class Book(object):

    def __init__(self):
        self.pdf = FPDF('L', 'cm', 'Letter')
        self.pdf.set_font('Arial', '', 16)

        #self.artists = self.getArtists

    def build(self):
        #for filename in self.getImageFilenames():
        #    self.addPage(filename)
        self.artists = self.getArtists()
        artist_keys = sorted(self.artists.keys())
        for artist in artist_keys:
            self.addPage(artist)
        self.pdf.output('book.pdf', 'F')

    def addPage(self, artist):
        self.pdf.add_page()
        images = self.artists[artist]['images']
        if images.front:
            self.pdf.image(IMAGE_DIR + '/' + images.front, 0, 0, 10)
        if images.back:
            self.pdf.image(IMAGE_DIR + '/' + images.back, 12, 0, 10)

    def getArtists(self):
        '''Return dictionary of artists data from
           - image files in IMAGE_DIR, and
           - artists.csv

        Data Structure:

        artists = {'amy_hughes': {'images': {'front': 'amy_hughes.jpg',
                                             'back': 'amy_hughes-b.jpg'},
                                  'name': 'Amy Hughes',
                                  'residence': 'White Plains, NY, USA'
                                  'website': 'blabla.com',
                                  }
                   'amy_hughes-2': {'images': {'front': 'amy_hughes-2.jpg',
                                               'back': 'amy_hughes-2b.jpg'},
                                    'name': 'Amy Hughes',
                                    'residence': 'White Plains, NY, USA'
                                    'website': 'blabla.com',
                                    }
                   }
        '''

        artists = odict()
        for n, filename in enumerate(os.listdir(IMAGE_DIR)):

            # separtate filename and extention:
            parts = filename.split('.')
            if len(parts) < 2:
                raise FilenameError('filename most one period: %s' % filename)
            elif len(parts) > 2:
                raise FilenameError('filename most have only one period: %s' %
                                  filename)

            # check file extension
            ext = parts[1]
            if ext not in SUPPORTED_EXTENSIONS:
                raise FilenameError('unrecognized extension: %s' % ext)

            # get name, and front or back
            parity = 'front'
            name = parts[0]
            if name.endswith('-b'):
                name = name[0:-2]
                parity = 'back'

            # init artist record if nec:
            if name not in artists:
                artists[name] = odict({'images': odict({'front': None,
                                                        'back': None})})

            # add filename
            artists[name]['images'][parity] = filename
    
        # check artists data and print warnings
        for artist, data in artists.items():
            if not data.images.front:
                print 'Warn: %s: No front image' % artist
            elif not data.images.back:
                print 'Warn: %s: No back image' % artist

        return artists

if __name__ == '__main__':
    Book().build()
    #for k, v in Book().getArtists().items():
    #    print k, v
