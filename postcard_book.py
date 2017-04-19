#!/usr/bin/env python

import os

from fpdf import FPDF

from odict import odict
from artists import Artists, ArtistNotFound
from images import Image

BLURB_BOOK_8X10_LANDSCAPE_DIM = [8.250, 9.625] # height, width
FONT = 'Arial'
BOOK_FILENAME = 'book.pdf'

IMAGE_DIR = '/data/afa_images'
SUPPORTED_EXTENSIONS = ['jpg', 'png']

class FilenameError(Exception): pass

class Book(object):

    def __init__(self):
        self.pdf = FPDF('L', 'in', BLURB_BOOK_8X10_LANDSCAPE_DIM)
        self.pdf.set_font(FONT, '', 12)
        self.pdf.set_text_color(169,169,169) # DarkGrey
        self.artists = Artists()

    def build(self):
        '''Build Book
           Creates PDF file, BOOK_FILENAME
        '''
        self.postcards = self.getPostcards()
        postcard_keys = sorted(self.postcards.keys())
        for i, postcard_key in enumerate(postcard_keys):
            print i, postcard_key
            self.addPage(self.postcards[postcard_key])
            #if i > 5:
            #    break
        self.pdf.output(BOOK_FILENAME, 'F')

    def addPage(self, postcard):
        #print 'p:', postcard
        if postcard.files.front is None:
            print 'skipping %s: no front' % postcard.name
            return

        if Image(IMAGE_DIR + '/' + postcard.files.front).orientation \
                == 'landscape':
            return self.addPage_landscape(postcard)
        else:
            return self.addPage_portrait(postcard)

    def addPage_landscape(self, postcard):
        self.pdf.add_page()
        if postcard.files.front:
            self.pdf.image(IMAGE_DIR + '/' + postcard.files.front, 1, .75, 4.5)

        if postcard.files.back:
            self.pdf.image(IMAGE_DIR + '/' + postcard.files.back, 1, 4.50, 4.5)

        self.place_text(6, 3.75, postcard)


    def addPage_portrait(self, postcard):
        self.pdf.add_page()
        if postcard.files.front:
            self.pdf.image(IMAGE_DIR + '/' + postcard.files.front, 1.5, 1, 3)

        if postcard.files.back:
            self.pdf.image(IMAGE_DIR + '/' + postcard.files.back, 5.25, 1, 3)

        self.place_text(4, 6, postcard)

    def place_text(self, x, y, postcard):
        try:
            artist = self.artists.getArtist(postcard['name'])
        except ArtistNotFound, e:
            print 'Failed to lookup artist: %s' % postcard['name']
            artist = Artists.UNKNOWN_ARTIST
            artist['name'] = postcard['name']

        text = [artist['name'],
                artist['location'],
                artist['website']]
        for t in text:
            self.pdf.set_xy(x, y)
            self.pdf.cell(0, 0, t)
            y += 0.25

    def getPostcards(self):
        '''Return dictionary of postcard data from
           - image files in IMAGE_DIR, and
           - artists.csv

        Data Structure:

        postcard = {'amy_hughes': {'files': {'front': 'amy_hughes.jpg',
                                             'back': 'amy_hughes-b.jpg'},
                                  'name': 'Amy Hughes',
                                  'residence': 'White Plains, NY, USA'
                                  'website': 'blabla.com',
                                  }
                   'amy_hughes-2': {'files': {'front': 'amy_hughes-2.jpg',
                                               'back': 'amy_hughes-2b.jpg'},
                                    'name': 'Amy Hughes',
                                    'residence': 'White Plains, NY, USA'
                                    'website': 'blabla.com',
                                    }
                   }
        '''

        postcards = odict()
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

            # get key, `name, and front or back
            parity = 'front'
            key = parts[0]
            if key.endswith('-b'):
                key = key[0:-2]
                parity = 'back'
            name = key.replace('_', ' ')
            if name[-1] in map(str, range(1,10)):
                name = name[0:-1]
            # init postcard record if nec:
            if key not in postcards:
                postcards[key] = odict({'name': name,
                                        'files': odict({'front': None,
                                                        'back': None})})

            # add filename
            postcards[key]['files'][parity] = filename
    
        # check postcards data and print warnings
        for postcard, data in postcards.items():
            if not data.files.front:
                print 'Warn: %s: No front image' % postcard
            elif not data.files.back:
                print 'Warn: %s: No back image' % postcard

        return postcards

if __name__ == '__main__':
    Book().build()
    #for k, v in Book().getPostcards().items():
    #    print k, v
