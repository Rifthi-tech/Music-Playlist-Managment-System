# Music Playlist Management System

A fully featured desktop music player built using Python, Tkinter, and Pygame.  
The application manages playlists using a Doubly Linked List ADT, supports ordered and shuffle playback, and provides a complete audio player interface.

---

## 🚀 Features
- Create and delete playlists  
- Add and remove songs (MP3, WAV, OGG, FLAC)  
- Ordered playback (queue mode)  
- Shuffle playback without repeating songs until all have been played  
- Play, pause, resume, stop, next, and previous controls  
- Volume control and Now Playing information  
- Automatic saving and loading of playlists using a `playlists.pkl` file  
- Handles missing song files with warnings  

---

## 🧠 Data Structures (ADTs)
The system uses several abstract data types:

1. **Doubly Linked List**  
   Used to store songs with previous/next pointers, allowing efficient insertion, removal, and traversal.

2. **Queue Behavior**  
   Enables sequential playback in ordered mode.

3. **Random Access for Shuffle Mode**  
   Maintains a shuffled copy of the playlist and tracks played songs to avoid repeats.

Each song node contains metadata such as file path, title, artist, album, and duration.

---

## 📐 Algorithm Overview

### Ordered Mode
- Locate the song in the `original_order` list  
- Swap with the previous or next item depending on direction  
- Rebuild the linked list  
- Keep the current song pointer active  

### Shuffle Mode
- Duplicate the song list  
- Randomize the order  
- Rebuild the linked list using the shuffled list  
- Track played songs to ensure all songs play once before repeating  

---

## 🖥️ User Interface
The UI includes:
- Playlist dropdown (create/delete)  
- Scrollable song list  
- Buttons to add and remove songs  
- Order and Shuffle toggle buttons  
- Playback controls: previous, play/pause, stop, next  
- Progress bar with elapsed and total time  
- Volume slider  
- Now Playing information area  

---

## 📦 Installation

### Requirements
- Python 3.8+  
- Pygame  
- Tkinter  

Install pygame using:

```bash
pip install pygame
