
# Ardour Lua Scripts (for Ardour v7)


For LUA Scrips, put the .lua files in ~/.config/ardour7/scripts/ folder.

A quick screencast for what the script does:

https://youtu.be/1X1beUfKZak


For more information: 
https://discourse.ardour.org/t/export-import-regions-between-different-sessions-projects/108147


LIMITATIONS:

- Works only for one audio track a time. Mono or Stereo channels are supported.
- Since the exported file location is a Linux path (/tmp/mb_ardour.tsv), may not work on Windows. (for now). 

NOTES:
Developed / Tested on Ubuntu 22.04 with Ardour 7.3.0



# ardour-playlist-copy (Python Script) (Tested with Ardour v6)
Copy Ardour playlists between sessions.

USAGE:

python3 ardour_copy_playlist_between_projects.py "SourceProject.ardour" "DestinationProject.ardour"
