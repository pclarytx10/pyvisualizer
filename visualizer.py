import pygame
import pyaudio
import numpy as np
import threading
import math
import colorsys
from collections import deque

class AudioVisualizer:
    def __init__(self, width=1200, height=800):
        # Initialize Pygame
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Python Audio Visualizer")
        self.clock = pygame.time.Clock()
        
        # Audio settings
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1
        self.RATE = 44100
        
        # Audio processing
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.audio_data = np.zeros(self.CHUNK)
        self.freq_data = np.zeros(self.CHUNK // 2)
        self.is_recording = False
        
        # Visualization settings
        self.mode = 1
        self.time = 0
        self.particles = []
        self.trail_surface = pygame.Surface((width, height))
        self.trail_surface.set_alpha(240)  # For trail effect
        
        # Colors
        self.bg_color = (0, 0, 0)
        self.primary_color = (0, 255, 136)
        
        # Initialize particles
        self.init_particles()
        
        # Audio thread
        self.audio_thread = None
        
    def init_particles(self):
        """Initialize particle system"""
        self.particles = []
        for _ in range(100):
            particle = {
                'x': np.random.random() * self.width,
                'y': np.random.random() * self.height,
                'vx': (np.random.random() - 0.5) * 4,
                'vy': (np.random.random() - 0.5) * 4,
                'size': np.random.random() * 3 + 1,
                'hue': np.random.random()
            }
            self.particles.append(particle)
    
    def start_audio(self):
        """Start audio input stream"""
        try:
            self.stream = self.audio.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK,
                stream_callback=self.audio_callback
            )
            self.is_recording = True
            self.stream.start_stream()
            print("Audio stream started successfully!")
        except Exception as e:
            print(f"Error starting audio: {e}")
    
    def audio_callback(self, in_data, frame_count, time_info, status):
        """Audio input callback"""
        audio_array = np.frombuffer(in_data, dtype=np.float32)
        self.audio_data = audio_array.copy()
        
        # Compute FFT for frequency analysis
        fft = np.fft.fft(audio_array)
        self.freq_data = np.abs(fft[:len(fft)//2])
        
        return (in_data, pyaudio.paContinue)
    
    def stop_audio(self):
        """Stop audio stream"""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.audio.terminate()
        self.is_recording = False
    
    def hsv_to_rgb(self, h, s, v):
        """Convert HSV to RGB"""
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return (int(r * 255), int(g * 255), int(b * 255))
    
    def draw_frequency_bars(self):
        """Draw frequency spectrum as bars"""
        if len(self.freq_data) == 0:
            return
            
        # Normalize frequency data
        freq_normalized = self.freq_data / (np.max(self.freq_data) + 1e-6)
        
        bar_width = self.width / len(freq_normalized)
        
        for i, amplitude in enumerate(freq_normalized):
            bar_height = amplitude * self.height * 0.8
            hue = i / len(freq_normalized)
            brightness = 0.5 + amplitude * 0.5
            
            color = self.hsv_to_rgb(hue, 1.0, brightness)
            
            # Draw main bar
            rect = pygame.Rect(i * bar_width, self.height - bar_height, 
                             bar_width - 1, bar_height)
            pygame.draw.rect(self.screen, color, rect)
            
            # Add glow effect
            glow_color = self.hsv_to_rgb(hue, 1.0, min(1.0, brightness + 0.3))
            glow_rect = pygame.Rect(i * bar_width - 1, self.height - bar_height - 2,
                                  bar_width + 1, bar_height + 4)
            pygame.draw.rect(self.screen, glow_color, glow_rect, 1)
    
    def draw_waveform(self):
        """Draw audio waveform"""
        if len(self.audio_data) == 0:
            return
            
        points = []
        wave_height = self.height // 2
        
        for i, sample in enumerate(self.audio_data):
            x = i * self.width / len(self.audio_data)
            y = wave_height + sample * wave_height * 0.8
            points.append((x, y))
        
        if len(points) > 1:
            pygame.draw.lines(self.screen, self.primary_color, False, points, 3)
            
            # Mirror effect
            mirror_points = [(x, self.height - y) for x, y in points]
            pygame.draw.lines(self.screen, 
                            (*self.primary_color[:2], self.primary_color[2] // 3), 
                            False, mirror_points, 2)
    
    def draw_particles(self):
        """Draw audio-reactive particles"""
        if len(self.freq_data) == 0:
            return
            
        avg_volume = np.mean(self.freq_data)
        volume_scale = min(1.0, avg_volume / 0.1)
        
        for i, particle in enumerate(self.particles):
            # Get frequency for this particle
            freq_idx = int((i / len(self.particles)) * len(self.freq_data))
            intensity = self.freq_data[freq_idx] / (np.max(self.freq_data) + 1e-6)
            
            # Update particle position
            particle['x'] += particle['vx'] * (1 + intensity * 2)
            particle['y'] += particle['vy'] * (1 + intensity * 2)
            
            # Wrap around edges
            if particle['x'] < 0:
                particle['x'] = self.width
            elif particle['x'] > self.width:
                particle['x'] = 0
            if particle['y'] < 0:
                particle['y'] = self.height
            elif particle['y'] > self.height:
                particle['y'] = 0
            
            # Update particle properties
            particle['size'] = 1 + intensity * 8
            particle['hue'] = (particle['hue'] + intensity * 0.02) % 1.0
            
            # Draw particle
            brightness = 0.5 + intensity * 0.5
            color = self.hsv_to_rgb(particle['hue'], 1.0, brightness)
            
            pygame.draw.circle(self.screen, color,
                             (int(particle['x']), int(particle['y'])),
                             int(particle['size']))
    
    def draw_spiral(self):
        """Draw frequency data in spiral pattern"""
        if len(self.freq_data) == 0:
            return
            
        center_x = self.width // 2
        center_y = self.height // 2
        
        for i, amplitude in enumerate(self.freq_data):
            if i % 4 != 0:  # Skip some points for performance
                continue
                
            angle = (i / len(self.freq_data)) * math.pi * 8 + self.time * 0.05
            intensity = amplitude / (np.max(self.freq_data) + 1e-6)
            radius = 50 + intensity * 150 + i * 0.3
            
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius
            
            hue = (i / len(self.freq_data) + self.time * 0.01) % 1.0
            brightness = 0.5 + intensity * 0.5
            color = self.hsv_to_rgb(hue, 1.0, brightness)
            
            size = int(2 + intensity * 6)
            pygame.draw.circle(self.screen, color, (int(x), int(y)), size)
    
    def draw_plasma(self):
        """Draw plasma effect based on audio"""
        if len(self.freq_data) == 0:
            return
            
        avg_volume = np.mean(self.freq_data)
        
        # Create plasma effect (simplified for performance)
        for x in range(0, self.width, 4):
            for y in range(0, self.height, 4):
                freq_idx = int((x / self.width) * len(self.freq_data))
                intensity = self.freq_data[freq_idx] / (np.max(self.freq_data) + 1e-6)
                
                value = (math.sin(x * 0.01 + self.time * 0.1) +
                        math.sin(y * 0.01 + self.time * 0.075) +
                        math.sin((x + y) * 0.005 + self.time * 0.05) +
                        intensity * 2)
                
                normalized = (value + 4) / 8
                hue = (normalized + self.time * 0.01) % 1.0
                brightness = 0.3 + normalized * 0.7 + avg_volume * 0.5
                
                color = self.hsv_to_rgb(hue, 1.0, min(1.0, brightness))
                
                pygame.draw.rect(self.screen, color, (x, y, 4, 4))
    
    def draw_ui(self):
        """Draw user interface"""
        font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)
        
        # Title
        title = font.render("Python Audio Visualizer", True, self.primary_color)
        self.screen.blit(title, (20, 20))
        
        # Mode indicator
        modes = ["Frequency Bars", "Waveform", "Particles", "Spiral", "Plasma"]
        mode_text = small_font.render(f"Mode: {modes[self.mode-1]}", True, (255, 255, 255))
        self.screen.blit(mode_text, (20, 60))
        
        # Controls
        controls = [
            "Controls:",
            "SPACE - Start/Stop Audio",
            "1-5 - Change Visualization Mode",
            "ESC - Quit"
        ]
        
        for i, control in enumerate(controls):
            color = self.primary_color if i == 0 else (200, 200, 200)
            text = small_font.render(control, True, color)
            self.screen.blit(text, (20, self.height - 120 + i * 25))
        
        # Status
        status = "Recording" if self.is_recording else "Not Recording"
        status_color = (0, 255, 0) if self.is_recording else (255, 100, 100)
        status_text = small_font.render(f"Status: {status}", True, status_color)
        self.screen.blit(status_text, (20, 90))
    
    def run(self):
        """Main application loop"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        if self.is_recording:
                            self.stop_audio()
                        else:
                            self.start_audio()
                    elif event.key >= pygame.K_1 and event.key <= pygame.K_5:
                        self.mode = event.key - pygame.K_0
            
            # Clear screen with trail effect
            self.trail_surface.fill((0, 0, 0, 15))  # Semi-transparent black
            self.screen.blit(self.trail_surface, (0, 0))
            self.screen.fill(self.bg_color)
            
            # Draw visualization based on mode
            if self.mode == 1:
                self.draw_frequency_bars()
            elif self.mode == 2:
                self.draw_waveform()
            elif self.mode == 3:
                self.draw_particles()
            elif self.mode == 4:
                self.draw_spiral()
            elif self.mode == 5:
                self.draw_plasma()
            
            # Draw UI
            self.draw_ui()
            
            # Update time
            self.time += 1
            
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS
        
        # Cleanup
        self.stop_audio()
        pygame.quit()

if __name__ == "__main__":
    print("Python Audio Visualizer")
    print("Make sure you have the required packages installed:")
    print("pip install pygame pyaudio numpy")
    print("\nStarting visualizer...")
    
    try:
        visualizer = AudioVisualizer()
        visualizer.run()
    except ImportError as e:
        print(f"Missing required package: {e}")
        print("Please install required packages:")
        print("pip install pygame pyaudio numpy")
    except Exception as e:
        print(f"Error: {e}")
