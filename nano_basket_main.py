#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Nano Basket
#   Copyright (C) 2011 Roy Vegard Ovesen <roy.vegard.ovesen@gmail.com>


#   This file is part of Nano Basket.
#
#   Nano Basket is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Nano Basket is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Nano Basket.  If not, see <http://www.gnu.org/licenses/>.

from nano_basket_gui import NanoKontrolGui
from nano_basket_backend import NanoKontrolScene, NanoKontrolAlsaMidiComm

Scene_1 = NanoKontrolScene()
Scene_2 = NanoKontrolScene()
Scene_3 = NanoKontrolScene()
Scene_4 = NanoKontrolScene()
Clipboard_Scene = NanoKontrolScene()

Scenes = [Scene_1, Scene_2, Scene_3, Scene_4, Clipboard_Scene]
Midi_Device = NanoKontrolAlsaMidiComm()

Gui = NanoKontrolGui(Scenes, Midi_Device)
Gui.main()
