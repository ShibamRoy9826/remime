from textual.binding import Binding
from textual.widgets import Footer, Header

from .widgets import *

catppuccin = Theme(
    name="catppuccin",
    primary="#89b4fa",
    secondary="#a6e3a1",
    accent="#89b4fa",
    foreground="#cdd6f4",
    background="#1e1e2e",
    success="#a6e3a1",
    warning="#f9e2af",
    error="#f38ba8",
    surface="#313244",
    panel="#45475a",
    dark=True,
    variables={
        "block-cursor-text-style": "none",
        "footer-key-foreground": "#1e1e2e",
        "input-selection-background": "#81a1c1 35%",
    },
)


class Remime(App):
    BINDINGS = [
        Binding("q", "quit_app", "Quits The Application"),
        Binding("d", "toggle_dark", "Toggles Dark Mode"),
        Binding("m", "stop_ring", "To Mute The Alarm"),
        Binding("p", "pause_time","To Pause Alarm Time"),
        Binding("r", "reset_time","To Reset Alarm Time")
    ]

    CSS_PATH = css_path

    def __init__(
        self, mode: str, fg: str, bg: str, time_list: list, begin: list, ringtone: str
    ):
        self.mode = mode
        self.fg = fg
        self.bg = bg
        self.completed = begin[0] * 3600 + begin[1] * 60 + begin[2]
        self.target_label = ""
        self.header_icon="󰍜"
        if mode == "clock":

            self.wdg = Time(
                mode, time_list, begin, ringtone, default_time=strftime(time_format)
            )
        elif mode == "clock_24":
            self.wdg = Time(
                mode, time_list, begin, ringtone, default_time=strftime(time_format_24)
            )
        elif mode == "pomodoro":
            self.target_label = f"Target -> {time_list[0]:02,.0f}:{time_list[1]:02,.0f}:{time_list[2]:02,.0f}"
            self.wdg = Pomodoro(time_list, begin, ringtone, default_time="00:00:00.00")
            self.time_list = "Next"

        elif mode == "stopwatch":
            self.wdg = Time(mode, [float("inf"), 0, 0], begin, ringtone)
        else:
            self.target_label = f"Target -> {time_list[0]:02,.0f}:{time_list[1]:02,.0f}:{time_list[2]:02,.0f}"
            self.wdg = Time(mode, time_list, begin, ringtone)

        if config["general"]["target_time_label"]:
            self.info = Label(self.target_label, id="info_text")
        else:
            self.info = Label("", id="info_text")

        self.stopRingingBtn=Button("Stop Ringing!",id="stop_ring_btn",disabled=True)
        self.stopRingingBtn.styles.display="none"

        super().__init__()

    def compose(self) -> ComposeResult:
        if config["general"]["header"]:
            yield Header(icon=self.header_icon)

        if config["general"]["footer"]:
            yield Footer(show_command_palette=False)

        if mode == "pomodoro":
            if self.completed != 0:
                self.inputBox = Input(value=begin[4], type="text", id="task_input")
                self.inputBox.disabled = True
                self.wdg.start()
            else:
                self.inputBox = Input(
                    placeholder="What did you plan to do?", type="text", id="task_input"
                )
            yield Vertical(
                self.inputBox,
                self.wdg,
                self.info,
                Horizontal(
                    Button("Pause", id="pause_button"),
                    Button("Reset", id="reset_button"),
                ),
                Horizontal(
                    Button("Pomodoro", id="pomodoro_btn"),
                    Button("Short Break", id="short_break_btn"),
                    Button("Long Break", id="long_break_btn"),
                    self.stopRingingBtn,
                ),
            )



        if mode == "stopwatch":
            self.info.update("Stopwatch Started!")
            yield Vertical(
                self.wdg,
                self.stopRingingBtn,
                Horizontal(
                    Button("Pause", id="pause_button"),
                    self.info,
                    Button("Reset", id="reset_button"),
                ),
            )
        else:
            yield self.stopRingingBtn
            yield Vertical(self.wdg, self.info)


    def on_mount(self) -> None:
        self.register_theme(catppuccin)
        self.theme = "catppuccin"
        self.wdg.styles.color = self.fg
        self.wdg.styles.background = self.bg
        if config["general"]["border_enabled"]:
            self.wdg.styles.border = (
                config["general"]["border_type"],
                config["general"]["border_color"],
            )
            self.wdg.border_title = config["general"]["custom_message"]
        if self.mode=="pomodoro":
            self.start_pomodoro()

    def start_pomodoro(self):
        if self.wdg.started:
            self.wdg.pause()
            self.wdg.reset()

        self.inputBox.value=""
        self.inputBox.disabled=False
        pomodoro_minutes=config["pomodoro"]["pomodoro"]
        self.wdg.target_seconds=pomodoro_minutes*60
        self.target_label=f"Target -> {pomodoro_minutes//60:02,.0f}:{pomodoro_minutes%60:02,.0f}:00"
        self.info.update(self.target_label)

    def start_short_break(self):
        if self.wdg.started:
            self.wdg.pause()
            self.wdg.reset()
        self.inputBox.value="Short break"
        self.inputBox.disabled=True
        short_min=config["pomodoro"]["short_break"]
        self.wdg.target_seconds=short_min*60
        self.target_label=f"Target -> {short_min//60:02,.0f}:{short_min%60:02,.0f}:00"
        self.info.update(self.target_label)
        self.wdg.start()

    def start_long_break(self):
        if self.wdg.started:
            self.wdg.pause()
            self.wdg.reset()
        self.inputBox.value="Long break"
        self.inputBox.disabled=True
        long_min=config["pomodoro"]["long_break"]
        self.wdg.target_seconds=long_min*60
        self.target_label=f"Target -> {long_min//60:02,.0f}:{long_min%60:02,.0f}:00"
        self.info.update(self.target_label)
        self.wdg.start()

    def pause_time(self,btn):
        if self.mode=="pomodoro":
            if self.wdg.started and self.inputBox.disabled:
                if str(btn.label) == "Pause":
                    btn.label = "Start"
                    btn.styles.background = self.theme_variables.get("secondary")
                    self.wdg.pause()
                    self.info.update(f"{self.target_label} (paused)")
                else:
                    btn.label = "Pause"
                    btn.styles.background = self.theme_variables.get("error")
                    self.wdg.resume()
                    self.info.update(self.target_label)
        elif self.mode=="stopwatch":
            if str(btn.label) == "Pause":
                btn.label = "Start"
                btn.styles.background = self.theme_variables.get("secondary")
                self.info.update("Paused stopwatch...")
                self.wdg.pause()
            else:
                btn.label = "Pause"
                btn.styles.background = self.theme_variables.get("error")
                self.info.update("Stopwatch Started!")
                self.wdg.resume()
    def reset_time(self):
        if self.mode=="pomodoro":
            if self.wdg.started:
                self.wdg.pause()
                self.wdg.reset()
            self.inputBox.disabled=False
            self.inputBox.value = ""
        elif self.mode=="stopwatch":
            self.wdg.pause()
            self.wdg.reset()
            self.info.update("Stopwatch has been reset")
    def action_pause_time(self) -> None:
        try:
            b=self.query_one("#pause_button",Button)
            self.pause_time(b)
        except:
            pass

    def action_reset_time(self) -> None:
        try:
            self.reset_time()
        except:
            pass

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def action_quit_app(self) -> None:
        self.exit()
        exit()

    def action_stop_ring(self) -> None:
        if mixer.music.get_busy:
            mixer.music.stop()
            self.stopRingingBtn.styles.display="none"
            self.stopRingingBtn.disabled=True
            try:
                if self.mode=="pomodoro":
                    if config["pomodoro"]["automatic_mode_change"]:
                        m=self.wdg.pomodoro_mode
                        btn2=self.app.query_one("#pause_button",Button)
                        btn2.disabled=False
                        btn3=self.app.query_one("#reset_button",Button)
                        btn3.disabled=False
                        if self.wdg.pomodoro_count==config["pomodoro"]["total_pomodoros"]:
                            self.start_long_break()
                        elif m=="long_break":
                            self.wdg.pomodoro_count=0
                            self.wdg.pomodoro_mode="pomodoro"
                            self.start_pomodoro()
                        else:
                            if m=="pomodoro":
                                self.wdg.pomodoro_mode="short_break"
                                self.start_short_break()
                            elif m=="short_break":
                                self.wdg.pomodoro_mode="pomodoro"
                                self.wdg.pomodoro_count+=1
                                self.start_pomodoro()
                    else:
                        self.wdg.pomodoro_mode="pomodoro"
                        self.start_pomodoro()
                else:
                    self.wdg.pomodoro_mode="pomodoro"
                    self.start_pomodoro()

                        

            except:
                pass

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "task_input":
            self.inputBox.disabled = True
            self.wdg.set_task(self.inputBox.value)
            self.wdg.start()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn = event.button
        btn_id = event.button.id
        if btn_id == "pause_button":
            self.pause_time(btn)

        if btn_id == "reset_button":
            self.reset_time()

        if btn_id == "pomodoro_btn":
            self.start_pomodoro()

        if btn_id == "short_break_btn":
            self.start_short_break()

        if btn_id == "long_break_btn":
            self.start_long_break()
        if btn_id == "stop_ring_btn":
            self.action_stop_ring()
            btn.styles.display="none"




