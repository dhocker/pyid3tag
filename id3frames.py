# coding: utf-8
#
# Copyright © 2019 Dave Hocker (email: AtHomeX10@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the LICENSE file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program (the LICENSE file).  If not, see <http://www.gnu.org/licenses/>.
#

from collections import OrderedDict
import mutagen.id3

def create_comm(tag, value):
    parts = tag.split(':')
    return mutagen.id3.COMM(desc=parts[1], lang=parts[2], text=value)

def create_talb(tag, value):
    return mutagen.id3.TALB(text=value)

def create_tcon(tag, value):
    return mutagen.id3.TCON(text=value)

def create_tcop(tag, value):
    return mutagen.id3.TCOP(text=value)

def create_tdrc(tag, value):
    return mutagen.id3.TDRC(text=value)

def create_tbpm(tag, value):
    return mutagen.id3.TBPM(text=value)

def create_tit1(tag, value):
    return mutagen.id3.TIT1(text=value)

def create_tit2(tag, value):
    return mutagen.id3.TIT2(text=value)

def create_tit3(tag, value):
    return mutagen.id3.TIT3(text=value)

def create_tpe1(tag, value):
    return mutagen.id3.TPE1(text=value)

def create_tpe2(tag, value):
    return mutagen.id3.TPE2(text=value)

def create_tpe3(tag, value):
    return mutagen.id3.TPE3(text=value)

def create_tpe4(tag, value):
    return mutagen.id3.TPE4(text=value)

def create_tpos(tag, value):
    return mutagen.id3.TPOS(text=value)

def create_trck(tag, value):
    return mutagen.id3.TRCK(text=value)

def _not_implemented(tag, value):
    return None

# Frame creators for most common tags
_frame_creators = OrderedDict({
    "COMM": create_comm,
    "TALB": create_talb,
    "TBPM": create_tbpm,
    "TCON": create_tcon,
    "TCOP": create_tcop,
    "TDAT": _not_implemented,
    "TDRC": create_tdrc,
    "TFLT": _not_implemented,
    "TIT1": create_tit1,
    "TIT2": create_tit2,
    "TIT3": create_tit3,
    "TPE1": create_tpe1,
    "TPE2": create_tpe2,
    "TPE3": create_tpe3,
    "TPE4": create_tpe4,
    "TPOS": create_tpos,
    "TRCK": create_trck,
})

# Tooltips for most common tags
_frame_tooltips = {
    "COMM": "Comment",
    "TALB": "Album title",
    "TBPM": "Tempo (beats per minute)",
    "TCON": "Content type",
    "TCOP": "Copyright message",
    "TDAT": "Date",
    "TDRC": "Recording time",
    "TFLT": "File type",
    "TIT1": "Content group description",
    "TIT2": "Title/songname/content description",
    "TIT3": "Subtitle/description refinement",
    "TPE1": "Lead performer/soloist(s)",
    "TPE2": "Band/orchestra/accompaniment",
    "TPE3": "Conductor/performer refinement",
    "TPE4": "Interpreted, remixed, or otherwise modified by",
    "TPOS": "Part of set",
    "TRCK": "Track number/position in set",
}

def create(tag, value):
    tag4 = tag[0:4]
    if tag4 in _frame_creators.keys():
        return _frame_creators[tag4](tag, value)
    return None

def frame_keys():
    """
    Return a simple list of all of the available ID3 tag keys
    :return: A list of keys.
    """
    return [k for k in _frame_creators.keys()]

def frame_tooltip(tag):
    tag4 = tag[0:4]
    if tag4 in _frame_tooltips.keys():
        return _frame_tooltips[tag4]
    return "Unavailable"
