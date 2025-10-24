# Pokemon Legends ZA Automation Tools

This repository contains automation scripts for Pokemon Legends ZA using a Raspberry Pi 3 B+ to simulate a Nintendo Switch Pro Controller via Bluetooth. The scripts I made are still in test but get the job done. I did this using a Switch 2 but it should work with Switch 1 

# NXBT
This is using the python module [NXBT](https://github.com/Brikwerk/nxbt/tree/master) to emulate the Switch Pro Controller. 

## `scripts/fast_travel.py`
This is the main file I use to do some macros. This script does 100 fast travels to Wild Area 5, then goes to the Magenta Plaza Pokemon Center and goes to the nearest bench to pass the day/night cycle (so if you start in the day, it'll cycle for the next day and vice versa).

## Prerequisites

- Raspberry Pi 3 B+ running Raspberry Pi OS
- Python 3.11.5 (We'll use pyenv to manage this)
- Nintendo Switch1/2
- Basic knowledge of terminal commands

## Hardware Setup
*This assumes that you have already configured a Raspberry Pi*
1. Ensure your Raspberry Pi 3 B+ is properly set up with Raspberry Pi OS (or any Debian-based Linux distro)
2. Connect to your Raspberry Pi via SSH or use it with desired display 

## Software Installation

### 1. Install System Dependencies

```bash
sudo apt update
sudo apt install -y git curl build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python3-openssl \
bluetooth bluez bluez-tools rfkill
```

### 2. Install and Configure pyenv

I suggest using Pyenv because it's easier to manage Python installation.
```bash
curl https://pyenv.run | bash

# Add these lines to your ~/.bashrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# Reload shell configuration
source ~/.bashrc

# Install Python 3.11.5 (this is what worked for me)
pyenv install 3.11.5
```

### 3. Clone and Setup the Project

```bash
# Clone the repository
git clone https://github.com/Cobalt-J/sw_macros.git
cd sw_macros

# Set local Python version
pyenv local 3.11.5

# Create and activate virtual environment
python -m venv </path/for/venv>
source </path/for/venv>/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### 1. Connect to Nintendo Switch

1. On your Nintendo Switch, go to System Settings > Controllers and Sensors > Change Grip/Order
2. Run one of the scripts:

NOTE: The `sudo $(which python3)` is done so nxbt could access the Pi's hardware.
```bash
# For fast travel automation
(venv)$ sudo $(which python3) fast_travel.py

# For testing movement patterns
(venv)$ sudo $(which python3) test_movement.py
```

3. Wait for the "Connected!" message in the terminal
4. Press Enter to start the automation

### Available Scripts

- `fast_travel.py`: Performs up to 100 fast travel sequences before running a day/night cycle
- `test_movement.py`: Used for testing individual movement patterns and macros
- `fast_travel_old.py`: Legacy version with alternative implementation (not recommended for regular use)

### Stopping the Automation

- Press `Ctrl+C` in the terminal to safely stop the automation
- The script will properly disconnect the controller when stopped


Unfortunately I have not fully tested controller compatability using the PI (PS/Xbox/Switch controller -> Pi --> Switch 2)

## Safety Notes

- Always ensure your game is saved before running automation scripts
- Be mindful of your Switch's environment to prevent overheating during long automation sessions
- It's recommended to monitor the automation during its first few cycles to ensure everything works as expected
- Would not suggest having this run in Online stuff in the game

## Contributing

Feel free to submit issues or pull requests if you have improvements or bug fixes to suggest.

