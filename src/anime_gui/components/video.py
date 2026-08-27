import cv2
import toga
from toga.style import Pack


from anime_gui.context import ApplicationContext


class VideoView(toga.Box):
    video_filename: str
    context: ApplicationContext
    webview: toga.WebView
    video_url: str
    video_width: int
    video_height: int

    def __init__(
        self,
        context: ApplicationContext,
        video_filename: str,
    ):
        self.video_filename = video_filename
        self.context = context
        self.video_url = context.file_name_to_video_resource_url(video_filename)

        self.video_width, self.video_height = self._get_video_dimensions()
        super().__init__(style=Pack(flex=1, width=500, height=self.video_height * 500 // self.video_width))

        self.webview = toga.WebView(style=Pack(flex=1))
        self.add(self.webview)

        html = f"""
        <html>
        <body style="margin:0;padding:0;background:black;">
            <video width="100%" height="100%" controls autoplay>
                <source src="{self.video_url}" type="video/mp4">
                Your browser doesn't support HTML5 video.
            </video>
        </body>
        </html>
        """

        print(f"Video URL: {self.video_url}")
        self.webview.set_content("text/html", html)

    def stop(self) -> None:
        self.webview.set_content("text/html", "<html></html>")

    def _get_video_dimensions(self) -> tuple[int, int]:
        """Get video dimensions using OpenCV"""
        try:
            cap = cv2.VideoCapture(self.video_url)
            if not cap.isOpened():
                print(f"Failed to open: {self.video_url}")
                return (0, 0)
            
            w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            cap.release()
            
            print(f"Video dimensions: {w}x{h}")
            return (w, h)
        except Exception as e:
            print(f"Error: {e}")
            return (0, 0)
