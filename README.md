# Remime

An easy and efficient way to manage your time using the terminal! 

written with ❤️  in Python and [textual](https://github.com/textualize/textual/) :)

> [!NOTE]
> This application is a little buggy right now, but still usable, I am working with my best on it! Any contribution will be appreciated!
> Please report the bugs if you see them!

## Features 😎

- A Pomodoro mode, with an automatic breaks option (Customizable)
- It can take backups of your timer, so incase you exit by mistake, the next time you open it, you will almost be on the same place!
- Highly customizable overall
- Multiple themes that [textual](https://github.com/textualize/textual/) provides 
- Modes include: Stopwatch, Clock, 24-hour Clock, Timer, and Pomodoro
- Keybindings for almost everything! not customizable at the moment but planning to work on that on the next update!

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

## Dependencies

The dependencies include: 

- [textual](https://github.com/textualize/textual/)

- [toml](https://pypi.org/project/toml/)

- [pygame](https://github.com/pygame/pygame) (For the audio)

Although the dependencies will be automatically installed while installing the application, if you still want to install these dependencies manually, you can checkout the `requirements.txt` file. and run `pip install -r requirements.txt`
If you want to use something other than feh or swww, you can do that by enabling `other` in the configuration file, and setting the cmd parameter

<h2>
    Installation <img src="https://github.com/Anmol-Baranwal/Cool-GIFs-For-GitHub/assets/74038190/7b282ec6-fcc3-4600-90a7-2c3140549f58" width="30">
</h2>

If you're on Arch Linux, like me, then you can install it from the AUR:
```bash
paru -S remime
```

There's also a development version to check out the latest changes:
```bash
paru -S remime-git
```
Make sure to replace `paru` with whatever AUR helper you use.

For other distros try (installs locally to the user):
```bash
python setup.py install --user
```
if you want to install it systemwide, you can try:
```bash
sudo python setup.py install
```

If your distro allows python package installation directly using pip,
You can install EasyFeh by cloning this repository locally.
Here's the command:
```bash
git clone https://github.com/ShibamRoy9826/remime.git
cd remime
pip install .
```
That's it! read the usage of the commands and enjoy!

## Configuration 🛠️

The configuration file for remime can be found at `$HOME/.config/remime/config.toml`
Its well-commented with explaination of each parameter. Here's the default configuration file of remime

```text
[general]
# Edit to some other ringtone if you want a different alarm sound 
ringtone_path="/home/{username}/.config/remime/digital_clock.mp3" 
# Whether to display a border around the clock
border_enabled=true 

# Border type, read at: https://textual.textualize.io/styles/border/#all-border-types
border_type="round"  

# Border color
border_color="#cdd6f4" 
custom_message="Either you run the day, or the day runs you!" # Custom message that you may want to have around the clock border
                                                              # Keep "" if you don't want this
# Format of clock when called --clock (12 hour clock)
time_format="%I:%M:%S" 
# Format of clock when called --clock-24 (24 hour clock)
time_format_24="%H:%M:%S" 
## Still under work, will not work properly
target_time_label=true 
# Number of seconds after which it will save the time, requires take_backups=true
backup_interval=5 
header=false # To toggle the header widget
footer=false # To toggle the footer widget

[pomodoro]
# Pomodoro time (in minutes)
pomodoro=25  
# Short break time (in minutes)
short_break=5  
# Long break time (in minutes)
long_break=20  
# Automatically change modes from pomodoro to short_break, and occasionally long_breaks
automatic_mode_change=true 
# Take time backups, if you quit the application by mistake, and reopen it, you will be almost on the same place! (depends on backup_interval)
take_backups=true 
# Total number of pomodoros, each pomodoro consits of 1 working session, and a short_break. After total_pomodoros, a long break timer starts
total_pomodoros=4 

[timer]
# Default hours when no time is specified while calling --in
default_hour=0 
# Default minutes when no time is specified while calling --in
default_min=0 
# Default seconds when no time is specified while calling --in
default_sec=0 
## Working on it, doesn't work for now..
take_backups=true 
```

<h2>
    Usage <img src="https://github.com/Anmol-Baranwal/Cool-GIFs-For-GitHub/assets/74038190/7b282ec6-fcc3-4600-90a7-2c3140549f58" width="30">
</h2>

Here's a list of all the commands 
```text
Remime
__________

Typical Usage: remime -[mode] -[options]
╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ remime -h     -> show this help message and exit                                                                                            │
│ or remime --help                                                                                                                            │
│                                                                                                                                             │
│ remime -in     -> Set a timer, requires -hr,-m, and -s parameters                                                                           │
│ or remime --intime                                                                                                                          │
│                                                                                                                                             │
│ remime -p     -> Starts a pomodoro timer for extra work efficiency                                                                          │
│ or remime --pomodoro                                                                                                                        │
│                                                                                                                                             │
│ remime -stop     -> Starts stopwatch                                                                                                        │
│ or remime --stopwatch                                                                                                                       │
│                                                                                                                                             │
│ remime -c     -> Starts a 12 hour clock                                                                                                     │
│ or remime --clock                                                                                                                           │
│                                                                                                                                             │
│ remime -c24     -> Starts a 24 hour clock                                                                                                   │
│ or remime --clock-24                                                                                                                        │
│                                                                                                                                             │
│ remime -rb     -> Removes backup timing if present                                                                                          │
│ or remime --remove-backup                                                                                                                   │
│                                                                                                                                             │
│ remime -rc     -> Resets configuration file                                                                                                 │
│ or remime --reset-config                                                                                                                    │
│                                                                                                                                             │
│ remime -fg     -> Sets clock foreground color, takes input in hex code                                                                      │
│ or remime --foreground                                                                                                                      │
│                                                                                                                                             │
│ remime -bg     -> Sets clock background color, takes input in hex code                                                                      │
│ or remime --background                                                                                                                      │
│                                                                                                                                             │
│ remime -m     -> Sets minutes if required by current mode                                                                                   │
│ or remime --minutes                                                                                                                         │
│                                                                                                                                             │
│ remime -hr     -> Sets hours if required by current mode                                                                                    │
│ or remime --hours                                                                                                                           │
│                                                                                                                                             │
│ remime -s     -> Sets minutes if required by current mode                                                                                   │
│ or remime --seconds                                                                                                                         │
│                                                                                                                                             │
│ remime -r     -> Sets ringtone for the alarm                                                                                                │
│ or remime --ringtone                                                                                                                        │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

The configuration file for remime can be found at $HOME/.config/remime/config.toml
```

<h2>
    Keybindings <img src="https://github.com/Anmol-Baranwal/Cool-GIFs-For-GitHub/assets/74038190/7b282ec6-fcc3-4600-90a7-2c3140549f58" width="30">
</h2>

Here's a list of all the default keybindings
```text
q -> Quits the application
d -> Toggles dark mode
m -> Mutes the alarm sound
p -> Pause/Resume the alarm
r -> Reset the alarm
```
But you can also change this bindings from your configuration file!

> [!NOTE]
> Fun Fact: The name Remime actually stands for "REMInd ME"

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

## To-Do 🛠️
- Configurable buttons(To manually disable or enable buttons)
- Nice quotes on top of clock border
- Work on a lightweight alternative for the audio
- Configurable alarm messages and target labels

## Known bugs 🐞
- Doesn't backup break timing properly
- occasionally shows wrong target labels, even when the original target time is correct.(In automatic pomodoro mode)

## Contributing 🤝

Everyone is welcome to contribute to the code!

You can also raise an issue, or suggest any features that you think would be great :)

> ✨ Please star this repository if you liked this project 😁
