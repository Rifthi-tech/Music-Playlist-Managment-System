import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import os
import random
import pickle
import pygame
from pygame import mixer
import time
import threading

# Initialize pygame
pygame.init()
mixer.init()

class Song:
    """Represents a song with metadata"""
    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.title = os.path.splitext(self.filename)[0]
        self.artist = "Unknown Artist"
        self.duration = self._get_duration()
        self.album = "Unknown Album"
        
    def _get_duration(self):
        """Get song duration using pygame"""
        try:
            sound = pygame.mixer.Sound(self.filepath)
            duration = sound.get_length()
            del sound  # Clean up memory
            return duration
        except:
            return 180  # Default to 3 minutes

class PlaylistNode:
    """Node for doubly-linked list implementation"""
    def __init__(self, song):
        self.song = song
        self.next = None
        self.prev = None

class Playlist:
    """Playlist ADT using doubly-linked list"""
    def __init__(self, name):
        self.name = name
        self.head = None
        self.tail = None
        self.current = None
        self.length = 0
        self.is_shuffled = False
        self.original_order = []
        self.shuffle_session = None  # Track played songs in shuffle mode
        
    def add_song(self, song):
        """Add song to end of playlist"""
        new_node = PlaylistNode(song)
        
        if not self.head:
            self.head = new_node
            self.tail = new_node
            self.current = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
            
        self.length += 1
        self.original_order.append(new_node)
        
    def remove_song(self, song_title):
        """Remove song by title"""
        current = self.head
        while current:
            if current.song.title == song_title:
                # Update pointers
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                    
                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                    
                # Update current if needed
                if self.current == current:
                    self.current = current.next if current.next else self.head
                    
                # Update original order
                if current in self.original_order:
                    self.original_order.remove(current)
                
                self.length -= 1
                return True
            current = current.next
        return False
        
    def move_song(self, song_title, direction):
        """Move song up or down in playlist"""
        if self.is_shuffled or self.length <= 1:
            return False
            
        # Find the song in original order
        for i, node in enumerate(self.original_order):
            if node.song.title == song_title:
                if direction == "up" and i > 0:
                    # Swap with previous in original order
                    self.original_order[i], self.original_order[i-1] = self.original_order[i-1], self.original_order[i]
                    self._rebuild_linked_list()
                    return True
                elif direction == "down" and i < len(self.original_order) - 1:
                    # Swap with next in original order
                    self.original_order[i], self.original_order[i+1] = self.original_order[i+1], self.original_order[i]
                    self._rebuild_linked_list()
                    return True
        return False
        
    def _rebuild_linked_list(self):
        """Rebuild the linked list from original_order"""
        if not self.original_order:
            self.head = self.tail = self.current = None
            return
            
        # Store current song reference
        current_song = self.current.song if self.current else None
        
        # Rebuild linked list
        for i, node in enumerate(self.original_order):
            node.prev = self.original_order[i-1] if i > 0 else None
            node.next = self.original_order[i+1] if i < len(self.original_order)-1 else None
            
        self.head = self.original_order[0]
        self.tail = self.original_order[-1]
        
        # Restore current song
        if current_song:
            for node in self.original_order:
                if node.song.title == current_song.title:
                    self.current = node
                    break
        else:
            self.current = self.head
        
    def shuffle(self):
        """Shuffle the playlist"""
        if self.length <= 1:
            return
            
        # Store current song
        current_song = self.current.song if self.current else None
        
        # Create shuffled copy of original order
        shuffled_nodes = self.original_order.copy()
        random.shuffle(shuffled_nodes)
        
        # Rebuild linked list with shuffled order
        for i, node in enumerate(shuffled_nodes):
            node.prev = shuffled_nodes[i-1] if i > 0 else None
            node.next = shuffled_nodes[i+1] if i < len(shuffled_nodes)-1 else None
            
        self.head = shuffled_nodes[0]
        self.tail = shuffled_nodes[-1]
        
        # Restore current song
        self.current = self.head  # Default
        if current_song:
            for node in shuffled_nodes:
                if node.song.title == current_song.title:
                    self.current = node
                    break
                    
        self.is_shuffled = True
        
    def unshuffle(self):
        """Restore original order"""
        if not self.is_shuffled:
            return
        
        self._rebuild_linked_list()
        self.is_shuffled = False
        
    def get_song_list(self):
        """Get list of song titles in current order"""
        songs = []
        current = self.head
        while current:
            songs.append(current.song.title)
            current = current.next
        return songs
        
    def play_next(self):
        """Move to next song in playlist or random in shuffle mode"""
        if not self.current:
            return None

        if self.is_shuffled:
            # True random shuffle: pick a random unplayed song
            if self.shuffle_session is None or len(self.shuffle_session) == self.length:
                # Reset session if all songs played
                self.shuffle_session = []
            # Build list of unplayed nodes
            unplayed = [node for node in self.original_order if node not in self.shuffle_session]
            if not unplayed:
                # All played, reset
                self.shuffle_session = []
                unplayed = self.original_order.copy()
            next_node = random.choice(unplayed)
            self.shuffle_session.append(next_node)
            self.current = next_node
        else:
            # Queue mode: play next in order
            if self.current.next:
                self.current = self.current.next
            else:
                self.current = self.head  # Loop to start

        return self.current.song
        
    def play_previous(self):
        """Move to previous song in playlist (queue mode only)"""
        if not self.current:
            return None

        if self.is_shuffled:
            # In shuffle mode, just pick another random song
            return self.play_next()
        else:
            if self.current.prev:
                self.current = self.current.prev
            else:
                self.current = self.tail  # Loop to end

        return self.current.song

