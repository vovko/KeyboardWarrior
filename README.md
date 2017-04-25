# Keyboard Warrior

Status: *WORK IN PROGRESS* (red explosions)

![keyboard_warrior_key_count](http://i.imgur.com/sgsG3C7.gif)

This project is a visual presentation of your keyboard performance, similarly to http://codeinthedark.com/editor/, Keyboard Warrior counts your keystrokes, time difference in between key presses, combo hits and time since last keyboard activity.

Current implementation is a bit naive and is subject to change in future.

[`logkeys`](https://github.com/kernc/logkeys) tracks your keyboard presses and outputs into log file. (For security reasons keymap provided to `logkeys` maps each key to a Zero)

Python app tracks changes of output file and counts time in between changes to the file.

*Note*: On Mac OS I could not get file's modified time narrowed down to a millisecond
