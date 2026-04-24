"""
Sound Manager Module for Minesweeper Game
Uses pygame mixer to handle sound effects.
Safely loads and plays sounds with error handling.
"""

import os
from pathlib import Path
import pygame


class SoundManager:
    """Manager for game sound effects using pygame mixer."""
    
    # Path to sound assets
    SOUNDS_DIR = Path("assets/sounds")
    
    # Sound file names
    SOUND_NAMES = {
        "click": "click.wav",
        "boom": "boom.wav",
        "win": "win.wav",
        "flag": "flag.wav",
    }
    
    def __init__(self, enabled=True):
        """
        Initialize the Sound Manager.
        
        Args:
            enabled: Whether sound is enabled (default: True)
        """
        self.enabled = enabled
        self.sounds = {}
        self.mixer_initialized = False
        
        if self.enabled:
            self._init_mixer()
            self._load_sounds()
    
    def _init_mixer(self):
        """Initialize pygame mixer with error handling."""
        try:
            pygame.mixer.init()
            self.mixer_initialized = True
            print("✅ Pygame mixer initialized successfully")
        except Exception as e:
            print(f"⚠️  Warning: Could not initialize mixer - {str(e)}")
            self.enabled = False
    
    def _load_sounds(self):
        """Load all sound files from assets/sounds folder."""
        if not self.mixer_initialized:
            return
        
        # Create sounds directory if it doesn't exist
        self.SOUNDS_DIR.mkdir(parents=True, exist_ok=True)
        
        for sound_key, sound_file in self.SOUND_NAMES.items():
            filepath = self.SOUNDS_DIR / sound_file
            
            try:
                if filepath.exists():
                    self.sounds[sound_key] = pygame.mixer.Sound(str(filepath))
                    print(f"✅ Loaded sound: {sound_file}")
                else:
                    print(f"⚠️  Warning: Sound file not found - {filepath}")
                    
            except pygame.error as e:
                print(f"❌ Error loading {sound_file}: {str(e)}")
            except Exception as e:
                print(f"❌ Unexpected error loading {sound_file}: {str(e)}")
    
    def _play_sound(self, sound_key):
        """
        Safely play a sound by key.
        
        Args:
            sound_key: The key of the sound to play (click, boom, win, flag)
        """
        if not self.enabled or not self.mixer_initialized:
            return False
        
        try:
            if sound_key in self.sounds:
                self.sounds[sound_key].play()
                return True
            else:
                print(f"⚠️  Sound '{sound_key}' not loaded")
                return False
                
        except pygame.error as e:
            print(f"❌ Error playing sound '{sound_key}': {str(e)}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error playing sound '{sound_key}': {str(e)}")
            return False
    
    def play_click(self):
        """Play the cell click sound effect."""
        return self._play_sound("click")
    
    def play_boom(self):
        """Play the mine explosion/boom sound effect."""
        return self._play_sound("boom")
    
    def play_win(self):
        """Play the game win/victory sound effect."""
        return self._play_sound("win")
    
    def play_flag(self):
        """Play the flag placement sound effect."""
        return self._play_sound("flag")
    
    def stop_all(self):
        """Stop all currently playing sounds."""
        if self.mixer_initialized:
            try:
                pygame.mixer.stop()
            except Exception as e:
                print(f"⚠️  Error stopping sounds: {str(e)}")
    
    def set_volume(self, volume):
        """
        Set the volume for all sounds (0.0 to 1.0).
        
        Args:
            volume: Volume level from 0.0 (silent) to 1.0 (max)
        """
        if not self.mixer_initialized:
            return
        
        volume = max(0.0, min(1.0, volume))
        try:
            pygame.mixer.music.set_volume(volume)
            for sound in self.sounds.values():
                sound.set_volume(volume)
        except Exception as e:
            print(f"⚠️  Error setting volume: {str(e)}")
    
    def toggle_sound(self, enabled):
        """
        Toggle sound on/off.
        
        Args:
            enabled: Whether to enable sound
        """
        self.enabled = enabled
        if not enabled:
            self.stop_all()


# Create a global sound manager instance
sound_manager = SoundManager(enabled=True)
