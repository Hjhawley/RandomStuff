from libpytunes import Library

l = Library("C:/Users/hjhaw/Music/iTunes/iTunes Music Library.xml")

for id, song in l.songs.items():
    if song and song.rating:
        if song.rating > 80:
            print(song.name, song.rating)

playlists=l.getPlaylistNames()

for song in l.getPlaylist(playlists[0]).tracks:
	print("[{t}] {a} - {n}".format(t=song.track_number, a=song.artist, n=song.name))