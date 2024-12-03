from os import environ
from time import monotonic

from textual.reactive import reactive
from textual.widgets import Digits

from .var_funcs import *

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
from pygame import mixer


class Time(Digits):
    start_time = reactive(monotonic)
    time = reactive(0.0)
    total = reactive(0.0)

    def __init__(
        self,
        mode: str,
        time_list: list,
        begin: list,
        ringtone: str,
        default_time="00:00:00.00",
    ):
        self.mode = mode
        self.time_list = time_list
        self.ringtone = ringtone
        self.target_seconds = time_list[0] * 3600 + time_list[1] * 60 + time_list[2]
        self.is_reset= True
        self.default_time=default_time

        if self.mode == "in":
            self.message = "Time Up!"
        else:
            self.message = "Target time hit!"

        mixer.init()

        super().__init__(default_time)

    def compose(self) -> ComposeResult:
        return super().compose()

    def on_mount(self) -> None:
        if self.mode == "clock" or self.mode == "clock_24":
            self.update_timer = self.set_interval(1, self.update_clock)
        else:
            self.update_timer = self.set_interval(1 / 60, self.update_time)

    def update_time(self) -> None:
        if self.is_reset:
            self.start_time=monotonic()
            self.is_reset=False
        self.time = monotonic() - self.start_time
        minutes, seconds = divmod(self.time, 60)
        hours, minutes = divmod(minutes, 60)
        self.update(f"{hours:02,.0f}:{minutes:02.0f}:{seconds:05.2f}")

        if int(self.time) >= self.target_seconds:
            self.update(self.message)
            self.update_timer.pause()
            self.app.query_one("#info_text", Label).update("Press q to quit")
            self.ring()

    def update_clock(self) -> None:
        if self.mode == "clock":
            self.time = strftime(time_format)
            self.update(self.time)
            self.app.query_one("#info_text", Label).update(strftime("%p"))
        else:
            self.time = strftime(time_format_24)
            self.update(self.time)

    def pause(self) -> None:
        self.update_timer.pause()
        self.temp=monotonic()

    def resume(self)->None:
        temp2=monotonic()
        pause_duration=temp2-self.temp
        self.start_time+=pause_duration
        
        self.update_timer.resume()

    def reset(self)-> None:
        self.is_reset=True
        self.update(self.default_time)

    def ring(self) -> None:
        mixer.music.load(self.ringtone)
        mixer.music.play()
        write_default_backup()
        try:
            btn=self.app.query_one("#stop_ring_btn",Button)
            btn.styles.display="block"
            btn.disabled=False
            btn2=self.app.query_one("#pause_button",Button)
            btn2.disabled=True
            btn3=self.app.query_one("#reset_button",Button)
            btn3.disabled=True
        except:
            pass


class Pomodoro(Digits):
    def __init__(
        self, time_list: list, begin: list, ringtone: str, default_time="00:00:00.00"
    ):
        self.time_list = time_list
        self.ringtone = ringtone

        self.pomodoro_mode=begin[-2]
        self.target_seconds = config["pomodoro"][self.pomodoro_mode] * 60 
        self.completed = begin[0] * 3600 + begin[1] * 60 + begin[2]
        self.task_statement = begin[-1]
        self.pomodoro_count=0

        self.default_time=default_time
        self.started=False
        mixer.init()
        super().__init__(default_time)

    def set_task(self, task):
        self.task_statement = task

    def compose(self) -> ComposeResult:
        return super().compose()

    def start(self) -> None:
        self.time = float(self.completed)
        self.start_time = monotonic()
        self.update_timer = self.set_interval(1 / 60, self.update_time)
        self.started=True

    def update_time(self) -> None:
        self.time = (monotonic() - self.start_time) + float(self.completed)
        minutes, seconds = divmod(self.time, 60)
        hours, minutes = divmod(minutes, 60)
        self.update(f"{hours:02,.0f}:{minutes:02.0f}:{seconds:05.2f}")

        if (int(self.time) % config["general"]["backup_interval"] == 0) and (
            config["pomodoro"]["take_backups"]
        ):
            backupTime(
                f"{int(hours)},{int(minutes)},{int(seconds)},{self.pomodoro_mode}", self.task_statement
            )
        if (int(self.time)>=self.target_seconds):
            self.update_timer.pause()
            write_default_backup()
            self.ring()

    def pause(self) -> None:
        self.update_timer.pause()
        self.temp=monotonic()

    def resume(self)->None:
        temp2=monotonic()
        pause_duration=temp2-self.temp
        self.start_time+=pause_duration
        self.update_timer.resume()

    def reset(self)-> None:
        self.is_reset=True
        self.update(self.default_time)
        self.completed=0
        write_default_backup()

    def ring(self):
        mixer.music.load(self.ringtone)
        mixer.music.play()
        write_default_backup()
        try:
            btn=self.app.query_one("#stop_ring_btn",Button)
            btn.styles.display="block"
            btn.disabled=False
            btn2=self.app.query_one("#pause_button",Button)
            btn2.disabled=True
            btn3=self.app.query_one("#reset_button",Button)
            btn3.disabled=True
        except:
            pass

