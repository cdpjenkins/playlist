#!/usr/bin/env bb

(require '[babashka.fs :as fs])

(declare visit-dir)

(defn ls [dir pattern]
  (->>
   (fs/list-dir dir pattern)
   (map str)
   (sort)))

(defn files-in-playlist [playlist-file dir]
  (->> playlist-file
       slurp
       str/split-lines
       (map #(str dir "/" %))))

(defn playlist-contents-for-dir [dir]
  (let [playlists (map str (fs/list-dir dir "*.m3u"))
        playlist-contents (mapcat #(files-in-playlist % dir) playlists)]
    playlist-contents))

(defn music-files-in-dir [dir]
  (concat
   (ls dir "*.mp3")
   (ls dir "*.ogg")
   (ls dir "*.m4a")))

(defn music-files-in-subdirs [dir]
  (->> 
   (ls dir "*")
   (filter fs/directory?)
   (mapcat visit-dir)))

(defn visit-dir [dir]
  (concat
   (playlist-contents-for-dir dir)
   (music-files-in-dir dir)
   (music-files-in-subdirs dir)))

(doseq [line (visit-dir ".")]
  (println line))