if __name__ == "__main__":
    a = ArgumentParser(
        prog="Remime",
        description="An easy to use TUI application to manage time efficiently",
        usage="remime [mode] [options] [values]",
        epilog="The configuration file for remime can be found at $HOME/.config/remime/config.toml"
    )
    # a.add_argument(
    #     "-at",
    #     "--at",
    #     help="Set an alarm at a particular time, takes 24hr clock input",
    #     action="store_true",
    # )
    a.add_argument(
        "-in",
        "--intime",
        help="Set a timer, requires -hr,-m, and -s parameters",
        action="store_true",
    )
    a.add_argument(
        "-p",
        "--pomodoro",
        help="Starts a pomodoro timer for extra work efficiency",
        action="store_true",
    )
    a.add_argument("-stop", "--stopwatch", help="Starts stopwatch", action="store_true")
    a.add_argument("-c", "--clock", help="Starts a 12 hour clock", action="store_true")
    a.add_argument(
        "-c24", "--clock-24", help="Starts a 24 hour clock", action="store_true"
    )
    a.add_argument(
        "-rb",
        "--remove-backup",
        help="Removes backup timing if present",
        action="store_true",
    )
    a.add_argument(
        "-rc",
        "--reset-config",
        help="Resets configuration file",
        action="store_true",
    )
    a.add_argument(
        "-fg",
        "--foreground",
        type=str,
        help="Sets clock foreground color, takes input in hex code",
        default="#cdd6f4",
    )
    a.add_argument(
        "-bg",
        "--background",
        type=str,
        help="Sets clock background color, takes input in hex code",
        default="#11111b",
    )
    a.add_argument(
        "-m",
        "--minutes",
        help="Sets minutes if required by current mode",
        default=config["timer"]["default_min"],
    )
    a.add_argument(
        "-hr",
        "--hours",
        help="Sets hours if required by current mode",
        default=config["timer"]["default_hour"],
    )
    a.add_argument(
        "-s",
        "--seconds",
        help="Sets minutes if required by current mode",
        default=config["timer"]["default_sec"],
    )
    a.add_argument(
        "-r",
        "--ringtone",
        help="Sets ringtone for the alarm",
        type=str,
        default=config["general"]["ringtone_path"],
    )

    args = a.parse_args()

    if args.pomodoro:
        mode = "pomodoro"
    elif args.intime:
        mode = "in"
    # elif args.at:
    #     mode = "at"
    elif args.clock_24:
        mode = "clock_24"
    elif args.stopwatch:
        mode = "stopwatch"
    else:
        mode = "clock"

    timeList = [args.hours, args.minutes, args.seconds]
    begin = []

    if mode == "pomodoro":
        bckp = readBackup()
    else:
        bckp = readBackup(False)

    for ind, j in enumerate(bckp[1]):
        if ind == 3:
            begin.append(j.replace("\n", ""))
        else:
            begin.append(int(j))

    begin.append(bckp[0])

    for ind, i in enumerate(timeList):
        timeList[ind] = int(i)

    notui = ["-h", "--help", "-rb", "--remove-backup","-rc","--reset-config"]
    is_notui = False
    for i in notui:
        if i in argv:
            is_notui = True
            break

    if not is_notui:
        app = Remime(
            mode, args.foreground, args.background, timeList, begin, args.ringtone
        )
        app.run()
    elif args.remove_backup:
        a=ask("Are you sure you want to remove your backup timing?")
        if a:
            write_default_backup()
        else:
            print("Aborted...")

    elif args.reset_config:
        a=ask("Are you sure you want to reset your config?")
        if a:
            write_default_conf()
        else:
            print("Aborted...")

    elif args.help:
        a.print_help()
