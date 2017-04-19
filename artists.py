import csv

DATAFILE = 'art_for_aleppo_artists.csv'

class Artists(object):

    def __init__(self):
        self._readData()

    def _readData(self):
        self.data = {}
        reader = csv.reader(open(DATAFILE, 'r'))
        for i, row in enumerate(reader):
            if i == 0:
                header = [x.lower() for x in row]
                continue
            key = row[2]
            self.data[key] = {}
            for i, h in enumerate(header):
                self.data[key][h] = row[i]
            self.data[key]['location'] = self._getLocation(self.data[key])

    def _getLocation(self, artist):
        location = ', '.join([artist['city'],
                              artist['state'],
                              artist['country']])
        return location.replace(', ,', ',')

    def getArtist(self, key):
        return self.data[key]
        
if __name__ == '__main__':
    artists = Artists()
    
    # one artist
    artist = artists.getArtist('Linda Karlsberg')
    for k, v in artist.items():
        print "%s: %s" % (k,v)

    # see all locations and website
    for k, v in artists.data.items():
        print "%s: %s - %s" % (k, v['location'], v['website'])