import toga
from toga.style import Pack
from moviepy.video.io.VideoFileClip import VideoFileClip
from PIL import Image
import threading
from typing import Optional
import time


class VlcVideo(toga.Box):
    video_path: str
    is_playing: bool
    image_view: toga.ImageView
    video_clip: Optional[VideoFileClip]

    def __init__(self, video_path: str):
        super().__init__(style=Pack(flex=1))
        
        self.video_path = video_path
        self.is_playing = False
        self.video_clip = None
        
        self.image_view = toga.ImageView(style=Pack(flex=1, width=500, height=500))
        self.add(self.image_view)

        self.play()
    
    def play(self) -> None:
        thread = threading.Thread(target=self._play, daemon=True)
        thread.start()

    def _replace_image_with_fitting_video_ratio(self, width: int, height: int) -> None:
        self.remove(self.image_view)
        print(f"Creating image with size ({width}, {height})")
        self.image_view = toga.ImageView(style=Pack(flex=1, width=width//4, height=height//4))
        self.add(self.image_view)

    def _play(self) -> None:
        """Play video by rendering frames"""
        try:
            print("Start video...")
            self.video_clip = VideoFileClip(self.video_path)
            self._replace_image_with_fitting_video_ratio(self.video_clip.size[0], self.video_clip.size[1])
            self.is_playing = True
            fps = self.video_clip.fps or 30
            frame_delay = 1 / fps
            
            for frame in self.video_clip.iter_frames():
                if not self.is_playing:
                    break
                
                # Convert numpy array to PIL Image
                img = Image.fromarray(frame.astype('uint8'), 'RGB')
                self.image_view.image = img
                self.image_view.refresh()
                
                # time.sleep(frame_delay)
        
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if self.video_clip:
                self.video_clip.close()
    
    def stop(self) -> None:
        """Stop playback"""
        self.is_playing = False