import os
import glob
import sys

from functools import reduce

def files(pattern):
    filenames = glob.glob(pattern)
    filenames.sort()
    return filenames

class Playlist:
    def __init__(self, dir="."):
        self.list = []
        self.file_set = set([])
        self.music_file_types = ["mp3", "ogg", "m4a", "AAC"]
        self.process_dir(dir)
    def process_dir(self, dir):
        # Process any playlists in the dir first
        for l in files("%s/*.m3u" % dir):
            self.process_playlist(dir, l)
        # Next process any music files in the dir
        self.add_files(reduce(list.__add__, \
              [files("%s/*.%s"%(dir, x)) for x in self.music_file_types]))
        # Finally process any subdirs
        for subdir in files("%s/*" % dir): self.process_dir(subdir)
    def process_playlist(self, dir, filename):
        with open(filename) as fd:
            self.add_files(["%s/%s" % (dir, f) for f in fd])
    def add_files(self, files):
        """Given a list of files, add to our playlist any files that are not
        already in the playlist"""
        for filename in [f.rstrip() for f in files]:
            if filename not in self.file_set:
                self.list.append(filename)
                self.file_set.add(filename)
    def write_playlist(self):
        for item in self.list: print(item.replace("/c/", "C:/", 1))

if __name__=='__main__':
    playlist = Playlist(".")
    playlist.write_playlist()

