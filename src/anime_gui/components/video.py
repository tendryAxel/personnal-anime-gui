import toga
from toga.style import Pack


class VideoView(toga.Box):
    video_filename: str
    webview: toga.WebView

    def __init__(self, video_filename: str):
        super().__init__(style=Pack(flex=1))

        self.video_filename = video_filename
        self.webview = toga.WebView(style=Pack(flex=1))
        self.add(self.webview)

        # Use localhost HTTP server (started by app)
        video_url = f"http://localhost:8765/{video_filename}"

        html = f"""
        <html>
        <body style="margin:0;padding:0;background:black;">
            <video width="100%" height="100%" controls autoplay>
                <source src="{video_url}" type="video/mp4">
                Your browser doesn't support HTML5 video.
            </video>
        </body>
        </html>
        """

        print(f"Video URL: {video_url}")
        self.webview.set_content("text/html", html)

    def stop(self) -> None:
        self.webview.set_content("text/html", "<html></html>")
