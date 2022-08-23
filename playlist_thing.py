from libpytunes import Library

l = Library("C:/Users/hjhaw\Music/iTunes/iTunes Music Library.xml")
funeral = Library.Playlist("C:/Users/hjhaw/OneDrive/Desktop/Python/libpytunes-master/funeral.xml")

def fiveStars():
    for id, song in l.songs.items():
        if song and song.rating:
            if song.rating > 80:
                print(song.name, song.rating)

def playlistNames():
    playlists=l.getPlaylistNames()
    for song in l.getPlaylist(playlists[0]).tracks:
        print("[{t}] {a} - {n}".format(t=song.track_number, a=song.artist, n=song.name))

def plTest():
    for id, song in funeral.songs.items():
        if song and song.comments:
            if song.comments == "test":
                #song.comments = "test 2"
                print(song.name, song.comments)

plTest()

'''
with open(itunesxml, 'rb') as f:
            self.il = plistlib.load(f)
'''