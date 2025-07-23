# 🎵 Python Audio Visualizer

A real-time audio visualizer inspired by classic Winamp visualizations. This application captures audio from your microphone and creates stunning visual effects that respond to sound in real-time.

## ✨ Features

- **5 Unique Visualization Modes:**
  - 🎚️ **Frequency Bars** - Classic spectrum analyzer with colorful bars
  - 〰️ **Waveform** - Real-time audio waveform with mirror effects
  - ✨ **Particles** - Audio-reactive particle system that dances to the beat
  - 🌀 **Spiral** - Frequency data arranged in beautiful spiral patterns
  - 🌈 **Plasma** - Psychedelic plasma effects that pulse with audio

- **Real-time Audio Processing:**
  - Live microphone input capture
  - Fast Fourier Transform (FFT) analysis
  - 60 FPS smooth animations
  - Dynamic color generation based on frequency content

- **Interactive Controls:**
  - Switch between visualization modes instantly
  - Start/stop audio recording
  - Responsive to all types of audio input

## 🚀 Quick Start

### Using uv (Recommended - Faster)

```bash
# Install uv if you haven't already
pip install uv

# Clone or download the project files
# Navigate to the project directory

# Install dependencies
uv pip install -r requirements.txt

# Run the visualizer
python audio_visualizer.py
```

### Using pip (Traditional)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the visualizer
python audio_visualizer.py
```

## 📋 Requirements

- Python 3.8 or higher
- Working microphone
- Audio drivers installed

### Dependencies
- `pygame>=2.1.0` - Graphics and window management
- `pyaudio>=0.2.11` - Real-time audio input
- `numpy>=1.21.0` - Audio processing and FFT analysis

## 🎮 Controls

| Key | Action |
|-----|--------|
| `SPACE` | Start/Stop audio recording |
| `1` | Frequency Bars mode |
| `2` | Waveform mode |
| `3` | Particles mode |
| `4` | Spiral mode |
| `5` | Plasma mode |
| `ESC` | Quit application |

## 🔧 Installation Troubleshooting

### PyAudio Installation Issues

PyAudio requires system audio libraries and can be tricky to install. Here are platform-specific solutions:

#### Windows
```bash
# Try pre-compiled wheel first
uv pip install --only-binary=all pyaudio

# If that fails, use pipwin
pip install pipwin
pipwin install pyaudio
```

#### macOS
```bash
# Install PortAudio first
brew install portaudio

# Then install PyAudio
uv pip install pyaudio
```

#### Linux (Ubuntu/Debian)
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install portaudio19-dev python3-pyaudio

# Then install PyAudio
uv pip install pyaudio
```

#### Linux (CentOS/RHEL/Fedora)
```bash
# Install system dependencies
sudo dnf install portaudio-devel python3-pyaudio

# Then install PyAudio
uv pip install pyaudio
```

### Alternative: SoundDevice

If PyAudio continues to cause issues, you can modify the requirements.txt to use `sounddevice` instead:

```txt
pygame>=2.1.0
sounddevice>=0.4.4
numpy>=1.21.0
```

## 🎯 Usage Tips

1. **Start the Application**: Run the Python script and you'll see the visualizer window
2. **Grant Microphone Permission**: Click "Start Audio" and allow microphone access
3. **Make Some Noise**: Speak, play music, or make sounds to see the visualizations react
4. **Try Different Modes**: Each visualization responds differently to various types of audio
5. **Optimal Audio**: Works best with music, speech, or varied audio input

## 🏗️ Project Structure

```
audio-visualizer/
├── audio_visualizer.py    # Main application file
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🔬 How It Works

1. **Audio Capture**: PyAudio captures real-time audio from your microphone
2. **Signal Processing**: NumPy performs Fast Fourier Transform (FFT) to analyze frequency content
3. **Visualization**: Pygame renders graphics at 60 FPS based on audio data
4. **Real-time Updates**: Audio callback runs in separate thread for smooth processing

Each visualization mode analyzes different aspects of the audio signal:
- **Frequency content** for spectrum-based modes
- **Amplitude variations** for waveform displays  
- **Beat detection** for particle systems
- **Harmonic analysis** for color generation

## 🎨 Customization

The visualizer is designed to be easily customizable. You can modify:

- **Colors**: Adjust HSV color generation in visualization functions
- **Sensitivity**: Change audio processing parameters
- **Window Size**: Modify width/height in the constructor
- **Frame Rate**: Adjust the FPS in the main loop
- **Particle Count**: Change the number of particles in particle mode

## 🐛 Common Issues

**"No audio detected"**
- Check microphone permissions
- Verify microphone is working in other applications
- Try speaking louder or playing music

**"Application crashes on audio start"**
- Ensure PyAudio is properly installed
- Check that no other applications are using the microphone exclusively
- Try running as administrator (Windows) or with sudo (Linux)

**"Poor performance"**
- Close other applications to free up system resources
- Reduce window size for better performance on older hardware
- Lower the FPS if needed

## 🤝 Contributing

Contributions are welcome! Here are some ways you can help:

- 🐛 Report bugs or issues
- 💡 Suggest new visualization modes
- 🎨 Improve graphics and effects
- 📚 Enhance documentation
- ⚡ Optimize performance

## 📜 License

This project is licensed under the GNU v3 License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Inspired by classic Winamp and media player visualizations
- Built with Python's excellent audio and graphics libraries
- Thanks to the open-source community for the amazing tools

---

**Enjoy creating beautiful visualizations with your audio! 🎵✨**