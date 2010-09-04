# -*- coding: utf-8 -*-

#   Nano Basket
#   Copyright (C) 2010 Roy Vegard Ovesen <roy.v.ovesen@haugnett.no>


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

from nano_basket_gui import *
from nano_basket_backend import *

Scene_1 = Nano_Kontrol_Scene()
Scene_2 = Nano_Kontrol_Scene()
Scene_3 = Nano_Kontrol_Scene()
Scene_4 = Nano_Kontrol_Scene()

Scenes = [Scene_1, Scene_2, Scene_3, Scene_4]
Midi_Device = Nano_Kontrol_Alsa_Midi_Comm()

Gui = Nano_Kontrol_Gui(Scenes, Midi_Device)
Gui.main()
