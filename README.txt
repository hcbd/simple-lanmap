

What is this?

A very visual lan monitor that should be fast and simple to setup.
functions not working yet include a automated device/network scanner and a gui node-editor.


What you need to make this code work at this moment: 

- Linuxsystem with Ping installed (tested on Debain 8.2 and Mint 17.2)
- python 3
- python PIL lib (need to dump this lib, is hard for windows users to install)
- sudo apt install python3-pil.imagetk
- Tkinter
- (probably forgot things here)


How to use:

run in terminal: python3 __init__.py


How to config:

check out the settings.ini file for the settings and networknodes


included are 2 config examples:

- the current settings.ini file
- the default config (rename or delete the settings.ini file)


TODO:

- make a gui for editing nodes in the network
- make a gui for scanning a network for devices to quickly map a network and name devices
- add MSWindows support
- Clean up and simplify GUI as much as possible.
- Clean up code in general
