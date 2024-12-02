from typing import Set

from widgets import *

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
        ("q", "quit_app", "Quits the application"),
        ("d", "toggle_dark", "Toggles dark mode"),
        ("m", "stop_ring", "Stops alarm sound"),
    ]
    CSS_PATH = "remime.tcss"

    def __init__(
        self, mode: str, fg: str, bg: str, time_list: list, begin: list, ringtone: str
    ):
        self.mode = mode
        self.fg = fg
        self.bg = bg
        self.completed = begin[0] * 3600 + begin[1] * 60 + begin[2]
        self.target_label = ""
        if mode == "clock":

            self.wdg = Time(
                mode, time_list, begin, ringtone, default_time=strftime(time_format)
            )
        elif mode == "clock_24":
            self.wdg = Time(
                mode, time_list, begin, ringtone, default_time=strftime(time_format_24)
            )
        elif mode == "pomodoro":

            self.target_label = f"Target -> {time_list[0]:02,.0f}:{time_list[1]:02,.0f}:{time_list[2]:02,.0f}.00"
            self.wdg = Pomodoro(time_list, begin, ringtone, default_time="00:00:00.00")
            self.time_list = "Next"
        elif mode == "stopwatch":
            self.wdg = Time(mode, [float("inf"), 0, 0], begin, ringtone)
        else:
            self.target_label = f"Target -> {time_list[0]:02,.0f}:{time_list[1]:02,.0f}:{time_list[2]:02,.0f}.00"
            self.wdg = Time(mode, time_list, begin, ringtone)

        if config["general"]["target_time_label"]:
            self.info = Label(self.target_label, id="info_text")
        else:
            self.info = Label("", id="info_text")

        super().__init__()

    def compose(self) -> ComposeResult:
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
                Horizontal(
                    Button("Pause", id="pause_button"),
                    self.info,
                    Button("Reset", id="reset_button"),
                ),
            )

        if mode == "stopwatch":
            self.info.update("Stopwatch Started!")
            yield Vertical(
                self.wdg,
                Horizontal(
                    Button("Pause", id="pause_button"),
                    self.info,
                    Button("Reset", id="reset_button"),
                ),
            )
        else:
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

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def action_quit_app(self) -> None:
        self.exit()
        exit()

    def action_stop_ring(self) -> None:
        mixer.music.stop()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "task_input":
            self.inputBox.disabled = True
            self.wdg.set_task(self.inputBox.value)
            self.wdg.start()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn = event.button
        btn_id = event.button.id
        if btn_id == "pause_button":
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
        if btn_id == "reset_button":
            self.wdg.pause()
            self.wdg.reset()
            if self.mode=="pomodoro":
                self.inputBox.disabled=False
                self.inputBox.value = ""
            else:
                self.info.update("Stopwatch has been reset")


if __name__ == "__main__":
    a = ArgumentParser(
        prog="Remime",
        description="An easy to use TUI application to manage time efficiently",
        usage="remime [mode] [options] [values]",
    )
    a.add_argument(
        "-at",
        "--at",
        help="Set an alarm at a particular time, takes 24hr clock input",
        action="store_true",
    )
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
    elif args.at:
        mode = "at"
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

    notui = ["-h", "--help", "-rb", "--remove-backup"]
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
    if args.remove_backup:
        write_default_backup()
    else:
        a.print_help()
