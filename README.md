v1.2.0 Discord Bot: Trobotsko

v1.2.0 Updates:

Trobotsko can now store, retrieve and delete files! See the following commands below about what is possible:

- Files
  - <delete-file deletes a file from both local storage and the remote db
  - <get-file specifically returns a files contents
  - <see-files displays information about all the files a particular user has stored
  - <store-file allows a user to store file(s) for later retrieval

- Minor tweaks / updates:
  - Fixed a bug where the song would suddenly stop playing due to improper streaming links in yt-dlp

v1.1.0 Updates:

Trobotsko can now play music! See the following commands below about what is possible:

- Songs
  - <add submits a song to the queue, will also play the song if a song is not playing
  - <clear clears the queue completely of all songs
  - <pause pauses the song that is currently playing
  - <play plays the song at the top of the queue, if a song is not playing
  - <remove removes a song from the queue, can specify which song by position, title or url
  - <reorder randomize the order of the queue, but the songs still play sequentially
  - <repeat toggles the song on or off repeat-mode
  - <resume unpauses the currently playing song, if possible
  - <see displays a list of the songs in the queue yet to be played
  - <shuffle puts the queue on shuffle mode, you never know which song might be played next!
  - <skip skips the currently playing song, if possible

Trobotsko can now store playlists and the user (you) can now play songs directly off saved playlists!

- Playlists
  - <add-song adds a song to a playlist
  - <create-pl creates an empty song playlist
  - <see-pl shows all playlists of the given user
  - <use-pl designates the bot to use a particular playlist as the song queue
  - <remove-song removes song from playlist, can be title or url
