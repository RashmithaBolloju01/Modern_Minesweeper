#!/usr/bin/env python3
"""
Download sound effects for Minesweeper game from free online sources.
Creates assets/sounds directory and downloads 4 WAV files.

Free sources used:
- Freesound.org: https://freesound.org
- Zapsplat: https://www.zapsplat.com
- Pixabay: https://pixabay.com/sound-effects

Includes fallback: generates beep sounds if downloads fail.
"""

import os
import requests
from pathlib import Path
import wave
import math

# Sound files with their URLs
# These are direct download links to free WAV files from public sources
SOUND_URLS = {
    "click.wav": "https://assets.mixkit.co/sfx/download/2869",
    "boom.wav": "https://assets.mixkit.co/sfx/download/1910", 
    "win.wav": "https://assets.mixkit.co/sfx/download/1435",
    "flag.wav": "https://assets.mixkit.co/sfx/download/2861",
}

# Fallback: Generate simple beep sounds if downloads fail
FALLBACK_SOUNDS = {
    "click.wav": (800, 0.1),    # Frequency (Hz), Duration (seconds)
    "boom.wav": (150, 0.3),
    "win.wav": (1000, 0.2),
    "flag.wav": (600, 0.15),
}


def create_sound_directory():
    """Create assets/sounds directory if it doesn't exist."""
    sound_dir = Path("assets/sounds")
    sound_dir.mkdir(parents=True, exist_ok=True)
    print(f"📁 Created directory: {sound_dir.absolute()}")
    return sound_dir


def download_sound(filename, url, save_dir):
    """
    Download a single sound file from URL.
    
    Args:
        filename: Name of the sound file to save
        url: URL of the sound file to download
        save_dir: Directory to save the file in
    """
    filepath = save_dir / filename
    
    # Headers to avoid being blocked by some servers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        print(f"\n📥 Downloading {filename}...", end=" ")
        response = requests.get(url, timeout=15, headers=headers, allow_redirects=True)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Write the file
        with open(filepath, "wb") as f:
            f.write(response.content)
        
        file_size = filepath.stat().st_size / 1024  # Convert to KB
        print(f"✅ Success! ({file_size:.1f} KB)")
        return True
        
    except requests.exceptions.Timeout:
        print(f"❌ Timeout")
        return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection Error")
        return False
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP {e.response.status_code}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Request Error")
        return False
    except IOError as e:
        print(f"❌ File Error")
        return False


def generate_beep_sound(filename, save_dir, frequency, duration):
    """
    Generate a simple beep sound as a WAV file (fallback method).
    
    Args:
        filename: Name of the sound file to save
        save_dir: Directory to save the file in
        frequency: Frequency of the beep in Hz
        duration: Duration of the beep in seconds
    """
    filepath = save_dir / filename
    sample_rate = 44100  # CD quality
    num_samples = int(sample_rate * duration)
    
    try:
        print(f"\n🔊 Generating {filename}...", end=" ")
        
        # Create WAV file
        with wave.open(str(filepath), 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 2 bytes = 16-bit
            wav_file.setframerate(sample_rate)
            
            # Generate beep sound data
            frames = []
            for i in range(num_samples):
                # Calculate sample value (sine wave)
                sample = int(32767 * 0.5 * math.sin(2 * math.pi * frequency * i / sample_rate))
                frames.append(sample.to_bytes(2, byteorder='little', signed=True))
            
            wav_file.writeframes(b''.join(frames))
        
        file_size = filepath.stat().st_size / 1024
        print(f"✅ Generated! ({file_size:.1f} KB)")
        return True
        
    except Exception as e:
        print(f"❌ Generation Error")
        return False


def main():
    """Main function to orchestrate the download process."""
    print("=" * 60)
    print("🎮 Minesweeper Sound Effects Downloader")
    print("=" * 60)
    
    # Create directory
    sound_dir = create_sound_directory()
    
    # Download each sound file
    successful = 0
    failed = 0
    generated = 0
    
    for filename, url in SOUND_URLS.items():
        if download_sound(filename, url, sound_dir):
            successful += 1
        else:
            # Fallback: Generate sound if download fails
            freq, duration = FALLBACK_SOUNDS[filename]
            if generate_beep_sound(filename, sound_dir, freq, duration):
                generated += 1
            else:
                failed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print(f"📊 Summary:")
    print(f"   ✅ Downloaded: {successful}/{len(SOUND_URLS)}")
    print(f"   🔊 Generated: {generated}/{len(SOUND_URLS)}")
    print(f"   ❌ Failed: {failed}/{len(SOUND_URLS)}")
    print(f"   📂 Location: {sound_dir.absolute()}")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
