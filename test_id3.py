from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TCON, Frame

fn = "test.mp3"
mp3 = MP3(fn)
# print(mp3.tags)

f = TCON(encoding=3, text="Rock")
# f = Frame("TCON", test="Rock and Roll Frame")
mp3.tags.add(f)

mp3.tags.save(fn)
