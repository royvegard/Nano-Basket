# -*- coding: utf-8 -*-
from nano_basket_gui import *
from nano_basket_backend import *

Scene_1 = Nano_Kontrol_Scene()
Scene_2 = Nano_Kontrol_Scene()
Scene_3 = Nano_Kontrol_Scene()
Scene_4 = Nano_Kontrol_Scene()

Scenes = [Scene_1, Scene_2, Scene_3, Scene_4]

Gui = Nano_Kontrol_Gui(Scenes)
Gui.main()
