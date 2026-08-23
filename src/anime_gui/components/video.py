from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


# ============================================================
# DATA
# ============================================================


@dataclass
class VideoSource:
    """
    Video source.

    url:
        Local file path or remote URL.

    title:
        Optional display title.

    thumbnail:
        Optional future poster image URL.
    """

    url: str
    title: Optional[str] = None
    thumbnail: Optional[str] = None


# ============================================================
# COMPONENT
# ============================================================


class VideoPlayer(toga.Box):
    """
    Reusable video player component.

    The component manages the complete UI and exposes a public
    API similar to a normal ImageView.

    The actual video rendering backend can later be implemented
    with GTK/GStreamer without changing the public API.
    """

    # --------------------------------------------------------
    # Constructor
    # --------------------------------------------------------

    def __init__(
        self,
        source: Optional[VideoSource] = None,
        *,
        autoplay: bool = False,
        loop: bool = False,
        show_controls: bool = True,
        on_play: Optional[Callable[["VideoPlayer"], None]] = None,
        on_pause: Optional[Callable[["VideoPlayer"], None]] = None,
        on_end: Optional[Callable[["VideoPlayer"], None]] = None,
        on_error: Optional[Callable[["VideoPlayer", Exception], None]] = None,
        style: Pack | None = None,
        id: str | None = None,
        **kwargs,
    ):
        self.source = source

        self.autoplay = autoplay
        self.loop = loop
        self.show_controls = show_controls

        self.on_play = on_play
        self.on_pause = on_pause
        self.on_end = on_end
        self.on_error = on_error

        # Player state
        self.duration = 0.0
        self.position = 0.0
        self.volume = 100
        self.playback_speed = 1.0

        self.is_playing = False
        self.is_muted = False
        self.is_loading = False
        self.has_error = False

        # ----------------------------------------------------
        # Widgets
        # ----------------------------------------------------

        self.video_surface = toga.Box(
            children=[
                toga.Label(
                    "No video loaded",
                    style=Pack(
                        font_size=16,
                    ),
                ),
            ],
            style=Pack(
                direction=COLUMN,
                flex=1,
                alignment="center",
                padding=20,
            ),
        )

        self.play_button = toga.Button(
            "▶",
            on_press=self._toggle_play_button,
            style=Pack(
                width=45,
            ),
        )

        self.stop_button = toga.Button(
            "■",
            on_press=self._stop_button,
            style=Pack(
                width=40,
            ),
        )

        self.previous_button = toga.Button(
            "⏪",
            on_press=self._previous_button,
            style=Pack(
                width=45,
            ),
        )

        self.next_button = toga.Button(
            "⏩",
            on_press=self._next_button,
            style=Pack(
                width=45,
            ),
        )

        self.time_label = toga.Label(
            "00:00 / 00:00",
            style=Pack(
                width=110,
            ),
        )

        self.progress_slider = toga.Slider(
            min=0,
            max=100,
            value=0,
            on_change=self._seek_slider,
            style=Pack(
                flex=1,
            ),
        )

        self.volume_button = toga.Button(
            "🔊",
            on_press=self._toggle_mute_button,
            style=Pack(
                width=45,
            ),
        )

        self.volume_slider = toga.Slider(
            min=0,
            max=100,
            value=100,
            on_change=self._volume_changed,
            style=Pack(
                width=120,
            ),
        )

        self.speed_button = toga.Button(
            "1x",
            on_press=self._change_speed_button,
            style=Pack(
                width=50,
            ),
        )

        self.fullscreen_button = toga.Button(
            "⛶",
            on_press=self._fullscreen_button,
            style=Pack(
                width=45,
            ),
        )

        # ----------------------------------------------------
        # Bottom controls
        # ----------------------------------------------------

        controls_top = toga.Box(
            children=[
                self.previous_button,
                self.play_button,
                self.stop_button,
                self.next_button,
                self.time_label,
                self.progress_slider,
            ],
            style=Pack(
                direction=ROW,
                alignment="center",
                padding=(8, 8, 4, 8),
            ),
        )

        controls_bottom = toga.Box(
            children=[
                self.volume_button,
                self.volume_slider,
                toga.Box(style=Pack(flex=1)),
                self.speed_button,
                self.fullscreen_button,
            ],
            style=Pack(
                direction=ROW,
                alignment="center",
                padding=(4, 8, 8, 8),
            ),
        )

        self.controls = toga.Box(
            children=[
                controls_top,
                controls_bottom,
            ],
            style=Pack(
                direction=COLUMN,
            ),
        )

        children = [
            self.video_surface,
        ]

        if show_controls:
            children.append(self.controls)

        super().__init__(
            children=children,
            style=Pack(
                direction=COLUMN,
                flex=1,
                **(style.__dict__ if style else {}),
            ),
            id=id,
            **kwargs,
        )

        self._build_idle()

    # ========================================================
    # PUBLIC API
    # ========================================================

    def set_source(
        self,
        source: VideoSource,
    ) -> None:
        """
        Replace the current video source.
        """

        self.source = source

        self.position = 0
        self.duration = 0
        self.is_playing = False
        self.has_error = False

        self._build_idle()

        if self.autoplay:
            self.play()

    def clear_source(self) -> None:
        """Remove the current video."""

        self.source = None

        self.stop()

        self._build_idle()

    def play(self) -> None:
        """Start playback."""

        if self.source is None:
            self._show_message(
                "No video selected."
            )
            return

        self.is_playing = True
        self.play_button.text = "⏸"

        self._backend_play()

        if self.on_play:
            self.on_play(self)

    def pause(self) -> None:
        """Pause playback."""

        if not self.is_playing:
            return

        self.is_playing = False
        self.play_button.text = "▶"

        self._backend_pause()

        if self.on_pause:
            self.on_pause(self)

    def toggle_play(self) -> None:
        """Toggle playback."""

        if self.is_playing:
            self.pause()
        else:
            self.play()

    def stop(self) -> None:
        """Stop playback."""

        self.is_playing = False
        self.position = 0

        self.play_button.text = "▶"

        self._backend_stop()

        self._refresh_ui()

    def seek(
        self,
        seconds: float,
    ) -> None:
        """Seek to an absolute position."""

        seconds = max(
            0,
            min(seconds, self.duration),
        )

        self.position = seconds

        self._backend_seek(seconds)

        self._refresh_ui()

    def seek_relative(
        self,
        seconds: float,
    ) -> None:
        """Seek forward or backward."""

        self.seek(
            self.position + seconds
        )

    def set_volume(
        self,
        volume: int,
    ) -> None:
        """Set volume between 0 and 100."""

        self.volume = max(
            0,
            min(volume, 100),
        )

        self.volume_slider.value = self.volume

        self.is_muted = self.volume == 0

        self._refresh_volume_icon()

        self._backend_set_volume(self.volume)

    def mute(self) -> None:
        """Mute audio."""

        self.is_muted = True

        self._backend_set_muted(True)

        self._refresh_volume_icon()

    def unmute(self) -> None:
        """Restore audio."""

        self.is_muted = False

        self._backend_set_muted(False)

        self._refresh_volume_icon()

    def toggle_mute(self) -> None:
        """Toggle mute."""

        if self.is_muted:
            self.unmute()
        else:
            self.mute()

    def set_playback_speed(
        self,
        speed: float,
    ) -> None:
        """Change playback speed."""

        self.playback_speed = speed

        self.speed_button.text = f"{speed:g}x"

        self._backend_set_speed(speed)

    def set_loop(
        self,
        enabled: bool,
    ) -> None:
        """Enable or disable looping."""

        self.loop = enabled

        self._backend_set_loop(enabled)

    def reload(self) -> None:
        """Reload the current source."""

        if self.source is None:
            return

        self.stop()

        self._backend_reload()

    def fullscreen(self) -> None:
        """Enter fullscreen mode."""

        self._backend_fullscreen()

    def snapshot(self) -> None:
        """Take a screenshot of the current frame."""

        self._backend_snapshot()

    def select_subtitle(
        self,
        track: str,
    ) -> None:
        """Select subtitle track."""

        self._backend_select_subtitle(track)

    def select_audio_track(
        self,
        track: str,
    ) -> None:
        """Select audio track."""

        self._backend_select_audio(track)

    # ========================================================
    # BACKEND EVENTS
    # ========================================================

    def backend_update_position(
        self,
        position: float,
        duration: float,
    ) -> None:
        """
        Called by the real backend every few milliseconds.
        """

        self.position = position
        self.duration = duration

        self._refresh_ui()

    def backend_finished(self) -> None:
        """Called when playback reaches the end."""

        if self.loop:
            self.seek(0)
            self.play()
            return

        self.stop()

        if self.on_end:
            self.on_end(self)

    def backend_error(
        self,
        error: Exception,
    ) -> None:
        """Called by backend on failure."""

        self.has_error = True
        self.is_playing = False

        self._build_error(error)

        if self.on_error:
            self.on_error(self, error)

    # ========================================================
    # BUTTON CALLBACKS
    # ========================================================

    async def _toggle_play_button(
        self,
        widget,
    ) -> None:
        self.toggle_play()

    async def _stop_button(
        self,
        widget,
    ) -> None:
        self.stop()

    async def _previous_button(
        self,
        widget,
    ) -> None:
        self.seek_relative(-10)

    async def _next_button(
        self,
        widget,
    ) -> None:
        self.seek_relative(10)

    async def _toggle_mute_button(
        self,
        widget,
    ) -> None:
        self.toggle_mute()

    async def _fullscreen_button(
        self,
        widget,
    ) -> None:
        self.fullscreen()

    async def _change_speed_button(
        self,
        widget,
    ) -> None:

        speeds = [
            0.5,
            0.75,
            1.0,
            1.25,
            1.5,
            2.0,
        ]

        index = speeds.index(self.playback_speed)

        index = (index + 1) % len(speeds)

        self.set_playback_speed(
            speeds[index]
        )

    async def _seek_slider(
        self,
        widget,
        value,
    ) -> None:

        if self.duration <= 0:
            return

        seconds = (
            value / 100
        ) * self.duration

        self.seek(seconds)

    async def _volume_changed(
        self,
        widget,
        value,
    ) -> None:
        self.set_volume(int(value))

    # ========================================================
    # UI
    # ========================================================

    def _build_idle(self) -> None:

        self.video_surface.clear()

        title = (
            self.source.title
            if self.source and self.source.title
            else "Video Player"
        )

        self.video_surface.add(
            toga.Label(
                title,
                style=Pack(
                    font_size=18,
                    font_weight="bold",
                    padding_bottom=10,
                ),
            )
        )

        self.video_surface.add(
            toga.Label(
                "Video renderer not connected yet",
            )
        )

        self._refresh_ui()

    def _build_error(
        self,
        error: Exception,
    ) -> None:

        self.video_surface.clear()

        self.video_surface.add(
            toga.Label(
                "Unable to play video",
                style=Pack(
                    font_size=18,
                    font_weight="bold",
                    padding_bottom=10,
                ),
            )
        )

        self.video_surface.add(
            toga.Label(str(error))
        )

    def _show_message(
        self,
        message: str,
    ) -> None:

        self.video_surface.clear()

        self.video_surface.add(
            toga.Label(message)
        )

    def _refresh_ui(self) -> None:

        if self.duration > 0:

            percentage = (
                self.position / self.duration
            ) * 100

        else:
            percentage = 0

        self.progress_slider.value = percentage

        self.time_label.text = (
            f"{self._format_time(self.position)}"
            f" / "
            f"{self._format_time(self.duration)}"
        )

        self.play_button.text = (
            "⏸"
            if self.is_playing
            else "▶"
        )

        self._refresh_volume_icon()

    def _refresh_volume_icon(self) -> None:

        if self.is_muted or self.volume == 0:
            self.volume_button.text = "🔇"

        elif self.volume < 50:
            self.volume_button.text = "🔉"

        else:
            self.volume_button.text = "🔊"

    @staticmethod
    def _format_time(
        seconds: float,
    ) -> str:

        seconds = int(seconds)

        minutes = seconds // 60
        seconds %= 60

        hours = minutes // 60
        minutes %= 60

        if hours > 0:
            return (
                f"{hours:02d}:"
                f"{minutes:02d}:"
                f"{seconds:02d}"
            )

        return (
            f"{minutes:02d}:"
            f"{seconds:02d}"
        )

    # ========================================================
    # BACKEND IMPLEMENTATION
    # ========================================================
    #
    # Everything below is intentionally empty.
    #
    # Replace these methods with GTK/GStreamer later.
    # The public API above never changes.
    #
    # ========================================================

    def _backend_play(self) -> None:
        pass

    def _backend_pause(self) -> None:
        pass

    def _backend_stop(self) -> None:
        pass

    def _backend_seek(
        self,
        seconds: float,
    ) -> None:
        pass

    def _backend_set_volume(
        self,
        volume: int,
    ) -> None:
        pass

    def _backend_set_muted(
        self,
        muted: bool,
    ) -> None:
        pass

    def _backend_set_speed(
        self,
        speed: float,
    ) -> None:
        pass

    def _backend_set_loop(
        self,
        enabled: bool,
    ) -> None:
        pass

    def _backend_reload(self) -> None:
        pass

    def _backend_fullscreen(self) -> None:
        pass

    def _backend_snapshot(self) -> None:
        pass

    def _backend_select_subtitle(
        self,
        track: str,
    ) -> None:
        pass

    def _backend_select_audio(
        self,
        track: str,
    ) -> None:
        pass
