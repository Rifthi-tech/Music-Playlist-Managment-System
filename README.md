# Music Playlist Management System

A fully‑featured desktop music player built using **Python**, **Tkinter**, and **Pygame**.  
The application manages playlists using a **Doubly Linked List ADT**, supports **ordered** and **true shuffle playback**, and provides a complete audio player GUI. [1](https://bcasac-my.sharepoint.com/personal/1030581_bcas_ac/_layouts/15/Doc.aspx?sourcedoc=%7B73FDF649-D960-47B1-9F20-09645BDFFE07%7D&file=Music%20Playlist%20Management%20System.pptx&action=edit&mobileredirect=true)[2](https://bcasac-my.sharepoint.com/personal/1030581_bcas_ac/Documents/Microsoft%20Copilot%20Chat%20Files/Music%20Playlist%20coding.txt)

---

## 🚀 Features
- Create and delete playlists. [1](https://bcasac-my.sharepoint.com/personal/1030581_bcas_ac/_layouts/15/Doc.aspx?sourcedoc=%7B73FDF649-D960-47B1-9F20-09645BDFFE07%7D&file=Music%20Playlist%20Management%20System.pptx&action=edit&mobileredirect=true)  
- Add and remove songs (MP3, WAV, OGG, FLAC). [2](https://bcasac-my.sharepoint.com/personal/1030581_bcas_ac/Documents/Microsoft%20Copilot%20Chat%20Files/Music%20Playlist%20coding.txt)  
- Ordered playback (queue mode). [1](https://bcasac-my.sharepoint.com/personal/1030581_bcas_ac/_layouts/15/Doc.aspx?sourcedoc=%7B73FDF649-D960-47B1-9F20-09645BDFFE07%7D&file=Music%20Playlist%20Management%20System.pptx&action=edit&mobileredirect=true)  
- True shuffle playback without repeats until all songs are played. [1](https://bcasac-my.sharepoint.com/personal/1030581_bcas_ac/_layouts/15/Doc.aspx?sourcedoc=%7B73FDF649-D960-47B1-9F20-09645BDFFE07%7D&file=Music%20Playlist%20Management%20System.pptx&action=edit&mobileredirect=true)  
- Play, pause, resume, stop, next, and previous controls. [2](https://bcasac-my.sharepoint.com/personal/1030581_bcas_ac/Documents/Microsoft%20Copilot%20Chat%20Files/Music%20Playlist%20coding.txt)  
- Volume control & now‑playing information. [2](https://bcasac-my.sharepoint.com/personal/1030581_bcas_ac/Documents/Microsoft%20Copilot%20Chat%20Files/Music%20Playlist%20coding.txt)  
- Automatic saving & loading of playlists via `playlists.pkl`. [1](https://bcasac-my.sharepoint.com/personal/1030581_bcas_ac/_layouts/15/Doc.aspx?sourcedoc=%7B73FDF649-D960-47B1-9F20-09645BDFFE07%7D&file=Music%20Playlist%20Management%20System.pptx&action=edit&mobileredirect=true)[2](https://bcasac-my.sharepoint.com/personal/1030581_bcas_ac/Documents/Microsoft%20Copilot%20Chat%20Files/Music%20Playlist%20coding.txt)  
- Handles missing song files gracefully with warnings. [1](https://bcasac-my.sharepoint.com/personal/1030581_bcas_ac/_layouts/15/Doc.aspx?sourcedoc=%7B73FDF649-D960-47B1-9F20-09645BDFFE07%7D&file=Music%20Playlist%20Management%20System.pptx&action=edit&mobileredirect=true)  

---

## 🧠 Data Structures (ADTs)
The app uses several abstract data types:  
1. **Doubly Linked List** for playlist navigation (prev/next). [1](https://bcasac-my.sharepoint.com/personal/1030581_bcas_ac/_layouts/15/Doc.aspx?sourcedoc=%7B73FDF649-D960-47B1-9F20-09645BDFFE07%7D&file=Music%20Playlist%20Management%20System.pptx&action=edit&mobileredirect=true)  
2. **Queue behavior** for ordered playback. [1](https://bcasac-my.sharepoint.com/personal/1030581_bcas_ac/_layouts/15/Doc.aspx?sourcedoc=%7B73FDF649-D960-47B1-9F20-09645BDFFE07%7D&file=Music%20Playlist%20Management%20System.pptx&action=edit&mobileredirect=true)  
3. **Random access** for shuffle mode using a non‑repeating shuffle list. [1](https://bcasac-my.sharepoint.com/personal/1030581_bcas_ac/_layouts/15/Doc.aspx?sourcedoc=%7B73FDF649-D960-47B1-9F20-09645BDFFE07%7D&file=Music%20Playlist%20Management%20System.pptx&action=edit&mobileredirect=true)  

Each song is stored as a node containing metadata, allowing efficient O(1) insert, delete, and traversal. [2](https://bcasac-my.sharepoint.com/personal/1030581_bcas_ac/Documents/Microsoft%20Copilot%20Chat%20Files/Music%20Playlist%20coding.txt)

---

## 📐 Algorithm Overview
### **Ordered Mode**
- Find song in `original_order`.  
- Swap positions (up/down).  
- Rebuild the linked list structure.  
- Preserve current song pointer.  
[1](https://bcasac-my.sharepoint.com/personal/1030581_bcas_ac/_layouts/15/Doc.aspx?sourcedoc=%7B73FDF649-D960-47B1-9F20-09645BDFFE07%7D&file=Music%20Playlist%20Management%20System.pptx&action=edit&mobileredirect=true)

### **Shuffle Mode**
- Duplicate `original_order`.  
- Randomly reorder.  
- Rebuild linked list nodes.  
- Track played songs to avoid repeats.  
[1](https://bcasac-my.sharepoint.com/personal/1030581_bcas_ac/_layouts/15/Doc.aspx?sourcedoc=%7B73FDF649-D960-47B1-9F20-09645BDFFE07%7D&file=Music%20Playlist%20Management%20System.pptx&action=edit&mobileredirect=true)

---

## 🖥️ User Interface
The UI includes:  
- Playlist dropdown (create/delete).  
- Song list with scroll support.  
- Add/Remove song buttons.  
- Order & Shuffle toggle buttons.  
- Playback buttons (prev, play/pause, stop, next).  
- Progress bar showing elapsed vs total time.  
- Volume slider.  
- Now Playing information panel.  
[2](https://bcasac-my.sharepoint.com/personal/1030581_bcas_ac/Documents/Microsoft%20Copilot%20Chat%20Files/Music%20Playlist%20coding.txt)

---

## 📦 Installation
### **Requirements**
- Python 3.8+  
- pygame  
- Tkinter (included in most Python installations)

Install pygame:
```bash
pip install pygame
``
