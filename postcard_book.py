#!/usr/bin/env python

import os

from fpdf import FPDF

from odict import odict
from artists import Artists, ArtistNotFound
from images import Image

BLURB_BOOK_8X10_LANDSCAPE_DIM = [8.250, 9.625] # height, width
BOOK_FILENAME = 'book2.pdf'

IMAGE_DIR = '/data/afa_images'
SUPPORTED_EXTENSIONS = ['jpg', 'png']
NON_POSTCARD_FILES = ['cover_art.jpg', '.DS_Store']

# HACK - need to set this manually
LAST_PAGE = 10

class FilenameError(Exception): pass

class PDF(FPDF):

    def footer(self):
        self.set_xy(0.5, 3.0)
        self.set_font('DejaVu', '', 8)
        self.set_text_color(169,169,169) # DarkGrey
        if self.page_no() > 1 and self.page_no()-1 < LAST_PAGE:
            self.cell(0, 10, str(self.page_no()-1), 0, 0, 'C')

class Book(object):

    def __init__(self):
        self.pdf = PDF('L', 'in', BLURB_BOOK_8X10_LANDSCAPE_DIM)
        self.pdf.alias_nb_pages()
        self.pdf.add_font('DejaVu', '', '/Applications/OpenOffice.org.app/Contents/basis-link/share/fonts/truetype/DejaVuSansCondensed.ttf', uni=True)
        self.pdf.set_font('DejaVu', '', 12)

        self.pdf.set_text_color(169,169,169) # DarkGrey
        self.artists = Artists()

    def build(self):
        '''Build Book
           Creates PDF file, BOOK_FILENAME
        '''
        self.addFrontCover()
        self.addIntro()

        self.postcards = self.getPostcards()
        postcard_keys = sorted(self.postcards.keys())
        for i, postcard_key in enumerate(postcard_keys):
            print i, postcard_key
            self.addPage(self.postcards[postcard_key])
            if i > 5:
                break

        self.addBackCover()

        self.pdf.output(BOOK_FILENAME, 'F')

    def addFrontCover(self):
        self.pdf.add_page()
        self.pdf.image(IMAGE_DIR + '/' + 'cover_art.jpg', 2, 1, 6)

        self.pdf.set_font('DejaVu', '', 32)
        self.pdf.set_xy(2.5, 5.25)
        self.pdf.cell(0, 0, 'Postcards to humanity')

        self.pdf.set_font('DejaVu', '', 18)
        self.pdf.set_xy(2, 6.25)
        self.pdf.cell(0, 0,
                      'In response to the atrocities in Aleppo, we have made')
        self.pdf.set_xy(2, 6.65)
        self.pdf.cell(0, 0, 
                      '    a call to artists from around the world to respond.'
                      )
    def addBackCover(self):
        'donna_marie' ' -b'
        'kerry mcaleer'
        'sheilah-b'
        'mj-bono'
        self.pdf.add_page()
        self.pdf.image(IMAGE_DIR + '/' + 'Donna_Marie_Fischer.jpg',
                       1.25, 1.25, 3)
        self.pdf.image(IMAGE_DIR + '/' + 'MJ_Bono.jpg',
                       5, 1.25, 3)
        #self.pdf.image(IMAGE_DIR + '/' + 'Sheilah_Rechtschaffer4-b.jpg',
        #               1.25, 4.25, 3)
        self.pdf.image(IMAGE_DIR + '/' + 'Sheilah_Rechtschaffer2-b.jpg',
                       1.25, 4.25, 3)
        self.pdf.image(IMAGE_DIR + '/' + 'Naomi_Genen2.jpg',
                       5, 4.40, 3)

        self.pdf.set_xy(4, 7.0)
        self.pdf.cell(0, 0, 'Art for Aleppo')


    def addPage(self, postcard):
        #print 'p:', postcard
        self.pdf.set_font('DejaVu', '', 12)
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
                           
            if filename in NON_POSTCARD_FILES:
                continue

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

    def addIntro(self):
        self.pdf.set_font('DejaVu', '', 12)
        self.pdf.add_page()
        self.pdf.set_xy(1, 1)
        self.pdf.multi_cell(0, .25, '''
The battle for Aleppo is marked by widespread violence against
civilians, repeated targeting of hospitals and schools, and
indiscriminate aerial strikes and shelling against civilian
areas. Hundreds of thousands of residents have been displaced by the
fighting and efforts to provide aid to civilians or facilitate
evacuation is routinely disrupted. After four years of fighting, the
battle represents one of the longest sieges in modern warfare. The
Syrian Observatory for Human Rights (SOHR) registered that in 1612
days of fighting 21,452 civilians died. Among them were 5,261 children
under the age of 18. We want to help and so can you! The Art For
Aleppo project gives visual artists an outlet to express themselves
around the Syrian crisis and help raise awareness and funds to aid in
the effort to provide Syrian children emergency care, food and
water. The Art For Aleppo project also gives non artists a chance to
help in three ways, through the purchase of art, through the purchase
of the catalog book of participating artists or through a direct
monetary donation in any amount. You may donate by going to
http://artforaleppo.org/donate.py

100% of your purchases or donations are tax deductible. All purchases
and donations are made directly to save the children Syria. We at "Art
For Aleppo" project won't take a single penny. Artwork will be
displayed at Catalyst Gallery 137 Main Street, Beacon NY on April 22nd
and will continue to be available for purchase online. The catalog
book of participating artists images will be available online with
blurb.com titled "Art For Aleppo" beginning on April 20th. Blurb is a
self publishing on demand book forum online so there is never a waste
of paper or upfront costs for Art For Aleppo. This allows us as
artists in this project to create without spending donations on
production or administration. All monies go directly to Save the
Children Syria.

April 19, 2017


The Art for Aleppo Team - Cold Spring, NY, USA

Russ Ritell - www.russritell.com
Carla Goldberg -  www.carlagoldberg.com
David Link - www.davidlinkart.com
''')
            
if __name__ == '__main__':
    Book().build()
    #for k, v in Book().getPostcards().items():
    #    print k, v
