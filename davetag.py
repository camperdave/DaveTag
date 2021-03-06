#    DaveTag - automatically move music files to where they belong, based on their metadata
#    Copyright (C) 2011  David Lee (aka camperdave)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import glob
import sys
import codecs
import shutil

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4



def process_dir(dir, copyTo):
    dir = unicode(dir)
    print(u"dir: " + dir)
    
    for root, dirs, files in os.walk(dir):
        for file in files:
            ext = os.path.splitext(file)
            if ext:
                ext = ext[1].lower()
                infile = os.path.join(root, file)
                if ext == ".mp3":
                    audio = MP3(infile, ID3=EasyID3)
                    process_file(audio, ".mp3", copyTo, infile)
                if ext == ".m4a":
                    audio = MP4(infile)
                    process_file(audio, ".m4a", copyTo, infile)
        
def process_file(audio, ext, copyTo, origFile):
    try:
        origFile = unicode(origFile)
        print(u"Processing: " + origFile)
        artist = audio.get("albumartistsort", {})
        if not artist:
            artist = audio.get("artist", {})
            if not artist:
                artist = audio.get('aART', {})
                if not artist:
                    artist = audio.get('\xa9ART', {})
                    if not artist:
                        artist = ""

        if isinstance(artist, str) or isinstance(artist, unicode):
            artist = unicode(artist.strip())
        else:
            artist = unicode(artist[0].strip())
        
        album = audio.get("album", {})
        if not album:
            album = audio.get('\xa9alb', {})
            if not album:
                album = ""

        if isinstance(album, str) or isinstance(album, unicode):
            album = unicode(album.strip())
        else:
            album = unicode(album[0].strip())
        
        title = audio.get("title", {})
        if not title:
            title = audio.get('\xa9nam', {})
            if not title:
                title = ""

        if isinstance(title, str) or isinstance(title, unicode):
            title = unicode(title.strip())
        else:
            title = unicode(title[0].strip())
        
        tracknum = audio.get("tracknumber", {})
        if not tracknum:
            tracknum = audio.get("trkn", {})
            if not tracknum:
                tracknum = ""

        if isinstance(tracknum, str) or isinstance(tracknum, unicode):
            tracknum = unicode(str(tracknum).strip())
        else:
            tracknum = unicode(str(tracknum[0]).strip())
        
        discnum = audio.get("discnubmer", {})
        if not discnum:
            discnum = audio.get("disk", {})
            if not discnum:
                discnum = ""
        
        if isinstance(discnum, str) or isinstance(discnum, unicode):
            discnum = unicode(str(discnum).strip())
        else:
            discnum = unicode(str(discnum[0]).strip())
        
        filename = unicode("")
        if discnum:
            filename += discnum + u"-"
        if tracknum:
            if tracknum.count("/") > 0:
                filename += tracknum[:tracknum.index("/")]
            else:
                filename += tracknum
            
            filename += u" "
        if title:
            filename += title + ext

        if filename == u"":
            # Fall back on original file name!
            filename = os.path.basename(origFile)

        bad_chars = {"/", "\\", ":", ">", "<", "*", "?", "\"", "|"}
        
        for bad in bad_chars:
            filename = filename.replace(bad,"_")
            artist = artist.replace(bad, "_")
            album = album.replace(bad, "_")
        

        # Folders can't end in .
        if artist[-1:] == '.':
            artist += u"_"

        if album[-1:] == '.':
            album += u"_"
        
        finalPath = os.path.join(copyTo, artist, album, filename)
        
        if finalPath == origFile:
            print("File " + finalPath + " is correctly placed!")
        else:
            print(u"Moving file from " + origFile + u" to " + finalPath)
            if os.path.isfile(finalPath):
                print("Error: would overwrite file!")
            else:
                if not os.path.isdir(os.path.split(finalPath)[0]):
                    os.makedirs(os.path.split(finalPath)[0])
                shutil.move(origFile, finalPath)
                print("File successfully moved to " + finalPath)
        
        
        
        
        print("###################################")
        
        
    except UnicodeEncodeError:
        print("Had trouble with a UnicodeEncodeError!")
        print(origFile.encode("utf-8"))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]      
        print(exc_type, fname, exc_tb.tb_lineno)
        raw_input("Press Enter to continue...")                     # Change to input(...) if on python3

# See http://kbyanc.blogspot.com/2007/04/python-printing-unicode.html
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

if len(sys.argv) == 2:    
    process_dir(sys.argv[1], u"H:\\Music")
elif len(sys.argv) >= 3:
    process_dir(sys.argv[1], sys.argv[2])
else:
    process_dir(os.getcwdu(), u"H:\\Music")