class MusicPlayerApp:
    """Main application GUI"""
    def __init__(self, root):
        self.root = root
        self.root.title("Music Playlist Management System")
        self.root.geometry("800x600")
        
        # Configure styles
        self._configure_styles()
        
        # Playlist manager
        self.playlists = {}
        self.current_playlist = None
        
        # Playback state
        self.is_playing = False
        self.is_paused = False
        self.current_song = None
        self.song_length = 0
        self.start_time = 0
        self.pause_time = 0
        
        # Store button references for state management
        self.move_up_btn = None
        self.move_down_btn = None
        self.shuffle_btn = None
        
        # Load saved playlists
        self._load_playlists()
        
        # Create GUI
        self._create_widgets()
        
        # Start progress updater
        self._update_progress()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _configure_styles(self):
        """Configure UI styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Custom styles
        style.configure("custom.Horizontal.TProgressbar",
                       background='#4CAF50',
                       troughcolor='#f0f0f0',
                       bordercolor='#333',
                       lightcolor='#4CAF50',
                       darkcolor='#2E7D32',
                       thickness=10)
        
        style.configure('TButton', font=('Helvetica', 10), padding=5)
        style.map('TButton',
                foreground=[('active', 'black'), ('!active', 'black')],
                background=[('active', '#E1E1E1'), ('!active', '#F0F0F0')])
        
        style.configure('TCombobox', font=('Helvetica', 10), padding=5)
    
    def _create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Playlist controls frame
        playlist_controls = tk.Frame(main_frame)
        playlist_controls.pack(fill=tk.X, pady=5)
        
        # Playlist selection
        tk.Label(playlist_controls, text="Playlist:").pack(side=tk.LEFT)
        
        self.playlist_var = tk.StringVar()
        self.playlist_dropdown = ttk.Combobox(
            playlist_controls,
            textvariable=self.playlist_var,
            state='readonly'
        )
        self.playlist_dropdown.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.playlist_dropdown.bind("<<ComboboxSelected>>", self._select_playlist)
        
        # Playlist management buttons
        ttk.Button(
            playlist_controls,
            text="New",
            command=self._create_playlist
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            playlist_controls,
            text="Delete",
            command=self._delete_playlist
        ).pack(side=tk.LEFT, padx=2)
        
        # Song list frame
        song_list_frame = tk.Frame(main_frame)
        song_list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Song list with scrollbar
        self.song_listbox = tk.Listbox(
            song_list_frame,
            selectmode=tk.SINGLE,
            font=('Helvetica', 10),
            activestyle='none',
            bg='white',
            fg='black',
            selectbackground='#4CAF50',
            selectforeground='white'
        )
        self.song_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(song_list_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.song_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.song_listbox.yview)
        
        # Bind double click to play song
        self.song_listbox.bind("<Double-Button-1>", lambda e: self._play_song())
        
        # Song controls frame
        song_controls = tk.Frame(main_frame)
        song_controls.pack(fill=tk.X, pady=5)
        
        # Song management buttons
        ttk.Button(
            song_controls,
            text="Add Songs",
            command=self._add_songs
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            song_controls,
            text="Remove",
            command=self._remove_song
        ).pack(side=tk.LEFT, padx=2)

        self.order_btn = ttk.Button(
            song_controls,
            text="Order: ON",
            command=self._toggle_order
        )
        self.order_btn.pack(side=tk.LEFT, padx=2)

        self.shuffle_btn = ttk.Button(
            song_controls,
            text="Shuffle: OFF",
            command=self._toggle_shuffle
        )
        self.shuffle_btn.pack(side=tk.LEFT, padx=2)
        
        # Playback controls frame
        playback_controls = tk.Frame(main_frame)
        playback_controls.pack(fill=tk.X, pady=5)
        
        # Playback buttons
        ttk.Button(
            playback_controls,
            text="⏮",
            command=self._previous_song
        ).pack(side=tk.LEFT, padx=2)
        
        self.play_pause_btn = ttk.Button(
            playback_controls,
            text="⏯",
            command=self._play_pause
        )
        self.play_pause_btn.pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            playback_controls,
            text="⏹",
            command=self._stop_song
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            playback_controls,
            text="⏭",
            command=self._next_song
        ).pack(side=tk.LEFT, padx=2)
        
        # Progress bar frame
        progress_frame = tk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=5)
        
        # Time labels and progress bar
        self.time_elapsed = tk.Label(
            progress_frame,
            text="0:00",
            width=6,
            font=('Helvetica', 9)
        )
        self.time_elapsed.pack(side=tk.LEFT)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            style="custom.Horizontal.TProgressbar",
            mode='determinate'
        )
        self.progress_bar.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        self.time_total = tk.Label(
            progress_frame,
            text="0:00",
            width=6,
            font=('Helvetica', 9)
        )
        self.time_total.pack(side=tk.RIGHT)
        
        # Volume control
        volume_frame = tk.Frame(main_frame)
        volume_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(volume_frame, text="🔈").pack(side=tk.LEFT)
        
        self.volume_var = tk.DoubleVar(value=0.7)
        mixer.music.set_volume(self.volume_var.get())
        
        ttk.Scale(
            volume_frame,
            from_=0,
            to=1,
            variable=self.volume_var,
            command=self._set_volume,
            length=150
        ).pack(side=tk.LEFT, padx=5)
        
        # Now playing info
        self.now_playing_frame = tk.Frame(main_frame, bd=1, relief=tk.SUNKEN)
        self.now_playing_frame.pack(fill=tk.X, pady=5)
        
        self.now_playing_label = tk.Label(
            self.now_playing_frame,
            text="Now Playing: ",
            font=('Helvetica', 10, 'bold'),
            anchor=tk.W
        )
        self.now_playing_label.pack(fill=tk.X)
        
        self.song_info_label = tk.Label(
            self.now_playing_frame,
            text="No song selected",
            font=('Helvetica', 9),
            anchor=tk.W
        )
        self.song_info_label.pack(fill=tk.X)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=('Helvetica', 9)
        )
        status_bar.pack(fill=tk.X, pady=(5, 0))
        
        # Update playlist dropdown
        self._update_playlist_dropdown()
    
    # Playlist management methods
    def _create_playlist(self):
        """Create a new playlist"""
        name = simpledialog.askstring("New Playlist", "Enter playlist name:")
        if name and name.strip():
            name = name.strip()
            if name in self.playlists:
                messagebox.showwarning("Duplicate Name", "Playlist with this name already exists")
                return
            self.playlists[name] = Playlist(name)
            self.current_playlist = name
            self._update_playlist_dropdown()
            self._update_song_list()
            self._save_playlists()
            self.status_var.set(f"Created playlist: {name}")
    
    def _delete_playlist(self):
        """Delete current playlist"""
        if not self.current_playlist:
            messagebox.showwarning("No Playlist", "No playlist selected")
            return
            
        if messagebox.askyesno("Delete Playlist", f"Delete playlist '{self.current_playlist}'?"):
            # Stop playback if deleting current playlist
            if self.is_playing:
                self._stop_song()
            
            del self.playlists[self.current_playlist]
            self.current_playlist = None
            self._update_playlist_dropdown()
            self._update_song_list()
            self._update_move_buttons_state()
            self._save_playlists()
            self.status_var.set("Playlist deleted")
    
    def _select_playlist(self, event=None):
        """Select a playlist from dropdown"""
        selected = self.playlist_var.get()
        if selected in self.playlists:
            self.current_playlist = selected
            self._update_song_list()
            self._update_move_buttons_state()
            self._update_shuffle_button_state()
            self.status_var.set(f"Selected playlist: {selected}")
    
    def _update_playlist_dropdown(self):
        """Update playlist dropdown menu"""
        self.playlist_dropdown['values'] = list(self.playlists.keys())
        if self.current_playlist and self.current_playlist in self.playlists:
            self.playlist_var.set(self.current_playlist)
        elif self.playlists:
            first_playlist = next(iter(self.playlists))
            self.playlist_var.set(first_playlist)
            self.current_playlist = first_playlist
        else:
            self.playlist_var.set("")
            self.current_playlist = None
    
    def _add_songs(self):
        """Add songs to current playlist"""
        if not self.current_playlist:
            messagebox.showwarning("No Playlist", "Please create or select a playlist first")
            return
        
        filepaths = filedialog.askopenfilenames(
            title="Select Songs",
            filetypes=[("Audio Files", "*.mp3 *.wav *.ogg *.flac")]
        )
        
        if filepaths:
            added_count = 0
            for filepath in filepaths:
                try:
                    if os.path.exists(filepath):
                        song = Song(filepath)
                        self.playlists[self.current_playlist].add_song(song)
                        added_count += 1
                    else:
                        messagebox.showwarning("File Not Found", f"File not found: {filepath}")
                except Exception as e:
                    messagebox.showerror("Error", f"Could not add {filepath}:\n{str(e)}")
            
            if added_count > 0:
                self._update_song_list()
                self._save_playlists()
                self.status_var.set(f"Added {added_count} song(s) to {self.current_playlist}")
    
    def _remove_song(self):
        """Remove selected song from playlist"""
        if not self.current_playlist:
            messagebox.showwarning("No Playlist", "No playlist selected")
            return
        
        selected = self.song_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a song to remove")
            return
        
        song_title = self.song_listbox.get(selected[0])
        if self.playlists[self.current_playlist].remove_song(song_title):
            # Stop playback if removed current song
            if self.current_song and self.current_song.title == song_title:
                self._stop_song()
            
            self._update_song_list()
            self._save_playlists()
            self.status_var.set(f"Removed: {song_title}")
        else:
            messagebox.showerror("Error", f"Could not remove {song_title}")
    
    def _move_song(self, direction):
        """Move song up or down in playlist"""
        if not self.current_playlist:
            messagebox.showwarning("No Playlist", "No playlist selected")
            return
        
        playlist = self.playlists[self.current_playlist]
        
        if playlist.is_shuffled:
            messagebox.showwarning("Shuffle Active", "Cannot move songs while shuffle is active")
            return
        
        selected = self.song_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a song to move")
            return
        
        song_title = self.song_listbox.get(selected[0])
        if playlist.move_song(song_title, direction):
            self._update_song_list()
            self._save_playlists()
            
            # Update selection to follow moved song
            new_pos = selected[0] - 1 if direction == "up" else selected[0] + 1
            new_pos = max(0, min(new_pos, playlist.length - 1))
                
            self.song_listbox.selection_clear(0, tk.END)
            self.song_listbox.selection_set(new_pos)
            self.song_listbox.see(new_pos)
            
            self.status_var.set(f"Moved {song_title} {direction}")
    
    def _toggle_order(self):
        """Set playlist to queue (ordered) mode"""
        if not self.current_playlist:
            messagebox.showwarning("No Playlist", "No playlist selected")
            return
        playlist = self.playlists[self.current_playlist]
        playlist.is_shuffled = False
        playlist.shuffle_session = None
        self.order_btn.config(text="Order: ON")
        self.shuffle_btn.config(text="Shuffle: OFF")
        self._update_song_list()
        self.status_var.set(f"{playlist.name} set to queue order")

    def _toggle_shuffle(self):
        """Set playlist to shuffle mode (true random)"""
        if not self.current_playlist:
            messagebox.showwarning("No Playlist", "No playlist selected")
            return
        playlist = self.playlists[self.current_playlist]
        playlist.is_shuffled = True
        playlist.shuffle_session = []
        self.shuffle_btn.config(text="Shuffle: ON")
        self.order_btn.config(text="Order: OFF")
        self._update_song_list()
        self.status_var.set(f"{playlist.name} set to shuffle mode")

    def _update_move_buttons_state(self):
        """Enable or disable Move Up/Down buttons based on shuffle state"""
        if not self.current_playlist or not self.move_up_btn or not self.move_down_btn:
            return
            
        playlist = self.playlists[self.current_playlist]
        state = 'disabled' if playlist.is_shuffled else 'normal'
        
        self.move_up_btn.config(state=state)
        self.move_down_btn.config(state=state)
    
    def _update_shuffle_button_state(self):
        """Update shuffle button text based on current playlist state"""
        if not self.current_playlist or not self.shuffle_btn:
            return
            
        playlist = self.playlists[self.current_playlist]
        text = "Shuffle: ON" if playlist.is_shuffled else "Shuffle: OFF"
        self.shuffle_btn.config(text=text)
    
    def _update_song_list(self):
        """Update the song listbox with current playlist songs"""
        self.song_listbox.delete(0, tk.END)
        
        if not self.current_playlist:
            return
        
        playlist = self.playlists[self.current_playlist]
        for song in playlist.get_song_list():
            self.song_listbox.insert(tk.END, song)
        
        # Highlight current song if playing
        if playlist.current and self.current_song:
            try:
                songs = playlist.get_song_list()
                if self.current_song.title in songs:
                    index = songs.index(self.current_song.title)
                    self.song_listbox.selection_clear(0, tk.END)
                    self.song_listbox.selection_set(index)
                    self.song_listbox.see(index)
            except (ValueError, AttributeError):
                pass
    
    # Playback control methods
    def _play_pause(self):
        """Toggle play/pause"""
        if self.is_paused:
            # Resume paused song
            mixer.music.unpause()
            self.is_paused = False
            self.start_time += time.time() - self.pause_time
            self.play_pause_btn.config(text="⏸")
            self.status_var.set(f"Resumed: {self.current_song.title if self.current_song else 'Unknown'}")
        elif self.is_playing:
            # Pause current song
            self._pause_song()
        else:
            # Start playing
            self._play_song()
    
    def _play_song(self):
        """Play selected or current song"""
        if not self.current_playlist or not self.playlists[self.current_playlist].length:
            messagebox.showwarning("No Songs", "No songs in current playlist")
            return
        
        playlist = self.playlists[self.current_playlist]
        
        # If song is selected, play that song
        selected = self.song_listbox.curselection()
        if selected:
            song_title = self.song_listbox.get(selected[0])
            current = playlist.head
            while current:
                if current.song.title == song_title:
                    playlist.current = current
                    break
                current = current.next
        
        # If no current song, start from beginning
        if not playlist.current:
            playlist.current = playlist.head
        
        if playlist.current:
            self._play_audio(playlist.current.song)
    
    def _play_audio(self, song):
        """Play audio file"""
        try:
            if not os.path.exists(song.filepath):
                messagebox.showerror("File Not Found", f"Audio file not found:\n{song.filepath}")
                return
                
            mixer.music.load(song.filepath)
            mixer.music.play()
            
            self.current_song = song
            self.song_length = song.duration if song.duration > 0 else 180
            self.is_playing = True
            self.is_paused = False
            self.start_time = time.time()

            self.time_total.config(text=self._format_time(self.song_length))
            self.progress_var.set(0)

            self.play_pause_btn.config(text="⏸")
            self._update_now_playing(song)
            self._update_song_list()
            self.status_var.set(f"Now playing: {song.title}")
            
        except pygame.error as e:
            messagebox.showerror("Playback Error", f"Could not play file:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An error occurred:\n{str(e)}")
    
    def _update_now_playing(self, song):
        """Update now playing info"""
        self.now_playing_label.config(text=f"Now Playing: {song.title}")
        
        # Format duration
        duration_str = self._format_time(song.duration)
        
        # Display song info
        info_text = f"Artist: {song.artist} | Album: {song.album} | Duration: {duration_str}"
        self.song_info_label.config(text=info_text)
    
    def _pause_song(self):
        """Pause current song"""
        if self.is_playing and not self.is_paused:
            mixer.music.pause()
            self.is_paused = True
            self.pause_time = time.time()
            self.play_pause_btn.config(text="⏯")
            self.status_var.set(f"Paused: {self.current_song.title if self.current_song else 'Unknown'}")
    
    def _stop_song(self):
        """Stop playback"""
        mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.current_song = None
        self.progress_var.set(0)
        self.time_elapsed.config(text="0:00")
        self.time_total.config(text="0:00")
        self.play_pause_btn.config(text="⏯")
        self.status_var.set("Playback stopped")
        self.now_playing_label.config(text="Now Playing: ")
        self.song_info_label.config(text="No song selected")
    
    def _next_song(self):
        """Play next song in playlist"""
        if not self.current_playlist:
            return
        
        playlist = self.playlists[self.current_playlist]
        if not playlist.length:
            return
            
        next_song = playlist.play_next()
        
        if next_song:
            self._play_audio(next_song)
        else:
            self._stop_song()
    
    def _previous_song(self):
        """Play previous song in playlist"""
        if not self.current_playlist:
            return
        
        playlist = self.playlists[self.current_playlist]
        if not playlist.length:
            return
            
        prev_song = playlist.play_previous()
        
        if prev_song:
            self._play_audio(prev_song)
        else:
            self._stop_song()
    
    def _set_volume(self, val):
        """Set playback volume"""
        try:
            volume = float(val)
            mixer.music.set_volume(volume)
        except (ValueError, pygame.error):
            pass
    
    def _update_progress(self):
        """Update progress bar and time display"""
        try:
            if self.is_playing and not self.is_paused and self.current_song:
                # Check if song is still playing
                if not mixer.music.get_busy():
                    # Song finished, play next
                    self._next_song()
                    self.root.after(200, self._update_progress)
                    return
                
                elapsed_time = time.time() - self.start_time
                
                if elapsed_time >= self.song_length:
                    # Song should be finished
                    self.progress_var.set(100)
                    self.time_elapsed.config(text=self._format_time(self.song_length))
                    self._next_song()
                    self.root.after(200, self._update_progress)
                    return
                
                # Update progress
                progress_percent = (elapsed_time / self.song_length) * 100 if self.song_length > 0 else 0
                progress_percent = min(100, max(0, progress_percent))
                
                self.progress_var.set(progress_percent)
                self.time_elapsed.config(text=self._format_time(elapsed_time))
        
        except Exception as e:
            # Handle any unexpected errors gracefully
            pass
        
        # Schedule next update
        self.root.after(200, self._update_progress)
    
    def _format_time(self, seconds):
        """Format seconds as MM:SS"""
        try:
            seconds = max(0, seconds)  # Ensure non-negative
            minutes = int(seconds // 60)
            seconds = int(seconds % 60)
            return f"{minutes}:{seconds:02d}"
        except (ValueError, TypeError):
            return "0:00"
    
    # Data persistence methods
    def _save_playlists(self):
        """Save playlists to file"""
        try:
            save_data = {}
            for name, playlist in self.playlists.items():
                # Save songs in original order
                songs = []
                for node in playlist.original_order:
                    if node and node.song and os.path.exists(node.song.filepath):
                        songs.append(node.song.filepath)
                save_data[name] = {
                    'songs': songs,
                    'is_shuffled': playlist.is_shuffled
                }
            
            with open('playlists.pkl', 'wb') as f:
                pickle.dump(save_data, f)
                
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save playlists:\n{str(e)}")
    
    def _load_playlists(self):
        """Load playlists from file"""
        try:
            with open('playlists.pkl', 'rb') as f:
                save_data = pickle.load(f)
            
            for name, playlist_data in save_data.items():
                # Handle old format (just list of songs)
                if isinstance(playlist_data, list):
                    songs = playlist_data
                    is_shuffled = False
                else:
                    songs = playlist_data.get('songs', [])
                    is_shuffled = playlist_data.get('is_shuffled', False)
                
                self.playlists[name] = Playlist(name)
                
                # Add songs that still exist
                for path in songs:
                    if os.path.exists(path):
                        try:
                            song = Song(path)
                            self.playlists[name].add_song(song)
                        except Exception:
                            continue  # Skip songs that can't be loaded
                
                # Restore shuffle state
                if is_shuffled and self.playlists[name].length > 1:
                    self.playlists[name].shuffle()
            
            # Set current playlist
            if self.playlists:
                self.current_playlist = next(iter(self.playlists))
                
        except (FileNotFoundError, EOFError):
            # No saved playlists or corrupted file
            pass
        except Exception as e:
            messagebox.showerror("Load Error", f"Could not load playlists:\n{str(e)}")
    
    def _on_close(self):
        """Handle window close event"""
        try:
            self._save_playlists()
            mixer.music.stop()
            mixer.quit()
            pygame.quit()
        except:
            pass
        finally:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayerApp(root)
    root.mainloop()