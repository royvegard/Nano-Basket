# Nano Basket

An effort to create configuration software for the Korg nanoSERIES
MIDI controllers.

Written in Python, using PyGObject for GUI and pyalsa for MIDI.

## Features
- Change all available settings to the Korg nanoKONTROL
- Download and upload to the Korg nanoKONTROL
- ALSA MIDI control
- Emulates the nanoKONTROL, i.e you can control your DAW with Nano Basket

## Dependencies
- PyGObject https://pygobject.readthedocs.io/en/latest/
- pyalsa http://www.alsa-project.org/main/index.php/Main_Page

PyGObject is available from pypi: ```pip install PyGObject```

pyalsa is not available from pypi, but is packaged by at least Debian (python3-pyalsa) and Arch (python-pyalsa)

## Usage 
Open a terminal in the folder these files are, then run:
python ./nano_basket_main.py

Perhaps try if you have errors with the above command:
python3 ./nano_basket_main.py
