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

import copy
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Nano_Kontrol_Gui:

   def delete_event(self, widget, event, data=None):
      Gtk.main_quit()
      return False

   def Focus_Event(self, widget, event, data=None):
      """Triggered when the focus-in-event is sent, i.e. whenever we need to change
      the control widgets."""

      print('Focus_Event')
      self.Current_Widget = data['Widget']
      self.Current_Widget_Type = data['Widget_Type']
      #widget.modify_text(state=Gtk.STATE_ACTIVE, color=Gtk.gdk.Color(red=0, green=65535, blue=0, pixel=0))

      # Show the appropriate control widgets.
      if (self.Current_Widget_Type == 'Slider'):
         self.Current_Block = data['Block']
         self.Button_Control_Table.hide()
         self.Transport_Control_Table.hide()
         self.Slider_Knob_Control_Table.show()
         self.Block_Midi_Channel.set_active(self.Scene[self.Current_Scene].Block[self.Current_Block].Block_Midi_Channel)
      elif (self.Current_Widget_Type == 'Button'):
         self.Current_Block = data['Block']
         self.Slider_Knob_Control_Table.hide()
         self.Transport_Control_Table.hide()
         self.Button_Control_Table.show()
         self.Block_Midi_Channel.set_active(self.Scene[self.Current_Scene].Block[self.Current_Block].Block_Midi_Channel)
      elif (self.Current_Widget_Type == 'Transport'):
         self.Slider_Knob_Control_Table.hide()
         self.Button_Control_Table.hide()
         self.Transport_Control_Table.show()

      # Read values from the backend datastore into the control widgets.
      self.Scene_Midi_Channel.set_active(self.Scene[self.Current_Scene].Common.Scene_Midi_Channel)
      self.Scene_Name.set_text(text=self.Scene[self.Current_Scene].Common.Scene_Name)
      self.Transport_Midi_Channel.set_active(self.Scene[self.Current_Scene].Transport_Midi_Channel)

      if (self.Current_Widget == 'Slider'):
         self.Slider_Assign_Type.set_active(self.Scene[self.Current_Scene].Block[self.Current_Block].Slider_Assign_Type)
         self.Slider_CC.set_value(self.Scene[self.Current_Scene].Block[self.Current_Block].Slider_CC)
         self.Slider_Min_Value.set_value(self.Scene[self.Current_Scene].Block[self.Current_Block].Slider_Min_Value)
         self.Slider_Max_Value.set_value(self.Scene[self.Current_Scene].Block[self.Current_Block].Slider_Max_Value)
      elif (self.Current_Widget == 'Knob'):
         self.Slider_Assign_Type.set_active(self.Scene[self.Current_Scene].Block[self.Current_Block].Knob_Assign_Type)
         self.Slider_CC.set_value(self.Scene[self.Current_Scene].Block[self.Current_Block].Knob_CC)
         self.Slider_Min_Value.set_value(self.Scene[self.Current_Scene].Block[self.Current_Block].Knob_Min_Value)
         self.Slider_Max_Value.set_value(self.Scene[self.Current_Scene].Block[self.Current_Block].Knob_Max_Value)
      elif (self.Current_Widget == 'Button_A'):
         self.Button_Assign_Type.set_active(self.Scene[self.Current_Scene].Block[self.Current_Block].SW_A_Assign_Type)
         self.Button_CC.set_value(self.Scene[self.Current_Scene].Block[self.Current_Block].SW_A_CC)
         self.Button_Off_Value.set_value(self.Scene[self.Current_Scene].Block[self.Current_Block].SW_A_Off_Value)
         self.Button_On_Value.set_value(self.Scene[self.Current_Scene].Block[self.Current_Block].SW_A_On_Value)
         self.Button_Attack_Time.set_value(self.Scene[self.Current_Scene].Block[self.Current_Block].SW_A_Attack_Time)
         self.Button_Release_Time.set_value(self.Scene[self.Current_Scene].Block[self.Current_Block].SW_A_Release_Time)
         self.Button_Switch_Type.set_active(self.Scene[self.Current_Scene].Block[self.Current_Block].SW_A_Switch_Type)
      elif (self.Current_Widget == 'Button_B'):
         self.Button_Assign_Type.set_active(self.Scene[self.Current_Scene].Block[self.Current_Block].SW_B_Assign_Type)
         self.Button_CC.set_value(self.Scene[self.Current_Scene].Block[self.Current_Block].SW_B_CC)
         self.Button_Off_Value.set_value(self.Scene[self.Current_Scene].Block[self.Current_Block].SW_B_Off_Value)
         self.Button_On_Value.set_value(self.Scene[self.Current_Scene].Block[self.Current_Block].SW_B_On_Value)
         self.Button_Attack_Time.set_value(self.Scene[self.Current_Scene].Block[self.Current_Block].SW_B_Attack_Time)
         self.Button_Release_Time.set_value(self.Scene[self.Current_Scene].Block[self.Current_Block].SW_B_Release_Time)
         self.Button_Switch_Type.set_active(self.Scene[self.Current_Scene].Block[self.Current_Block].SW_B_Switch_Type)
      elif (self.Current_Widget in range(6)):
         self.Transport_Assign_Type.set_active(self.Scene[self.Current_Scene].Transport_Button[self.Current_Widget].Assign_Type)
         self.Transport_CC.set_value(self.Scene[self.Current_Scene].Transport_Button[self.Current_Widget].CC)
         self.Transport_MMC_Command.set_active(self.Scene[self.Current_Scene].Transport_Button[self.Current_Widget].MMC_Command)
         self.Transport_MMC_Dev_ID.set_value(self.Scene[self.Current_Scene].Transport_Button[self.Current_Widget].MMC_Device_ID)
         self.Transport_Switch_Type.set_active(self.Scene[self.Current_Scene].Transport_Button[self.Current_Widget].Switch_Type)

      # Emphasize the current widget.
      if (widget):
         Highlight_Color = Gtk.Gdk.Color(red=0, green=65535, blue=0, pixel=0)
         Normal_Color = self.Scene_Button.get_style().bg[0]

         for child in self.Transport_Table.get_children():
            child.modify_bg(state=Gtk.STATE_NORMAL, color=Normal_Color)

         for child in self.Block_1_Table.get_children():
            child.modify_bg(state=Gtk.STATE_NORMAL, color=Normal_Color)

         for child in self.Block_2_Table.get_children():
            child.modify_bg(state=Gtk.STATE_NORMAL, color=Normal_Color)

         for child in self.Block_3_Table.get_children():
            child.modify_bg(state=Gtk.STATE_NORMAL, color=Normal_Color)

         for child in self.Block_4_Table.get_children():
            child.modify_bg(state=Gtk.STATE_NORMAL, color=Normal_Color)

         for child in self.Block_5_Table.get_children():
            child.modify_bg(state=Gtk.STATE_NORMAL, color=Normal_Color)

         for child in self.Block_6_Table.get_children():
            child.modify_bg(state=Gtk.STATE_NORMAL, color=Normal_Color)

         for child in self.Block_7_Table.get_children():
            child.modify_bg(state=Gtk.STATE_NORMAL, color=Normal_Color)

         for child in self.Block_8_Table.get_children():
            child.modify_bg(state=Gtk.STATE_NORMAL, color=Normal_Color)

         for child in self.Block_9_Table.get_children():
            child.modify_bg(state=Gtk.STATE_NORMAL, color=Normal_Color)

         widget.modify_bg(state=Gtk.STATE_NORMAL, color=Highlight_Color)


   def Spin_Event(self, widget, data=None):
      """Triggered when a spinbox widget's value is changed. The changed value
      is stored in the backend datastore."""

      print('Spin_Event')
      Value = widget.get_value_as_int()
      Input_Widget = data['Widget']

      # Read value from widget, and store the value in the backend datastore.
      if (self.Current_Widget == 'Slider'):
         if (Input_Widget == 'CC'):
            self.Scene[self.Current_Scene].Block[self.Current_Block].Slider_CC = Value
         elif (Input_Widget == 'Min_Value'):
            self.Scene[self.Current_Scene].Block[self.Current_Block].Slider_Min_Value = Value
         elif (Input_Widget == 'Max_Value'):
            self.Scene[self.Current_Scene].Block[self.Current_Block].Slider_Max_Value = Value

      elif (self.Current_Widget == 'Knob'):
         if (Input_Widget == 'CC'):
            self.Scene[self.Current_Scene].Block[self.Current_Block].Knob_CC = Value
         elif (Input_Widget == 'Min_Value'):
            self.Scene[self.Current_Scene].Block[self.Current_Block].Knob_Min_Value = Value
         elif (Input_Widget == 'Max_Value'):
            self.Scene[self.Current_Scene].Block[self.Current_Block].Knob_Max_Value = Value

      elif (self.Current_Widget == 'Button_A'):
         if (Input_Widget == 'CC'):
            self.Scene[self.Current_Scene].Block[self.Current_Block].SW_A_CC = Value
         elif (Input_Widget == 'Off_Value'):
            self.Scene[self.Current_Scene].Block[self.Current_Block].SW_A_Off_Value = Value
         elif (Input_Widget == 'On_Value'):
            self.Scene[self.Current_Scene].Block[self.Current_Block].SW_A_On_Value = Value
         elif (Input_Widget == 'Attack_Time'):
            self.Scene[self.Current_Scene].Block[self.Current_Block].SW_A_Attack_Time = Value
         elif (Input_Widget == 'Release_Time'):
            self.Scene[self.Current_Scene].Block[self.Current_Block].SW_A_Release_Time = Value

      elif (self.Current_Widget == 'Button_B'):
         if (Input_Widget == 'CC'):
            self.Scene[self.Current_Scene].Block[self.Current_Block].SW_B_CC = Value
         elif (Input_Widget == 'Off_Value'):
            self.Scene[self.Current_Scene].Block[self.Current_Block].SW_B_Off_Value = Value
         elif (Input_Widget == 'On_Value'):
            self.Scene[self.Current_Scene].Block[self.Current_Block].SW_B_On_Value = Value
         elif (Input_Widget == 'Attack_Time'):
            self.Scene[self.Current_Scene].Block[self.Current_Block].SW_B_Attack_Time = Value
         elif (Input_Widget == 'Release_Time'):
            self.Scene[self.Current_Scene].Block[self.Current_Block].SW_B_Release_Time = Value

      elif (self.Current_Widget in range(6)):
         if (Input_Widget == 'CC'):
            self.Scene[self.Current_Scene].Transport_Button[self.Current_Widget].CC = Value
         elif (Input_Widget == 'MMC_Dev_ID'):
            self.Scene[self.Current_Scene].Transport_Button[self.Current_Widget].MMC_Device_ID = Value

   def Combo_Event(self, widget, data=None):
      """Triggered when combobox widget's value (index) is changed.
      The changed value (index) is stored in the backend datastore."""

      print('Combo_Event')
      Value = widget.get_active()
      Input_Widget = data['Widget']

      # Read value from widget, and store the value in the backend datastore.
      if (Input_Widget == 'Scene_Midi_Channel'):
         self.Scene[self.Current_Scene].Common.Scene_Midi_Channel = Value

      elif (Input_Widget == 'Block_Midi_Channel'):
         self.Scene[self.Current_Scene].Block[self.Current_Block].Block_Midi_Channel = Value

      elif (Input_Widget == 'Transport_Midi_Channel'):
         self.Scene[self.Current_Scene].Transport_Midi_Channel = Value

      elif (self.Current_Widget == 'Slider'):
         if (Input_Widget == 'Assign_Type'):
            self.Scene[self.Current_Scene].Block[self.Current_Block].Slider_Assign_Type = Value

      elif (self.Current_Widget == 'Knob'):
         if (Input_Widget == 'Assign_Type'):
            self.Scene[self.Current_Scene].Block[self.Current_Block].Knob_Assign_Type = Value

      elif (self.Current_Widget == 'Button_A'):
         if (Input_Widget == 'Assign_Type'):
            self.Scene[self.Current_Scene].Block[self.Current_Block].SW_A_Assign_Type = Value
         elif (Input_Widget == 'Switch_Type'):
            self.Scene[self.Current_Scene].Block[self.Current_Block].SW_A_Switch_Type = Value

      elif (self.Current_Widget == 'Button_B'):
         if (Input_Widget == 'Assign_Type'):
            self.Scene[self.Current_Scene].Block[self.Current_Block].SW_B_Assign_Type = Value
         elif (Input_Widget == 'Switch_Type'):
            self.Scene[self.Current_Scene].Block[self.Current_Block].SW_B_Switch_Type = Value

      elif (self.Current_Widget in range(6)):
         if (Input_Widget == 'Assign_Type'):
            self.Scene[self.Current_Scene].Transport_Button[self.Current_Widget].Assign_Type = Value
         elif (Input_Widget == 'MMC_Command'):
            self.Scene[self.Current_Scene].Transport_Button[self.Current_Widget].MMC_Command = Value
         elif (Input_Widget == 'Switch_Type'):
            self.Scene[self.Current_Scene].Transport_Button[self.Current_Widget].Switch_Type = Value

      return False

   def Entry_Event(self, widget, event, data=None):
      print('Entry_Event')
      Value = widget.get_text()
      Input_Widget = data['Widget']

      # Read value from widget, and store the value in the backend datastore.
      if (Input_Widget == 'Scene_Name'):
         self.Scene[self.Current_Scene].Common.Scene_Name = Value

      return False

   def Scene_Cycle_Event(self, widget, data=None):
      """Triggered when the Scene button is pressed. The current scene is cycled
      through the scenes."""

      print('Scene_Cycle_Event')
      Radio_Buttons = self.Scene_1_Light.get_group()
      # Sort the list so that they are in the correct order.
      Radio_Buttons.sort(key=Gtk.RadioButton.get_name)

      for i in range(len(Radio_Buttons)):
         if (i == len(Radio_Buttons)-1):
            # If we come this far, we need to wrap around to the first.
            Radio_Buttons[0].set_active(is_active=True)
            break
         elif Radio_Buttons[i].get_active():
            Radio_Buttons[i+1].set_active(is_active=True)
            break

      return False

   def Scene_Change_Event(self, widget, data=None):
      """Triggered when any of the scene radio buttons are clicked.
      Sets the current scene to the clicked radio button."""

      # TODO: This gets triggered several times when the scene
      # or the scene radio buttons are clicked.
      # PRIORITY: LOW

      print('Scene_Change_Event')
      Radio_Buttons = self.Scene_1_Light.get_group()
      Radio_Buttons.sort(key=Gtk.RadioButton.get_name)

      for i in range(len(Radio_Buttons)):
         if (Radio_Buttons[i].get_active()):
            self.Current_Scene = i

      # Fire off the Focus_Event so that the control widgets
      # get populated with values from the new scene.
      self.Focus_Event(widget=None, event=None,
                       data={'Block':self.Current_Block, 'Widget':self.Current_Widget, 'Widget_Type':self.Current_Widget_Type})
      return False

   def Upload_Scene_Event(self, widget, data=None):
      try:
         self.Midi_Comm.Scene_Change_Request(Scene_Number=self.Current_Scene)
         Scene_List = self.Scene[self.Current_Scene].Get_List()
         self.Midi_Comm.Scene_Upload_Request(Scene_List=Scene_List, Scene_Number=self.Current_Scene)
         self.Midi_Comm.Scene_Write_Request(Scene_Number=self.Current_Scene)
      except:
         self.Status_Bar.push(context_id=self.Status_Bar_Context_ID, text='Error:Upload Scene failed')
         return False

      self.Status_Bar.push(context_id=self.Status_Bar_Context_ID, text='Uploaded Scene to device')
      return False

   def Download_Scene_Event(self, widget, data=None):
      try:
         self.Midi_Comm.Scene_Change_Request(Scene_Number=self.Current_Scene)
         Scene_Data = self.Midi_Comm.Scene_Dump_Request()
         self.Scene[self.Current_Scene].Parse_Data(Scene_Data)
      except:
         self.Status_Bar.push(context_id=self.Status_Bar_Context_ID, text='Error: Download Scene failed')
         return False
      # Fire off the Focus_Event so that the control widgets
      # get populated with values from the new scene.
      self.Focus_Event(widget=None, event=None,
                       data={'Block':self.Current_Block, 'Widget':self.Current_Widget, 'Widget_Type':self.Current_Widget_Type})
      self.Status_Bar.push(context_id=self.Status_Bar_Context_ID, text='Downloaded Scene from device')
      return False

   def Copy_Scene_Event (self, widget, data=None):
      self.Scene[-1] = copy.deepcopy(self.Scene[self.Current_Scene])
      return False

   def Paste_Scene_Event (self, widget, data=None):
      self.Scene[self.Current_Scene] = copy.deepcopy(self.Scene[-1])
      # Fire off the Focus_Event so that the control widgets
      # get populated with values from the new scene.
      self.Focus_Event(widget=None, event=None,
                       data={'Block':self.Current_Block, 'Widget':self.Current_Widget, 'Widget_Type':self.Current_Widget_Type})
      return False

   def Fader_Event (self, widget, data=None):
      print('Fader Event')
      print(widget.value)
      print('Block: ' + str(data['Block']))
      if (data['Type'] == 'Slider'):
         Assign_Type = self.Scene[self.Current_Scene].Block[data['Block']].Slider_Assign_Type
         CC_Number = self.Scene[self.Current_Scene].Block[data['Block']].Slider_CC
         Min_Value = self.Scene[self.Current_Scene].Block[data['Block']].Slider_Min_Value
         Max_Value = self.Scene[self.Current_Scene].Block[data['Block']].Slider_Max_Value
      elif (data['Type'] == 'Knob'):
         Assign_Type = self.Scene[self.Current_Scene].Block[data['Block']].Knob_Assign_Type
         CC_Number = self.Scene[self.Current_Scene].Block[data['Block']].Knob_CC
         Min_Value = self.Scene[self.Current_Scene].Block[data['Block']].Knob_Min_Value
         Max_Value = self.Scene[self.Current_Scene].Block[data['Block']].Knob_Max_Value

      Block_Midi_Channel = self.Scene[self.Current_Scene].Block[data['Block']].Block_Midi_Channel
      Midi_Channel = Block_Midi_Channel
      if (Midi_Channel == 16):
         Midi_Channel = self.Scene[self.Current_Scene].Common.Scene_Midi_Channel

      print('Max value: ' + str(Max_Value))
      print('Min value: ' + str(Min_Value))
      print('CC number: ' + str(CC_Number))
      print('Assign type: ' + str(Assign_Type))
      print('Midi Channel: ' + str(Midi_Channel))
      Midi_Value = int((widget.value/127.0  * (Max_Value - Min_Value) + Min_Value) + 0.5)
      print('Midi Value: ' + str(Midi_Value))

      if (Assign_Type == 1):
         self.Midi_Comm.Send_Midi_CC(Channel=Midi_Channel, CC=CC_Number, Value=Midi_Value)

      return False

   def Button_Pressed_Event (self, widget, data=None):
      print('Button Pressed Event')
      if (data['Widget'] == 'Button_A'):
         Assign_Type = self.Scene[self.Current_Scene].Block[data['Block']].SW_A_Assign_Type
         CC_Number = self.Scene[self.Current_Scene].Block[data['Block']].SW_A_CC
         Off_Value = self.Scene[self.Current_Scene].Block[data['Block']].SW_A_Off_Value
         On_Value = self.Scene[self.Current_Scene].Block[data['Block']].SW_A_On_Value
         Switch_Type = self.Scene[self.Current_Scene].Block[data['Block']].SW_A_Switch_Type
      elif (data['Widget'] == 'Button_B'):
         Assign_Type = self.Scene[self.Current_Scene].Block[data['Block']].SW_B_Assign_Type
         CC_Number = self.Scene[self.Current_Scene].Block[data['Block']].SW_B_CC
         Off_Value = self.Scene[self.Current_Scene].Block[data['Block']].SW_B_Off_Value
         On_Value = self.Scene[self.Current_Scene].Block[data['Block']].SW_B_On_Value
         Switch_Type = self.Scene[self.Current_Scene].Block[data['Block']].SW_B_Switch_Type

      Block_Midi_Channel = self.Scene[self.Current_Scene].Block[data['Block']].Block_Midi_Channel
      Midi_Channel = Block_Midi_Channel
      if (Midi_Channel == 16):
         Midi_Channel = self.Scene[self.Current_Scene].Common.Scene_Midi_Channel

      print('On value: ' + str(On_Value))
      print('Off value: ' + str(Off_Value))
      print('CC number: ' + str(CC_Number))
      print('Assign type: ' + str(Assign_Type))
      print('Midi Channel: ' + str(Midi_Channel))
      print('Switch Type: ' + str(Switch_Type))
      print(widget.get_active())

      if (Assign_Type == 1):
         if (Switch_Type == 0):
            self.Midi_Comm.Send_Midi_CC(Channel=Midi_Channel, CC=CC_Number, Value=On_Value)
            widget.set_active(True)
         elif (Switch_Type == 1):
            Toggle_State = widget.get_active()
            if (Toggle_State):
               self.Midi_Comm.Send_Midi_CC(Channel=Midi_Channel, CC=CC_Number, Value=Off_Value)
            elif (not Toggle_State):
               self.Midi_Comm.Send_Midi_CC(Channel=Midi_Channel, CC=CC_Number, Value=On_Value)

      return False

   def Button_Released_Event (self, widget, data=None):
      print('Button Released Event')
      if (data['Widget'] == 'Button_A'):
         Assign_Type = self.Scene[self.Current_Scene].Block[data['Block']].SW_A_Assign_Type
         CC_Number = self.Scene[self.Current_Scene].Block[data['Block']].SW_A_CC
         Off_Value = self.Scene[self.Current_Scene].Block[data['Block']].SW_A_Off_Value
         On_Value = self.Scene[self.Current_Scene].Block[data['Block']].SW_A_On_Value
         Switch_Type = self.Scene[self.Current_Scene].Block[data['Block']].SW_A_Switch_Type
      elif (data['Widget'] == 'Button_B'):
         Assign_Type = self.Scene[self.Current_Scene].Block[data['Block']].SW_B_Assign_Type
         CC_Number = self.Scene[self.Current_Scene].Block[data['Block']].SW_B_CC
         Off_Value = self.Scene[self.Current_Scene].Block[data['Block']].SW_B_Off_Value
         On_Value = self.Scene[self.Current_Scene].Block[data['Block']].SW_B_On_Value
         Switch_Type = self.Scene[self.Current_Scene].Block[data['Block']].SW_B_Switch_Type

      Block_Midi_Channel = self.Scene[self.Current_Scene].Block[data['Block']].Block_Midi_Channel
      Midi_Channel = Block_Midi_Channel
      if (Midi_Channel == 16):
         Midi_Channel = self.Scene[self.Current_Scene].Common.Scene_Midi_Channel

      print('On value: ' + str(On_Value))
      print('Off value: ' + str(Off_Value))
      print('CC number: ' + str(CC_Number))
      print('Assign type: ' + str(Assign_Type))
      print('Midi Channel: ' + str(Midi_Channel))
      print('Switch Type: ' + str(Switch_Type))

      if (Assign_Type == 1 and Switch_Type == 0):
         self.Midi_Comm.Send_Midi_CC(Channel=Midi_Channel, CC=CC_Number, Value=Off_Value)

      return False

   def Transport_Button_Pressed_Event(self, widget, data=None):
      print('Transport_Button_Pressed_Event')
      Assign_Type = self.Scene[self.Current_Scene].Transport_Button[data['Button']].Assign_Type
      CC_Number = self.Scene[self.Current_Scene].Transport_Button[data['Button']].CC
      MMC_Command = self.Scene[self.Current_Scene].Transport_Button[data['Button']].MMC_Command + 1
      MMC_Device_ID = self.Scene[self.Current_Scene].Transport_Button[data['Button']].MMC_Device_ID
      Switch_Type = self.Scene[self.Current_Scene].Transport_Button[data['Button']].Switch_Type

      print('Assign type: ' + str(Assign_Type))
      print('CC: ' + str(CC_Number))
      print('MMC Command: ' + str(MMC_Command))
      print('MMC Device ID: ' + str(MMC_Device_ID))
      print('Switch Type: ' + str(Switch_Type))

      if (Assign_Type == 1):
         Transport_Midi_Channel = self.Scene[self.Current_Scene].Transport_Midi_Channel
         Midi_Channel = Transport_Midi_Channel
         if (Midi_Channel == 16):
            Midi_Channel = self.Scene[self.Current_Scene].Common.Scene_Midi_Channel
         if (Switch_Type == 0):
            self.Midi_Comm.Send_Midi_CC(Channel=Midi_Channel, CC=CC_Number, Value=127)
            widget.set_active(True)
         elif (Switch_Type == 1):
            Toggle_State = widget.get_active()
            if (Toggle_State):
               self.Midi_Comm.Send_Midi_CC(Channel=Midi_Channel, CC=CC_Number, Value=0)
            elif (not Toggle_State):
               self.Midi_Comm.Send_Midi_CC(Channel=Midi_Channel, CC=CC_Number, Value=127)

      elif (Assign_Type == 2):
         self.Midi_Comm.Send_Midi_MMC(Device_ID=MMC_Device_ID, Command=MMC_Command)
         widget.set_active(True)

      return False

   def Transport_Button_Released_Event(self, widget, data=None):
      Assign_Type = self.Scene[self.Current_Scene].Transport_Button[data['Button']].Assign_Type
      CC_Number = self.Scene[self.Current_Scene].Transport_Button[data['Button']].CC
      MMC_Command = self.Scene[self.Current_Scene].Transport_Button[data['Button']].MMC_Command + 1
      MMC_Device_ID = self.Scene[self.Current_Scene].Transport_Button[data['Button']].MMC_Device_ID
      Switch_Type = self.Scene[self.Current_Scene].Transport_Button[data['Button']].Switch_Type

      print('Assign type: ' + str(Assign_Type))
      print('CC: ' + str(CC_Number))
      print('MMC Command: ' + str(MMC_Command))
      print('MMC Device ID: ' + str(MMC_Device_ID))
      print('Switch Type: ' + str(Switch_Type))

      Transport_Midi_Channel = self.Scene[self.Current_Scene].Transport_Midi_Channel
      Midi_Channel = Transport_Midi_Channel
      if (Midi_Channel == 16):
         Midi_Channel = self.Scene[self.Current_Scene].Common.Scene_Midi_Channel

      if (Assign_Type == 1 and Switch_Type == 0):
         self.Midi_Comm.Send_Midi_CC(Channel=Midi_Channel, CC=CC_Number, Value=0)

      return False


   def __init__(self, Scene, Midi_Device):
      self.Scene = Scene
      self.Midi_Comm = Midi_Device
      self.Current_Block = 0
      self.Current_Widget = None
      self.Current_Widget_Type = None

      self.Window = Gtk.Window(title="Nano")
      self.Window.connect("delete_event", self.delete_event, None)

      # # # # Menu # # # #
      ####################
      self.Menu_Bar = Gtk.MenuBar()
      self.File_Menu = Gtk.Menu()
      self.File_Open = Gtk.MenuItem(label='Open...')
      self.File_Save = Gtk.MenuItem(label='Save...')
      self.File_Upload_Scene = Gtk.MenuItem(label='Upload Scene to Device')
      self.File_Upload_Scene.connect("activate", self.Upload_Scene_Event)
      self.File_Download_Scene = Gtk.MenuItem(label='Download Scene from Device')
      self.File_Download_Scene.connect("activate", self.Download_Scene_Event)

      self.File_Quit = Gtk.MenuItem(label='Quit')
      self.File_Quit.connect("activate", lambda w: Gtk.main_quit())

      self.File_Menu.append(child=self.File_Open)
      self.File_Open.show()
      self.File_Menu.append(child=self.File_Save)
      self.File_Save.show()
      self.File_Menu.append(child=self.File_Upload_Scene)
      self.File_Upload_Scene.show()
      self.File_Menu.append(child=self.File_Download_Scene)
      self.File_Download_Scene.show()
      self.File_Menu.append(child=self.File_Quit)
      self.File_Quit.show()

      self.File_Menu_Item = Gtk.MenuItem(label='File')
      self.File_Menu_Item.show()
      self.File_Menu_Item.set_submenu(submenu=self.File_Menu)

      self.Edit_Menu = Gtk.Menu()
      self.Edit_Copy = Gtk.MenuItem(label='Copy Scene')
      self.Edit_Copy.connect("activate", self.Copy_Scene_Event)
      self.Edit_Paste = Gtk.MenuItem(label='Paste Scene')
      self.Edit_Paste.connect("activate", self.Paste_Scene_Event)

      self.Edit_Menu.append(child=self.Edit_Copy)
      self.Edit_Menu.append(child=self.Edit_Paste)
      self.Edit_Copy.show()
      self.Edit_Paste.show()

      self.Edit_Menu_Item = Gtk.MenuItem(label='Edit')
      self.Edit_Menu_Item.show()
      self.Edit_Menu_Item.set_submenu(submenu=self.Edit_Menu)

      self.Menu_Bar.append(child=self.File_Menu_Item)
      self.Menu_Bar.append(child=self.Edit_Menu_Item)
      self.Menu_Bar.show()

      self.V_Box_Top = Gtk.VBox()
      self.V_Box_Top.pack_start(child=self.Menu_Bar, expand=False, fill=False, padding=2)
      self.H_Box_Level_1 = Gtk.HBox()

      # # # # Transport and Scene Buttons # # # #
      ###########################################
      self.Transport_Table = Gtk.Table(rows=3, columns=3)
      self.Transport_Rewind = Gtk.ToggleButton(label='REW')
      self.Transport_Rewind.connect("focus-in-event", self.Focus_Event,
                                    {'Widget':0, 'Widget_Type':'Transport'})
      self.Transport_Rewind.connect("pressed", self.Transport_Button_Pressed_Event,
                                    {'Widget':'Transport', 'Button':0})
      self.Transport_Rewind.connect("released", self.Transport_Button_Released_Event,
                                    {'Widget':'Transport', 'Button':0})

      self.Transport_Play = Gtk.ToggleButton(label='PLAY')
      self.Transport_Play.connect("focus-in-event", self.Focus_Event,
                                  {'Widget':1, 'Widget_Type':'Transport'})
      self.Transport_Play.connect("pressed", self.Transport_Button_Pressed_Event,
                                    {'Widget':'Transport', 'Button':1})
      self.Transport_Play.connect("released", self.Transport_Button_Released_Event,
                                    {'Widget':'Transport', 'Button':1})

      self.Transport_Fast_Forward = Gtk.ToggleButton(label='FF')
      self.Transport_Fast_Forward.connect("focus-in-event", self.Focus_Event,
                                  {'Widget':2, 'Widget_Type':'Transport'})
      self.Transport_Fast_Forward.connect("pressed", self.Transport_Button_Pressed_Event,
                                    {'Widget':'Transport', 'Button':2})
      self.Transport_Fast_Forward.connect("released", self.Transport_Button_Released_Event,
                                    {'Widget':'Transport', 'Button':2})

      self.Transport_Loop = Gtk.ToggleButton(label='LOOP')
      self.Transport_Loop.connect("focus-in-event", self.Focus_Event,
                                  {'Widget':3, 'Widget_Type':'Transport'})
      self.Transport_Loop.connect("pressed", self.Transport_Button_Pressed_Event,
                                    {'Widget':'Transport', 'Button':3})
      self.Transport_Loop.connect("released", self.Transport_Button_Released_Event,
                                    {'Widget':'Transport', 'Button':3})

      self.Transport_Stop = Gtk.ToggleButton(label='STOP')
      self.Transport_Stop.connect("focus-in-event", self.Focus_Event,
                                  {'Widget':4, 'Widget_Type':'Transport'})
      self.Transport_Stop.connect("pressed", self.Transport_Button_Pressed_Event,
                                    {'Widget':'Transport', 'Button':4})
      self.Transport_Stop.connect("released", self.Transport_Button_Released_Event,
                                    {'Widget':'Transport', 'Button':4})

      self.Transport_Record = Gtk.ToggleButton('REC')
      self.Transport_Record.connect("focus-in-event", self.Focus_Event,
                                  {'Widget':5, 'Widget_Type':'Transport'})
      self.Transport_Record.connect("pressed", self.Transport_Button_Pressed_Event,
                                    {'Widget':'Transport', 'Button':5})
      self.Transport_Record.connect("released", self.Transport_Button_Released_Event,
                                    {'Widget':'Transport', 'Button':5})


      self.Scene_H_Box = Gtk.HBox()
      self.Scene_Button = Gtk.Button('SCENE')
      self.Scene_Button.connect("clicked", self.Scene_Cycle_Event, {'Type':'Cyclic',})
      self.Scene_1_Light = Gtk.RadioButton(group=None, label='1', use_underline=False)
      self.Scene_1_Light.set_name(name='Scene_1')
      self.Scene_1_Light.connect("clicked", self.Scene_Change_Event, {'Type':'Direct',})
      self.Scene_2_Light = Gtk.RadioButton(group=self.Scene_1_Light, label='2', use_underline=False)
      self.Scene_2_Light.set_name(name='Scene_2')
      self.Scene_2_Light.connect("clicked", self.Scene_Change_Event, {'Type':'Direct',})
      self.Scene_3_Light = Gtk.RadioButton(group=self.Scene_1_Light, label='3', use_underline=False)
      self.Scene_3_Light.set_name(name='Scene_3')
      self.Scene_3_Light.connect("clicked", self.Scene_Change_Event, {'Type':'Direct',})
      self.Scene_4_Light = Gtk.RadioButton(group=self.Scene_1_Light, label='4', use_underline=False)
      self.Scene_4_Light.set_name(name='Scene_4')
      self.Scene_4_Light.connect("clicked", self.Scene_Change_Event, {'Type':'Direct',})
      self.Scene_H_Box.pack_start(self.Scene_Button,
                                   expand=True, fill=True, padding=0)
      self.Scene_H_Box.pack_start(self.Scene_1_Light,
                                   expand=True, fill=True, padding=0)
      self.Scene_H_Box.pack_start(self.Scene_2_Light,
                                   expand=True, fill=True, padding=0)
      self.Scene_H_Box.pack_start(self.Scene_3_Light,
                                   expand=True, fill=True, padding=0)
      self.Scene_H_Box.pack_start(self.Scene_4_Light,
                                   expand=True, fill=True, padding=0)
      self.Scene_Button.show()
      self.Scene_1_Light.show()
      self.Scene_2_Light.show()
      self.Scene_3_Light.show()
      self.Scene_4_Light.show()
      self.Scene_H_Box.show()

      self.Transport_Table.attach(child=self.Transport_Rewind,
                                  left_attach=0,
                                  right_attach=1,
                                  top_attach=0,
                                  bottom_attach=1)
      self.Transport_Rewind.show()
      self.Transport_Table.attach(child=self.Transport_Play,
                                  left_attach=1,
                                  right_attach=2,
                                  top_attach=0,
                                  bottom_attach=1)
      self.Transport_Play.show()
      self.Transport_Table.attach(child=self.Transport_Fast_Forward,
                                  left_attach=2,
                                  right_attach=3,
                                  top_attach=0,
                                  bottom_attach=1)
      self.Transport_Fast_Forward.show()
      self.Transport_Table.attach(child=self.Transport_Loop,
                                  left_attach=0,
                                  right_attach=1,
                                  top_attach=1,
                                  bottom_attach=2)
      self.Transport_Loop.show()
      self.Transport_Table.attach(child=self.Transport_Stop,
                                  left_attach=1,
                                  right_attach=2,
                                  top_attach=1,
                                  bottom_attach=2)
      self.Transport_Stop.show()
      self.Transport_Table.attach(child=self.Transport_Record,
                                  left_attach=2,
                                  right_attach=3,
                                  top_attach=1,
                                  bottom_attach=2)
      self.Transport_Record.show()
      self.Transport_Table.attach(child=self.Scene_H_Box,
                                  left_attach=0,
                                  right_attach=3,
                                  top_attach=2,
                                  bottom_attach=3)
      self.Transport_Table.show()

      # # # # Block 1 # # # #
      #######################
      self.Block_1_Table = Gtk.Table(rows=4, columns=2)
      self.Block_1_Label = Gtk.Label()
      self.Block_1_Label.set_markup('<span foreground="black">1</span>')
      adj = Gtk.Adjustment(value=0, lower=0, upper=127, step_incr=1, page_incr=5, page_size=0)
      adj.connect("value_changed", self.Fader_Event, {'Block':0, 'Type':'Slider'})
      self.Block_1_Slider = Gtk.VScale(adjustment=adj)
      self.Block_1_Slider.set_draw_value(draw_value=False)
      self.Block_1_Slider.set_inverted(setting=True)
      self.Block_1_Slider.connect("focus-in-event", self.Focus_Event,
                                  {'Block':0, 'Widget':'Slider', 'Widget_Type':'Slider'})
      adj = Gtk.Adjustment(value=0, lower=0, upper=127, step_incr=1, page_incr=5, page_size=0)
      adj.connect("value_changed", self.Fader_Event, {'Block':0, 'Type':'Knob'})
      self.Block_1_Knob = Gtk.HScale(adjustment=adj)
      self.Block_1_Knob.set_draw_value(draw_value=False)
      self.Block_1_Knob.connect("focus-in-event", self.Focus_Event,
                                {'Block':0, 'Widget':'Knob', 'Widget_Type':'Slider'})
      self.Block_1_Button_A = Gtk.ToggleButton(label='A')
      self.Block_1_Button_A.connect("focus-in-event", self.Focus_Event,
                                    {'Block':0, 'Widget':'Button_A', 'Widget_Type':'Button'})
      self.Block_1_Button_A.connect("pressed", self.Button_Pressed_Event,
                                    {'Block':0, 'Widget':'Button_A'})
      self.Block_1_Button_A.connect("released", self.Button_Released_Event,
                                    {'Block':0, 'Widget':'Button_A'})
      self.Block_1_Button_B = Gtk.ToggleButton(label='B')
      self.Block_1_Button_B.connect("focus-in-event", self.Focus_Event,
                                    {'Block':0, 'Widget':'Button_B', 'Widget_Type':'Button'})
      self.Block_1_Button_B.connect("pressed", self.Button_Pressed_Event,
                                    {'Block':0, 'Widget':'Button_B'})
      self.Block_1_Button_B.connect("released", self.Button_Released_Event,
                                    {'Block':0, 'Widget':'Button_B'})
      self.Block_1_Table.attach(child=self.Block_1_Label,
                                left_attach=0,
                                right_attach=1,
                                top_attach=0,
                                bottom_attach=1,
                                yoptions=Gtk.AttachOptions.FILL)
      self.Block_1_Label.show()
      self.Block_1_Table.attach(child=self.Block_1_Slider,
                                left_attach=1,
                                right_attach=2,
                                top_attach=1,
                                bottom_attach=3)
      self.Block_1_Slider.show()
      self.Block_1_Table.attach(child=self.Block_1_Knob,
                                left_attach=1,
                                right_attach=2,
                                top_attach=0,
                                bottom_attach=1,
                                yoptions=Gtk.AttachOptions.FILL)
      self.Block_1_Knob.show()
      self.Block_1_Table.attach(child=self.Block_1_Button_A,
                                left_attach=0,
                                right_attach=1,
                                top_attach=1,
                                bottom_attach=2)
      self.Block_1_Button_A.show()
      self.Block_1_Table.attach(child=self.Block_1_Button_B,
                                left_attach=0,
                                right_attach=1,
                                top_attach=2,
                                bottom_attach=3)
      self.Block_1_Button_B.show()
      self.Block_1_Table.show()

      # # # # Block 2 # # # #
      #######################
      self.Block_2_Table = Gtk.Table(rows=3, columns=2)
      self.Block_2_Label = Gtk.Label()
      self.Block_2_Label.set_markup('<span foreground="black">2</span>')
      adj = Gtk.Adjustment(value=0, lower=0, upper=127, step_incr=1, page_incr=5, page_size=0)
      adj.connect("value_changed", self.Fader_Event, {'Block':1, 'Type':'Slider'})
      self.Block_2_Slider = Gtk.VScale(adjustment=adj)
      self.Block_2_Slider.set_draw_value(draw_value=False)
      self.Block_2_Slider.set_inverted(setting=True)
      self.Block_2_Slider.connect("focus-in-event", self.Focus_Event,
                                  {'Block':1, 'Widget':'Slider', 'Widget_Type':'Slider'})
      adj = Gtk.Adjustment(value=0, lower=0, upper=127, step_incr=1, page_incr=5, page_size=0)
      adj.connect("value_changed", self.Fader_Event, {'Block':1, 'Type':'Knob'})
      self.Block_2_Knob = Gtk.HScale(adjustment=adj)
      self.Block_2_Knob.set_draw_value(draw_value=False)
      self.Block_2_Knob.connect("focus-in-event", self.Focus_Event,
                                  {'Block':1, 'Widget':'Knob', 'Widget_Type':'Slider'})
      self.Block_2_Button_A = Gtk.ToggleButton(label='A')
      self.Block_2_Button_A.connect("focus-in-event", self.Focus_Event,
                                  {'Block':1, 'Widget':'Button_A', 'Widget_Type':'Button'})
      self.Block_2_Button_A.connect("pressed", self.Button_Pressed_Event,
                                    {'Block':1, 'Widget':'Button_A'})
      self.Block_2_Button_A.connect("released", self.Button_Released_Event,
                                    {'Block':1, 'Widget':'Button_A'})
      self.Block_2_Button_B = Gtk.ToggleButton(label='B')
      self.Block_2_Button_B.connect("focus-in-event", self.Focus_Event,
                                  {'Block':1, 'Widget':'Button_B', 'Widget_Type':'Button'})
      self.Block_2_Button_B.connect("pressed", self.Button_Pressed_Event,
                                    {'Block':1, 'Widget':'Button_B'})
      self.Block_2_Button_B.connect("released", self.Button_Released_Event,
                                    {'Block':1, 'Widget':'Button_B'})
      self.Block_2_Table.attach(child=self.Block_2_Label,
                                left_attach=0,
                                right_attach=1,
                                top_attach=0,
                                bottom_attach=1,
                                yoptions=Gtk.AttachOptions.SHRINK)
      self.Block_2_Label.show()
      self.Block_2_Table.attach(child=self.Block_2_Slider,
                                left_attach=1,
                                right_attach=2,
                                top_attach=1,
                                bottom_attach=3)
      self.Block_2_Slider.show()
      self.Block_2_Table.attach(child=self.Block_2_Knob,
                                left_attach=1,
                                right_attach=2,
                                top_attach=0,
                                bottom_attach=1,
                                yoptions=Gtk.AttachOptions.FILL)
      self.Block_2_Knob.show()
      self.Block_2_Table.attach(child=self.Block_2_Button_A,
                                left_attach=0,
                                right_attach=1,
                                top_attach=1,
                                bottom_attach=2)
      self.Block_2_Button_A.show()
      self.Block_2_Table.attach(child=self.Block_2_Button_B,
                                left_attach=0,
                                right_attach=1,
                                top_attach=2,
                                bottom_attach=3)
      self.Block_2_Button_B.show()
      self.Block_2_Table.show()

      # # # # Block 3 # # # #
      #######################
      self.Block_3_Table = Gtk.Table(rows=3, columns=2)
      self.Block_3_Label = Gtk.Label()
      self.Block_3_Label.set_markup('<span foreground="black">3</span>')
      adj = Gtk.Adjustment(value=0, lower=0, upper=127, step_incr=1, page_incr=5, page_size=0)
      adj.connect("value_changed", self.Fader_Event, {'Block':2, 'Type':'Slider'})
      self.Block_3_Slider = Gtk.VScale(adjustment=adj)
      self.Block_3_Slider.set_draw_value(draw_value=False)
      self.Block_3_Slider.set_inverted(setting=True)
      self.Block_3_Slider.connect("focus-in-event", self.Focus_Event,
                                  {'Block':2, 'Widget':'Slider', 'Widget_Type':'Slider'})
      adj = Gtk.Adjustment(value=0, lower=0, upper=127, step_incr=1, page_incr=5, page_size=0)
      adj.connect("value_changed", self.Fader_Event, {'Block':2, 'Type':'Knob'})
      self.Block_3_Knob = Gtk.HScale(adjustment=adj)
      self.Block_3_Knob.set_draw_value(draw_value=False)
      self.Block_3_Knob.connect("focus-in-event", self.Focus_Event,
                                {'Block':2, 'Widget':'Knob', 'Widget_Type':'Slider'})
      self.Block_3_Button_A = Gtk.ToggleButton(label='A')
      self.Block_3_Button_A.connect("focus-in-event", self.Focus_Event,
                                  {'Block':2, 'Widget':'Button_A', 'Widget_Type':'Button'})
      self.Block_3_Button_A.connect("pressed", self.Button_Pressed_Event,
                                    {'Block':2, 'Widget':'Button_A'})
      self.Block_3_Button_A.connect("released", self.Button_Released_Event,
                                    {'Block':2, 'Widget':'Button_A'})
      self.Block_3_Button_B = Gtk.ToggleButton(label='B')
      self.Block_3_Button_B.connect("focus-in-event", self.Focus_Event,
                                  {'Block':2, 'Widget':'Button_B', 'Widget_Type':'Button'})
      self.Block_3_Button_B.connect("pressed", self.Button_Pressed_Event,
                                    {'Block':2, 'Widget':'Button_B'})
      self.Block_3_Button_B.connect("released", self.Button_Released_Event,
                                    {'Block':2, 'Widget':'Button_B'})
      self.Block_3_Table.attach(child=self.Block_3_Label,
                                left_attach=0,
                                right_attach=1,
                                top_attach=0,
                                bottom_attach=1,
                                yoptions=Gtk.AttachOptions.FILL)
      self.Block_3_Label.show()
      self.Block_3_Table.attach(child=self.Block_3_Slider,
                                left_attach=1,
                                right_attach=2,
                                top_attach=1,
                                bottom_attach=3)
      self.Block_3_Slider.show()
      self.Block_3_Table.attach(child=self.Block_3_Knob,
                                left_attach=1,
                                right_attach=2,
                                top_attach=0,
                                bottom_attach=1,
                                yoptions=Gtk.AttachOptions.FILL)
      self.Block_3_Knob.show()
      self.Block_3_Table.attach(child=self.Block_3_Button_A,
                                left_attach=0,
                                right_attach=1,
                                top_attach=1,
                                bottom_attach=2)
      self.Block_3_Button_A.show()
      self.Block_3_Table.attach(child=self.Block_3_Button_B,
                                left_attach=0,
                                right_attach=1,
                                top_attach=2,
                                bottom_attach=3)
      self.Block_3_Button_B.show()
      self.Block_3_Table.show()

      # # # # Block 4 # # # #
      #######################
      self.Block_4_Table = Gtk.Table(rows=3, columns=2)
      self.Block_4_Label = Gtk.Label()
      self.Block_4_Label.set_markup('<span foreground="black">4</span>')
      adj = Gtk.Adjustment(value=0, lower=0, upper=127, step_incr=1, page_incr=5, page_size=0)
      adj.connect("value_changed", self.Fader_Event, {'Block':3, 'Type':'Slider'})
      self.Block_4_Slider = Gtk.VScale(adjustment=adj)
      self.Block_4_Slider.set_draw_value(draw_value=False)
      self.Block_4_Slider.set_inverted(setting=True)
      self.Block_4_Slider.connect("focus-in-event", self.Focus_Event,
                                  {'Block':3, 'Widget':'Slider', 'Widget_Type':'Slider'})
      adj = Gtk.Adjustment(value=0, lower=0, upper=127, step_incr=1, page_incr=5, page_size=0)
      adj.connect("value_changed", self.Fader_Event, {'Block':3, 'Type':'Knob'})
      self.Block_4_Knob = Gtk.HScale(adjustment=adj)
      self.Block_4_Knob.set_draw_value(draw_value=False)
      self.Block_4_Knob.connect("focus-in-event", self.Focus_Event,
                                {'Block':3, 'Widget':'Knob', 'Widget_Type':'Slider'})
      self.Block_4_Button_A = Gtk.ToggleButton(label='A')
      self.Block_4_Button_A.connect("focus-in-event", self.Focus_Event,
                                  {'Block':3, 'Widget':'Button_A', 'Widget_Type':'Button'})
      self.Block_4_Button_A.connect("pressed", self.Button_Pressed_Event,
                                    {'Block':3, 'Widget':'Button_A'})
      self.Block_4_Button_A.connect("released", self.Button_Released_Event,
                                    {'Block':3, 'Widget':'Button_A'})
      self.Block_4_Button_B = Gtk.ToggleButton(label='B')
      self.Block_4_Button_B.connect("focus-in-event", self.Focus_Event,
                                  {'Block':3, 'Widget':'Button_B', 'Widget_Type':'Button'})
      self.Block_4_Button_B.connect("pressed", self.Button_Pressed_Event,
                                    {'Block':3, 'Widget':'Button_B'})
      self.Block_4_Button_B.connect("released", self.Button_Released_Event,
                                    {'Block':3, 'Widget':'Button_B'})
      self.Block_4_Table.attach(child=self.Block_4_Label,
                                left_attach=0,
                                right_attach=1,
                                top_attach=0,
                                bottom_attach=1,
                                yoptions=Gtk.AttachOptions.FILL)
      self.Block_4_Label.show()
      self.Block_4_Table.attach(child=self.Block_4_Slider,
                                left_attach=1,
                                right_attach=2,
                                top_attach=1,
                                bottom_attach=3)
      self.Block_4_Slider.show()
      self.Block_4_Table.attach(child=self.Block_4_Knob,
                                left_attach=1,
                                right_attach=2,
                                top_attach=0,
                                bottom_attach=1,
                                yoptions=Gtk.AttachOptions.FILL)
      self.Block_4_Knob.show()
      self.Block_4_Table.attach(child=self.Block_4_Button_A,
                                left_attach=0,
                                right_attach=1,
                                top_attach=1,
                                bottom_attach=2)
      self.Block_4_Button_A.show()
      self.Block_4_Table.attach(child=self.Block_4_Button_B,
                                left_attach=0,
                                right_attach=1,
                                top_attach=2,
                                bottom_attach=3)
      self.Block_4_Button_B.show()
      self.Block_4_Table.show()

      # # # # Block 5 # # # #
      #######################
      self.Block_5_Table = Gtk.Table(rows=3, columns=2)
      self.Block_5_Label = Gtk.Label()
      self.Block_5_Label.set_markup('<span foreground="black">5</span>')
      adj = Gtk.Adjustment(value=0, lower=0, upper=127, step_incr=1, page_incr=5, page_size=0)
      adj.connect("value_changed", self.Fader_Event, {'Block':4, 'Type':'Slider'})
      self.Block_5_Slider = Gtk.VScale(adjustment=adj)
      self.Block_5_Slider.set_draw_value(draw_value=False)
      self.Block_5_Slider.set_inverted(setting=True)
      self.Block_5_Slider.connect("focus-in-event", self.Focus_Event,
                                  {'Block':4, 'Widget':'Slider', 'Widget_Type':'Slider'})
      adj = Gtk.Adjustment(value=0, lower=0, upper=127, step_incr=1, page_incr=5, page_size=0)
      adj.connect("value_changed", self.Fader_Event, {'Block':4, 'Type':'Knob'})
      self.Block_5_Knob = Gtk.HScale(adjustment=adj)
      self.Block_5_Knob.set_draw_value(draw_value=False)
      self.Block_5_Knob.connect("focus-in-event", self.Focus_Event,
                                {'Block':4, 'Widget':'Knob', 'Widget_Type':'Slider'})
      self.Block_5_Button_A = Gtk.ToggleButton(label='A')
      self.Block_5_Button_A.connect("focus-in-event", self.Focus_Event,
                                  {'Block':4, 'Widget':'Button_A', 'Widget_Type':'Button'})
      self.Block_5_Button_A.connect("pressed", self.Button_Pressed_Event,
                                    {'Block':4, 'Widget':'Button_A'})
      self.Block_5_Button_A.connect("released", self.Button_Released_Event,
                                    {'Block':4, 'Widget':'Button_A'})
      self.Block_5_Button_B = Gtk.ToggleButton(label='B')
      self.Block_5_Button_B.connect("focus-in-event", self.Focus_Event,
                                  {'Block':4, 'Widget':'Button_B', 'Widget_Type':'Button'})
      self.Block_5_Button_B.connect("pressed", self.Button_Pressed_Event,
                                    {'Block':4, 'Widget':'Button_B'})
      self.Block_5_Button_B.connect("released", self.Button_Released_Event,
                                    {'Block':4, 'Widget':'Button_B'})
      self.Block_5_Table.attach(child=self.Block_5_Label,
                                left_attach=0,
                                right_attach=1,
                                top_attach=0,
                                bottom_attach=1,
                                yoptions=Gtk.AttachOptions.FILL)
      self.Block_5_Label.show()
      self.Block_5_Table.attach(child=self.Block_5_Slider,
                                left_attach=1,
                                right_attach=2,
                                top_attach=1,
                                bottom_attach=3)
      self.Block_5_Slider.show()
      self.Block_5_Table.attach(child=self.Block_5_Knob,
                                left_attach=1,
                                right_attach=2,
                                top_attach=0,
                                bottom_attach=1,
                                yoptions=Gtk.AttachOptions.FILL)
      self.Block_5_Knob.show()
      self.Block_5_Table.attach(child=self.Block_5_Button_A,
                                left_attach=0,
                                right_attach=1,
                                top_attach=1,
                                bottom_attach=2)
      self.Block_5_Button_A.show()
      self.Block_5_Table.attach(child=self.Block_5_Button_B,
                                left_attach=0,
                                right_attach=1,
                                top_attach=2,
                                bottom_attach=3)
      self.Block_5_Button_B.show()
      self.Block_5_Table.show()

      # # # # Block 6 # # # #
      #######################
      self.Block_6_Table = Gtk.Table(rows=3, columns=2)
      self.Block_6_Label = Gtk.Label()
      self.Block_6_Label.set_markup('<span foreground="black">6</span>')
      adj = Gtk.Adjustment(value=0, lower=0, upper=127, step_incr=1, page_incr=5, page_size=0)
      adj.connect("value_changed", self.Fader_Event, {'Block':5, 'Type':'Slider'})
      self.Block_6_Slider = Gtk.VScale(adjustment=adj)
      self.Block_6_Slider.set_draw_value(draw_value=False)
      self.Block_6_Slider.set_inverted(setting=True)
      self.Block_6_Slider.connect("focus-in-event", self.Focus_Event,
                                  {'Block':5, 'Widget':'Slider', 'Widget_Type':'Slider'})
      adj = Gtk.Adjustment(value=0, lower=0, upper=127, step_incr=1, page_incr=5, page_size=0)
      adj.connect("value_changed", self.Fader_Event, {'Block':5, 'Type':'Knob'})
      self.Block_6_Knob = Gtk.HScale(adjustment=adj)
      self.Block_6_Knob.set_draw_value(draw_value=False)
      self.Block_6_Knob.connect("focus-in-event", self.Focus_Event,
                                {'Block':5, 'Widget':'Knob', 'Widget_Type':'Slider'})
      self.Block_6_Button_A = Gtk.ToggleButton(label='A')
      self.Block_6_Button_A.connect("focus-in-event", self.Focus_Event,
                                  {'Block':5, 'Widget':'Button_A', 'Widget_Type':'Button'})
      self.Block_6_Button_A.connect("pressed", self.Button_Pressed_Event,
                                    {'Block':5, 'Widget':'Button_A'})
      self.Block_6_Button_A.connect("released", self.Button_Released_Event,
                                    {'Block':5, 'Widget':'Button_A'})
      self.Block_6_Button_B = Gtk.ToggleButton(label='B')
      self.Block_6_Button_B.connect("focus-in-event", self.Focus_Event,
                                  {'Block':5, 'Widget':'Button_B', 'Widget_Type':'Button'})
      self.Block_6_Button_B.connect("pressed", self.Button_Pressed_Event,
                                    {'Block':5, 'Widget':'Button_B'})
      self.Block_6_Button_B.connect("released", self.Button_Released_Event,
                                    {'Block':5, 'Widget':'Button_B'})
      self.Block_6_Table.attach(child=self.Block_6_Label,
                                left_attach=0,
                                right_attach=1,
                                top_attach=0,
                                bottom_attach=1,
                                yoptions=Gtk.AttachOptions.FILL)
      self.Block_6_Label.show()
      self.Block_6_Table.attach(child=self.Block_6_Slider,
                                left_attach=1,
                                right_attach=2,
                                top_attach=1,
                                bottom_attach=3)
      self.Block_6_Slider.show()
      self.Block_6_Table.attach(child=self.Block_6_Knob,
                                left_attach=1,
                                right_attach=2,
                                top_attach=0,
                                bottom_attach=1,
                                yoptions=Gtk.AttachOptions.FILL)
      self.Block_6_Knob.show()
      self.Block_6_Table.attach(child=self.Block_6_Button_A,
                                left_attach=0,
                                right_attach=1,
                                top_attach=1,
                                bottom_attach=2)
      self.Block_6_Button_A.show()
      self.Block_6_Table.attach(child=self.Block_6_Button_B,
                                left_attach=0,
                                right_attach=1,
                                top_attach=2,
                                bottom_attach=3)
      self.Block_6_Button_B.show()
      self.Block_6_Table.show()

      # # # # Block 7 # # # #
      #######################
      self.Block_7_Table = Gtk.Table(rows=3, columns=2)
      self.Block_7_Label = Gtk.Label()
      self.Block_7_Label.set_markup('<span foreground="black">7</span>')
      adj = Gtk.Adjustment(value=0, lower=0, upper=127, step_incr=1, page_incr=5, page_size=0)
      adj.connect("value_changed", self.Fader_Event, {'Block':6, 'Type':'Slider'})
      self.Block_7_Slider = Gtk.VScale(adjustment=adj)
      self.Block_7_Slider.set_draw_value(draw_value=False)
      self.Block_7_Slider.set_inverted(setting=True)
      self.Block_7_Slider.connect("focus-in-event", self.Focus_Event,
                                  {'Block':6, 'Widget':'Slider', 'Widget_Type':'Slider'})
      adj = Gtk.Adjustment(value=0, lower=0, upper=127, step_incr=1, page_incr=5, page_size=0)
      adj.connect("value_changed", self.Fader_Event, {'Block':6, 'Type':'Knob'})
      self.Block_7_Knob = Gtk.HScale(adjustment=adj)
      self.Block_7_Knob.set_draw_value(draw_value=False)
      self.Block_7_Knob.connect("focus-in-event", self.Focus_Event,
                                {'Block':6, 'Widget':'Knob', 'Widget_Type':'Slider'})
      self.Block_7_Button_A = Gtk.ToggleButton(label='A')
      self.Block_7_Button_A.connect("focus-in-event", self.Focus_Event,
                                  {'Block':6, 'Widget':'Button_A', 'Widget_Type':'Button'})
      self.Block_7_Button_A.connect("pressed", self.Button_Pressed_Event,
                                    {'Block':6, 'Widget':'Button_A'})
      self.Block_7_Button_A.connect("released", self.Button_Released_Event,
                                    {'Block':6, 'Widget':'Button_A'})
      self.Block_7_Button_B = Gtk.ToggleButton(label='B')
      self.Block_7_Button_B.connect("focus-in-event", self.Focus_Event,
                                  {'Block':6, 'Widget':'Button_B', 'Widget_Type':'Button'})
      self.Block_7_Button_B.connect("pressed", self.Button_Pressed_Event,
                                    {'Block':6, 'Widget':'Button_B'})
      self.Block_7_Button_B.connect("released", self.Button_Released_Event,
                                    {'Block':6, 'Widget':'Button_B'})
      self.Block_7_Table.attach(child=self.Block_7_Label,
                                left_attach=0,
                                right_attach=1,
                                top_attach=0,
                                bottom_attach=1,
                                yoptions=Gtk.AttachOptions.FILL)
      self.Block_7_Label.show()
      self.Block_7_Table.attach(child=self.Block_7_Slider,
                                left_attach=1,
                                right_attach=2,
                                top_attach=1,
                                bottom_attach=3)
      self.Block_7_Slider.show()
      self.Block_7_Table.attach(child=self.Block_7_Knob,
                                left_attach=1,
                                right_attach=2,
                                top_attach=0,
                                bottom_attach=1,
                                yoptions=Gtk.AttachOptions.FILL)
      self.Block_7_Knob.show()
      self.Block_7_Table.attach(child=self.Block_7_Button_A,
                                left_attach=0,
                                right_attach=1,
                                top_attach=1,
                                bottom_attach=2)
      self.Block_7_Button_A.show()
      self.Block_7_Table.attach(child=self.Block_7_Button_B,
                                left_attach=0,
                                right_attach=1,
                                top_attach=2,
                                bottom_attach=3)
      self.Block_7_Button_B.show()
      self.Block_7_Table.show()

      # # # # Block 8 # # # #
      #######################
      self.Block_8_Table = Gtk.Table(rows=3, columns=2)
      self.Block_8_Label = Gtk.Label()
      self.Block_8_Label.set_markup('<span foreground="black">8</span>')
      adj = Gtk.Adjustment(value=0, lower=0, upper=127, step_incr=1, page_incr=5, page_size=0)
      adj.connect("value_changed", self.Fader_Event, {'Block':7, 'Type':'Slider'})
      self.Block_8_Slider = Gtk.VScale(adjustment=adj)
      self.Block_8_Slider.set_draw_value(draw_value=False)
      self.Block_8_Slider.set_inverted(setting=True)
      self.Block_8_Slider.connect("focus-in-event", self.Focus_Event,
                                  {'Block':7, 'Widget':'Slider', 'Widget_Type':'Slider'})
      adj = Gtk.Adjustment(value=0, lower=0, upper=127, step_incr=1, page_incr=5, page_size=0)
      adj.connect("value_changed", self.Fader_Event, {'Block':7, 'Type':'Knob'})
      self.Block_8_Knob = Gtk.HScale(adjustment=adj)
      self.Block_8_Knob.set_draw_value(draw_value=False)
      self.Block_8_Knob.connect("focus-in-event", self.Focus_Event,
                                {'Block':7, 'Widget':'Knob', 'Widget_Type':'Slider'})
      self.Block_8_Button_A = Gtk.ToggleButton(label='A')
      self.Block_8_Button_A.connect("focus-in-event", self.Focus_Event,
                                  {'Block':7, 'Widget':'Button_A', 'Widget_Type':'Button'})
      self.Block_8_Button_A.connect("pressed", self.Button_Pressed_Event,
                                    {'Block':7, 'Widget':'Button_A'})
      self.Block_8_Button_A.connect("released", self.Button_Released_Event,
                                    {'Block':7, 'Widget':'Button_A'})
      self.Block_8_Button_B = Gtk.ToggleButton(label='B')
      self.Block_8_Button_B.connect("focus-in-event", self.Focus_Event,
                                  {'Block':7, 'Widget':'Button_B', 'Widget_Type':'Button'})
      self.Block_8_Button_B.connect("pressed", self.Button_Pressed_Event,
                                    {'Block':7, 'Widget':'Button_B'})
      self.Block_8_Button_B.connect("released", self.Button_Released_Event,
                                    {'Block':7, 'Widget':'Button_B'})
      self.Block_8_Table.attach(child=self.Block_8_Label,
                                left_attach=0,
                                right_attach=1,
                                top_attach=0,
                                bottom_attach=1,
                                yoptions=Gtk.AttachOptions.FILL)
      self.Block_8_Label.show()
      self.Block_8_Table.attach(child=self.Block_8_Slider,
                                left_attach=1,
                                right_attach=2,
                                top_attach=1,
                                bottom_attach=3)
      self.Block_8_Slider.show()
      self.Block_8_Table.attach(child=self.Block_8_Knob,
                                left_attach=1,
                                right_attach=2,
                                top_attach=0,
                                bottom_attach=1,
                                yoptions=Gtk.AttachOptions.FILL)
      self.Block_8_Knob.show()
      self.Block_8_Table.attach(child=self.Block_8_Button_A,
                                left_attach=0,
                                right_attach=1,
                                top_attach=1,
                                bottom_attach=2)
      self.Block_8_Button_A.show()
      self.Block_8_Table.attach(child=self.Block_8_Button_B,
                                left_attach=0,
                                right_attach=1,
                                top_attach=2,
                                bottom_attach=3)
      self.Block_8_Button_B.show()
      self.Block_8_Table.show()

      # # # # Block 9 # # # #
      #######################
      self.Block_9_Table = Gtk.Table(rows=3, columns=2)
      self.Block_9_Label = Gtk.Label()
      self.Block_9_Label.set_markup('<span foreground="black">9</span>')
      adj = Gtk.Adjustment(value=0, lower=0, upper=127, step_incr=1, page_incr=5, page_size=0)
      adj.connect("value_changed", self.Fader_Event, {'Block':8, 'Type':'Slider'})
      self.Block_9_Slider = Gtk.VScale(adjustment=adj)
      self.Block_9_Slider.set_draw_value(draw_value=False)
      self.Block_9_Slider.set_inverted(setting=True)
      self.Block_9_Slider.connect("focus-in-event", self.Focus_Event,
                                  {'Block':8, 'Widget':'Slider', 'Widget_Type':'Slider'})
      adj = Gtk.Adjustment(value=0, lower=0, upper=127, step_incr=1, page_incr=5, page_size=0)
      adj.connect("value_changed", self.Fader_Event, {'Block':8, 'Type':'Knob'})
      self.Block_9_Knob = Gtk.HScale(adjustment=adj)
      self.Block_9_Knob.set_draw_value(draw_value=False)
      self.Block_9_Knob.connect("focus-in-event", self.Focus_Event,
                                {'Block':8, 'Widget':'Knob', 'Widget_Type':'Slider'})
      self.Block_9_Button_A = Gtk.ToggleButton(label='A')
      self.Block_9_Button_A.connect("focus-in-event", self.Focus_Event,
                                  {'Block':8, 'Widget':'Button_A', 'Widget_Type':'Button'})
      self.Block_9_Button_A.connect("pressed", self.Button_Pressed_Event,
                                    {'Block':8, 'Widget':'Button_A'})
      self.Block_9_Button_A.connect("released", self.Button_Released_Event,
                                    {'Block':8, 'Widget':'Button_A'})
      self.Block_9_Button_B = Gtk.ToggleButton(label='B')
      self.Block_9_Button_B.connect("focus-in-event", self.Focus_Event,
                                  {'Block':8, 'Widget':'Button_B', 'Widget_Type':'Button'})
      self.Block_9_Button_B.connect("pressed", self.Button_Pressed_Event,
                                    {'Block':8, 'Widget':'Button_B'})
      self.Block_9_Button_B.connect("released", self.Button_Released_Event,
                                    {'Block':8, 'Widget':'Button_B'})
      self.Block_9_Table.attach(child=self.Block_9_Label,
                                left_attach=0,
                                right_attach=1,
                                top_attach=0,
                                bottom_attach=1,
                                yoptions=Gtk.AttachOptions.FILL)
      self.Block_9_Label.show()
      self.Block_9_Table.attach(child=self.Block_9_Slider,
                                left_attach=1,
                                right_attach=2,
                                top_attach=1,
                                bottom_attach=3)
      self.Block_9_Slider.show()
      self.Block_9_Table.attach(child=self.Block_9_Knob,
                                left_attach=1,
                                right_attach=2,
                                top_attach=0,
                                bottom_attach=1,
                                yoptions=Gtk.AttachOptions.FILL)
      self.Block_9_Knob.show()
      self.Block_9_Table.attach(child=self.Block_9_Button_A,
                                left_attach=0,
                                right_attach=1,
                                top_attach=1,
                                bottom_attach=2)
      self.Block_9_Button_A.show()
      self.Block_9_Table.attach(child=self.Block_9_Button_B,
                                left_attach=0,
                                right_attach=1,
                                top_attach=2,
                                bottom_attach=3)
      self.Block_9_Button_B.show()
      self.Block_9_Table.show()

      self.Block_Labels = [self.Block_1_Label, self.Block_2_Label, self.Block_3_Label,
                           self.Block_4_Label, self.Block_5_Label, self.Block_6_Label,
                           self.Block_7_Label, self.Block_8_Label, self.Block_9_Label]

      # # # # Common controls # # # #
      ###############################
      self.Common_H_Box = Gtk.HBox()
      self.Transport_Midi_Channel_Label = Gtk.Label.new(str='Transport MIDI Channel:')
      self.Transport_Midi_Channel = Gtk.ComboBoxText()
      self.Transport_Midi_Channel.append_text('1')
      self.Transport_Midi_Channel.append_text('2')
      self.Transport_Midi_Channel.append_text('3')
      self.Transport_Midi_Channel.append_text('4')
      self.Transport_Midi_Channel.append_text('5')
      self.Transport_Midi_Channel.append_text('6')
      self.Transport_Midi_Channel.append_text('7')
      self.Transport_Midi_Channel.append_text('8')
      self.Transport_Midi_Channel.append_text('9')
      self.Transport_Midi_Channel.append_text('10')
      self.Transport_Midi_Channel.append_text('11')
      self.Transport_Midi_Channel.append_text('12')
      self.Transport_Midi_Channel.append_text('13')
      self.Transport_Midi_Channel.append_text('14')
      self.Transport_Midi_Channel.append_text('15')
      self.Transport_Midi_Channel.append_text('16')
      self.Transport_Midi_Channel.append_text('Scene')
      self.Transport_Midi_Channel.connect("changed", self.Combo_Event,
                                          {'Widget':'Transport_Midi_Channel', 'Widget_Type':'Slider'})
      self.Block_Midi_Channel_Label = Gtk.Label(label='Block MIDI Channel:')
      self.Block_Midi_Channel = Gtk.ComboBoxText()
      self.Block_Midi_Channel.append_text('1')
      self.Block_Midi_Channel.append_text('2')
      self.Block_Midi_Channel.append_text('3')
      self.Block_Midi_Channel.append_text('4')
      self.Block_Midi_Channel.append_text('5')
      self.Block_Midi_Channel.append_text('6')
      self.Block_Midi_Channel.append_text('7')
      self.Block_Midi_Channel.append_text('8')
      self.Block_Midi_Channel.append_text('9')
      self.Block_Midi_Channel.append_text('10')
      self.Block_Midi_Channel.append_text('11')
      self.Block_Midi_Channel.append_text('12')
      self.Block_Midi_Channel.append_text('13')
      self.Block_Midi_Channel.append_text('14')
      self.Block_Midi_Channel.append_text('15')
      self.Block_Midi_Channel.append_text('16')
      self.Block_Midi_Channel.append_text('Scene')
      self.Block_Midi_Channel.connect("changed", self.Combo_Event,
                                      {'Widget':'Block_Midi_Channel', 'Widget_Type':'Slider'})
      self.Scene_Name_Label = Gtk.Label(label='Scene Name:')
      self.Scene_Name = Gtk.Entry()
      self.Scene_Name.connect("focus-out-event", self.Entry_Event,
                              {'Widget':'Scene_Name', 'Widget_Type':'Entry'})
      self.Scene_Midi_Channel_Label = Gtk.Label(label='Scene MIDI Channel:')
      self.Scene_Midi_Channel = Gtk.ComboBoxText()
      self.Scene_Midi_Channel.append_text('1')
      self.Scene_Midi_Channel.append_text('2')
      self.Scene_Midi_Channel.append_text('3')
      self.Scene_Midi_Channel.append_text('4')
      self.Scene_Midi_Channel.append_text('5')
      self.Scene_Midi_Channel.append_text('6')
      self.Scene_Midi_Channel.append_text('7')
      self.Scene_Midi_Channel.append_text('8')
      self.Scene_Midi_Channel.append_text('9')
      self.Scene_Midi_Channel.append_text('10')
      self.Scene_Midi_Channel.append_text('11')
      self.Scene_Midi_Channel.append_text('12')
      self.Scene_Midi_Channel.append_text('13')
      self.Scene_Midi_Channel.append_text('14')
      self.Scene_Midi_Channel.append_text('15')
      self.Scene_Midi_Channel.append_text('16')
      self.Scene_Midi_Channel.connect("changed", self.Combo_Event,
                                      {'Widget':'Scene_Midi_Channel', 'Widget_Type':'Slider'})

      self.Common_H_Box.pack_start(self.Transport_Midi_Channel_Label,
                                   expand=True, fill=True, padding=2)
      self.Common_H_Box.pack_start(self.Transport_Midi_Channel,
                                   expand=True, fill=True, padding=2)
      self.Common_H_Box.pack_start(self.Block_Midi_Channel_Label,
                                   expand=True, fill=True, padding=2)
      self.Common_H_Box.pack_start(self.Block_Midi_Channel,
                                   expand=True, fill=True, padding=2)
      self.Common_H_Box.pack_start(self.Scene_Name_Label,
                                   expand=True, fill=True, padding=2)
      self.Common_H_Box.pack_start(self.Scene_Name,
                                   expand=True, fill=True, padding=2)
      self.Common_H_Box.pack_start(self.Scene_Midi_Channel_Label,
                                   expand=True, fill=True, padding=2)
      self.Common_H_Box.pack_start(self.Scene_Midi_Channel,
                                   expand=True, fill=True, padding=2)
      self.Transport_Midi_Channel_Label.show()
      self.Transport_Midi_Channel.show()
      self.Block_Midi_Channel_Label.show()
      self.Block_Midi_Channel.show()
      self.Scene_Name_Label.show()
      self.Scene_Name.show()
      self.Scene_Midi_Channel_Label.show()
      self.Scene_Midi_Channel.show()
      self.Common_H_Box.show()

      # # # # Transport controls # # # #
      ##################################
      self.Transport_Control_Table = Gtk.Table(rows=4, columns=4)
      self.Transport_Assign_Type_Label = Gtk.Label(label='Assign Type:')
      self.Transport_Assign_Type = Gtk.ComboBoxText()
      self.Transport_Assign_Type.append_text('No Assign')
      self.Transport_Assign_Type.append_text('CC')
      self.Transport_Assign_Type.append_text('MMC')
      self.Transport_Assign_Type.connect("changed", self.Combo_Event,
                                         {'Widget':'Assign_Type', 'Widget_Type':'Transport'})
      self.Transport_CC_Label = Gtk.Label(label='CC Number:')
      adj = Gtk.Adjustment(value=0, lower=0, upper=127, step_incr=1, page_incr=5, page_size=0)
      self.Transport_CC = Gtk.SpinButton(adjustment=adj, climb_rate=0.0, digits=0)
      self.Transport_CC.set_range(min=0, max=127)
      self.Transport_CC.set_numeric(numeric=True)
      self.Transport_CC.connect("value-changed", self.Spin_Event,
                                {'Widget':'CC', 'Widget_Type':'Transport'})
      self.Transport_MMC_Command_Label = Gtk.Label(label='MMC Command:')
      self.Transport_MMC_Command = Gtk.ComboBoxText()
      self.Transport_MMC_Command.append_text('Stop')
      self.Transport_MMC_Command.append_text('Play')
      self.Transport_MMC_Command.append_text('Deffered Play')
      self.Transport_MMC_Command.append_text('Fast Forward')
      self.Transport_MMC_Command.append_text('Rewind')
      self.Transport_MMC_Command.append_text('Record Strobe')
      self.Transport_MMC_Command.append_text('Record Exit')
      self.Transport_MMC_Command.append_text('Record Pause')
      self.Transport_MMC_Command.append_text('Pause')
      self.Transport_MMC_Command.append_text('Eject')
      self.Transport_MMC_Command.append_text('Chase')
      self.Transport_MMC_Command.append_text('Command Error Reset')
      self.Transport_MMC_Command.append_text('MMC Reset')
      self.Transport_MMC_Command.connect("changed", self.Combo_Event,
                                         {'Widget':'MMC_Command', 'Widget_Type':'Transport'})
      self.Transport_MMC_Dev_ID_Label = Gtk.Label(label='MMC Device ID:')
      adj = Gtk.Adjustment(value=0, lower=0, upper=127, step_incr=1, page_incr=5, page_size=0)
      self.Transport_MMC_Dev_ID = Gtk.SpinButton(adjustment=adj, climb_rate=0.0, digits=0)
      self.Transport_MMC_Dev_ID.set_range(min=0, max=127)
      self.Transport_MMC_Dev_ID.set_numeric(numeric=True)
      self.Transport_MMC_Dev_ID.connect("value-changed", self.Spin_Event,
                                        {'Widget':'MMC_Dev_ID', 'Widget_Type':'Transport'})
      self.Transport_Switch_Type_Label = Gtk.Label(label='Switch Type:')
      self.Transport_Switch_Type = Gtk.ComboBoxText()
      self.Transport_Switch_Type.append_text('Momentary')
      self.Transport_Switch_Type.append_text('Toggle')
      self.Transport_Switch_Type.connect("changed", self.Combo_Event,
                                         {'Widget':'Switch_Type', 'Widget_Type':'Transport'})

      self.Transport_Control_Table.attach(child=self.Transport_Assign_Type_Label,
                                          left_attach=0,
                                          right_attach=1,
                                          top_attach=0,
                                          bottom_attach=1)
      self.Transport_Assign_Type_Label.show()
      self.Transport_Control_Table.attach(child=self.Transport_Assign_Type,
                                          left_attach=1,
                                          right_attach=2,
                                          top_attach=0,
                                          bottom_attach=1)
      self.Transport_Assign_Type.show()
      self.Transport_Control_Table.attach(child=self.Transport_CC_Label,
                                          left_attach=0,
                                          right_attach=1,
                                          top_attach=1,
                                          bottom_attach=2)
      self.Transport_CC_Label.show()
      self.Transport_Control_Table.attach(child=self.Transport_CC,
                                          left_attach=1,
                                          right_attach=2,
                                          top_attach=1,
                                          bottom_attach=2)
      self.Transport_CC.show()
      self.Transport_Control_Table.attach(child=self.Transport_MMC_Command_Label,
                                          left_attach=0,
                                          right_attach=1,
                                          top_attach=2,
                                          bottom_attach=3)
      self.Transport_MMC_Command_Label.show()
      self.Transport_Control_Table.attach(child=self.Transport_MMC_Command,
                                          left_attach=1,
                                          right_attach=2,
                                          top_attach=2,
                                          bottom_attach=3)
      self.Transport_MMC_Command.show()
      self.Transport_Control_Table.attach(child=self.Transport_MMC_Dev_ID_Label,
                                          left_attach=0,
                                          right_attach=1,
                                          top_attach=3,
                                          bottom_attach=4)
      self.Transport_MMC_Dev_ID_Label.show()
      self.Transport_Control_Table.attach(child=self.Transport_MMC_Dev_ID,
                                          left_attach=1,
                                          right_attach=2,
                                          top_attach=3,
                                          bottom_attach=4)
      self.Transport_MMC_Dev_ID.show()
      self.Transport_Control_Table.attach(child=self.Transport_Switch_Type_Label,
                                          left_attach=2,
                                          right_attach=3,
                                          top_attach=0,
                                          bottom_attach=1)
      self.Transport_Switch_Type_Label.show()
      self.Transport_Control_Table.attach(child=self.Transport_Switch_Type,
                                          left_attach=3,
                                          right_attach=4,
                                          top_attach=0,
                                          bottom_attach=1)
      self.Transport_Switch_Type.show()


      # # # # Slider and Knob controls # # # #
      ########################################
      self.Slider_Knob_Control_Table = Gtk.Table(rows=4, columns=2)
      self.Slider_Assign_Type_Label = Gtk.Label(label='Assign type:')
      self.Slider_Assign_Type = Gtk.ComboBoxText()
      self.Slider_Assign_Type.append_text('No Assign')
      self.Slider_Assign_Type.append_text('CC')
      self.Slider_Assign_Type.connect("changed", self.Combo_Event,
                                      {'Widget':'Assign_Type', 'Widget_Type':'Slider'})
      self.Slider_CC_Label = Gtk.Label(label='CC number:')
      adj = Gtk.Adjustment(value=0, lower=0, upper=127, step_incr=1, page_incr=5, page_size=0)
      self.Slider_CC = Gtk.SpinButton(adjustment=adj, climb_rate=0.0, digits=0)
      self.Slider_CC.set_range(min=0, max=127)
      self.Slider_CC.set_numeric(numeric=True)
      self.Slider_CC.connect("value-changed", self.Spin_Event,
                             {'Widget':'CC', 'Widget_Type':'Slider'})
      self.Slider_Min_Value_Label = Gtk.Label(label='Min value:')
      adj = Gtk.Adjustment(value=0, lower=0, upper=127, step_incr=1, page_incr=5, page_size=0)
      self.Slider_Min_Value = Gtk.SpinButton(adjustment=adj, climb_rate=0.0, digits=0)
      self.Slider_Min_Value.set_range(min=0, max=127)
      self.Slider_Min_Value.set_numeric(numeric=True)
      self.Slider_Min_Value.connect("value-changed", self.Spin_Event,
                                    {'Widget':'Min_Value', 'Widget_Type':'Slider'})
      self.Slider_Max_Value_Label = Gtk.Label(label='Max value:')
      adj = Gtk.Adjustment(value=0, lower=0, upper=127, step_incr=1, page_incr=5, page_size=0)
      self.Slider_Max_Value = Gtk.SpinButton(adjustment=adj, climb_rate=0.0, digits=0)
      self.Slider_Max_Value.set_range(min=0, max=127)
      self.Slider_Max_Value.set_numeric(numeric=True)
      self.Slider_Max_Value.connect("value-changed", self.Spin_Event,
                                    {'Widget':'Max_Value', 'Widget_Type':'Slider'})

      self.Slider_Knob_Control_Table.attach(child=self.Slider_Assign_Type_Label,
                                            left_attach=0,
                                            right_attach=1,
                                            top_attach=0,
                                            bottom_attach=1)
      self.Slider_Assign_Type_Label.show()
      self.Slider_Knob_Control_Table.attach(child=self.Slider_Assign_Type,
                                            left_attach=1,
                                            right_attach=2,
                                            top_attach=0,
                                            bottom_attach=1)
      self.Slider_Assign_Type.show()
      self.Slider_Knob_Control_Table.attach(child=self.Slider_CC_Label,
                                            left_attach=0,
                                            right_attach=1,
                                            top_attach=1,
                                            bottom_attach=2)
      self.Slider_CC_Label.show()
      self.Slider_Knob_Control_Table.attach(child=self.Slider_CC,
                                            left_attach=1,
                                            right_attach=2,
                                            top_attach=1,
                                            bottom_attach=2)
      self.Slider_CC.show()
      self.Slider_Knob_Control_Table.attach(child=self.Slider_Min_Value_Label,
                                            left_attach=0,
                                            right_attach=1,
                                            top_attach=2,
                                            bottom_attach=3)
      self.Slider_Min_Value_Label.show()
      self.Slider_Knob_Control_Table.attach(child=self.Slider_Min_Value,
                                            left_attach=1,
                                            right_attach=2,
                                            top_attach=2,
                                            bottom_attach=3)
      self.Slider_Min_Value.show()
      self.Slider_Knob_Control_Table.attach(child=self.Slider_Max_Value_Label,
                                            left_attach=0,
                                            right_attach=1,
                                            top_attach=3,
                                            bottom_attach=4)
      self.Slider_Max_Value_Label.show()
      self.Slider_Knob_Control_Table.attach(child=self.Slider_Max_Value,
                                            left_attach=1,
                                            right_attach=2,
                                            top_attach=3,
                                            bottom_attach=4)
      self.Slider_Max_Value.show()


      # # # # Button controls # # # #
      ###############################
      self.Button_Control_Table = Gtk.Table(rows=4, columns=4)
      self.Button_Assign_Type_Label = Gtk.Label(label='Assign type:')
      self.Button_Assign_Type = Gtk.ComboBoxText()
      self.Button_Assign_Type.append_text('No Assign')
      self.Button_Assign_Type.append_text('CC')
      self.Button_Assign_Type.append_text('Note')
      self.Button_Assign_Type.connect("changed", self.Combo_Event,
                                      {'Widget':'Assign_Type', 'Widget_Type':'Button'})
      self.Button_CC_Label = Gtk.Label(label='CC/Note number:')
      adj = Gtk.Adjustment(value=0, lower=0, upper=127, step_incr=1, page_incr=5, page_size=0)
      self.Button_CC = Gtk.SpinButton(adjustment=adj, climb_rate=0.0, digits=0)
      self.Button_CC.set_range(min=0, max=127)
      self.Button_CC.connect("value-changed", self.Spin_Event,
                             {'Widget':'CC', 'Widget_Type':'Button'})
      self.Button_Off_Value_Label = Gtk.Label(label='Off value:')
      adj = Gtk.Adjustment(value=0, lower=0, upper=127, step_incr=1, page_incr=5, page_size=0)
      self.Button_Off_Value = Gtk.SpinButton(adjustment=adj, climb_rate=0.0, digits=0)
      self.Button_Off_Value.set_range(min=0, max=127)
      self.Button_Off_Value.connect("value-changed", self.Spin_Event,
                                    {'Widget':'Off_Value', 'Widget_Type':'Button'})
      self.Button_On_Value_Label = Gtk.Label(label='On value:')
      adj = Gtk.Adjustment(value=0, lower=0, upper=127, step_incr=1, page_incr=5, page_size=0)
      self.Button_On_Value = Gtk.SpinButton(adjustment=adj, climb_rate=0.0, digits=0)
      self.Button_On_Value.set_range(min=0, max=127)
      self.Button_On_Value.connect("value-changed", self.Spin_Event,
                                   {'Widget':'On_Value', 'Widget_Type':'Button'})
      self.Button_Attack_Time_Label = Gtk.Label(label='Attack time:')
      adj = Gtk.Adjustment(value=0, lower=0, upper=127, step_incr=1, page_incr=5, page_size=0)
      self.Button_Attack_Time = Gtk.SpinButton(adjustment=adj, climb_rate=0.0, digits=0)
      self.Button_Attack_Time.set_range(min=0, max=127)
      self.Button_Attack_Time.connect("value-changed", self.Spin_Event,
                                      {'Widget':'Attack_Time', 'Widget_Type':'Button'})
      self.Button_Release_Time_Label = Gtk.Label(label='Release time:')
      adj = Gtk.Adjustment(value=0, lower=0, upper=127, step_incr=1, page_incr=5, page_size=0)
      self.Button_Release_Time = Gtk.SpinButton(adjustment=adj, climb_rate=0.0, digits=0)
      self.Button_Release_Time.set_range(min=0, max=127)
      self.Button_Release_Time.connect("value-changed", self.Spin_Event,
                                       {'Widget':'Release_Time', 'Widget_Type':'Button'})
      self.Button_Switch_Type_Label = Gtk.Label(label='Switch type:')
      self.Button_Switch_Type = Gtk.ComboBoxText()
      self.Button_Switch_Type.append_text('Momentary')
      self.Button_Switch_Type.append_text('Toggle')
      self.Button_Switch_Type.connect("changed", self.Combo_Event,
                                      {'Widget':'Switch_Type', 'Widget_Type':'Button'})

      self.Button_Control_Table.attach(child=self.Button_Assign_Type_Label,
                                            left_attach=0,
                                            right_attach=1,
                                            top_attach=0,
                                            bottom_attach=1)
      self.Button_Assign_Type_Label.show()
      self.Button_Control_Table.attach(child=self.Button_Assign_Type,
                                            left_attach=1,
                                            right_attach=2,
                                            top_attach=0,
                                            bottom_attach=1)
      self.Button_Assign_Type.show()
      self.Button_Control_Table.attach(child=self.Button_CC_Label,
                                            left_attach=0,
                                            right_attach=1,
                                            top_attach=1,
                                            bottom_attach=2)
      self.Button_CC_Label.show()
      self.Button_Control_Table.attach(child=self.Button_CC,
                                            left_attach=1,
                                            right_attach=2,
                                            top_attach=1,
                                            bottom_attach=2)
      self.Button_CC.show()
      self.Button_Control_Table.attach(child=self.Button_Off_Value_Label,
                                            left_attach=0,
                                            right_attach=1,
                                            top_attach=2,
                                            bottom_attach=3)
      self.Button_Off_Value_Label.show()
      self.Button_Control_Table.attach(child=self.Button_Off_Value,
                                            left_attach=1,
                                            right_attach=2,
                                            top_attach=2,
                                            bottom_attach=3)
      self.Button_Off_Value.show()
      self.Button_Control_Table.attach(child=self.Button_On_Value_Label,
                                            left_attach=0,
                                            right_attach=1,
                                            top_attach=3,
                                            bottom_attach=4)
      self.Button_On_Value_Label.show()
      self.Button_Control_Table.attach(child=self.Button_On_Value,
                                            left_attach=1,
                                            right_attach=2,
                                            top_attach=3,
                                            bottom_attach=4)
      self.Button_On_Value.show()
      self.Button_Control_Table.attach(child=self.Button_Attack_Time_Label,
                                            left_attach=2,
                                            right_attach=3,
                                            top_attach=0,
                                            bottom_attach=1)
      self.Button_Attack_Time_Label.show()
      self.Button_Control_Table.attach(child=self.Button_Attack_Time,
                                            left_attach=3,
                                            right_attach=4,
                                            top_attach=0,
                                            bottom_attach=1)
      self.Button_Attack_Time.show()
      self.Button_Control_Table.attach(child=self.Button_Release_Time_Label,
                                            left_attach=2,
                                            right_attach=3,
                                            top_attach=1,
                                            bottom_attach=2)
      self.Button_Release_Time_Label.show()
      self.Button_Control_Table.attach(child=self.Button_Release_Time,
                                            left_attach=3,
                                            right_attach=4,
                                            top_attach=1,
                                            bottom_attach=2)
      self.Button_Release_Time.show()
      self.Button_Control_Table.attach(child=self.Button_Switch_Type_Label,
                                            left_attach=2,
                                            right_attach=3,
                                            top_attach=2,
                                            bottom_attach=3)
      self.Button_Switch_Type_Label.show()
      self.Button_Control_Table.attach(child=self.Button_Switch_Type,
                                            left_attach=3,
                                            right_attach=4,
                                            top_attach=2,
                                            bottom_attach=3)
      self.Button_Switch_Type.show()


      self.Status_Bar = Gtk.Statusbar()
      self.Status_Bar.show()
      self.Status_Bar_Context_ID = self.Status_Bar.get_context_id('Message')
      self.Status_Bar.push(self.Status_Bar_Context_ID, 'Status Bar')

      self.H_Box_Level_1.pack_start(self.Transport_Table,
                                    expand=True, fill=True, padding=2)
      self.H_Box_Level_1.pack_start(self.Block_1_Table,
                                    expand=True, fill=True, padding=2)
      self.H_Box_Level_1.pack_start(self.Block_2_Table,
                                    expand=True, fill=True, padding=2)
      self.H_Box_Level_1.pack_start(self.Block_3_Table,
                                    expand=True, fill=True, padding=2)
      self.H_Box_Level_1.pack_start(self.Block_4_Table,
                                    expand=True, fill=True, padding=2)
      self.H_Box_Level_1.pack_start(self.Block_5_Table,
                                    expand=True, fill=True, padding=2)
      self.H_Box_Level_1.pack_start(self.Block_6_Table,
                                    expand=True, fill=True, padding=2)
      self.H_Box_Level_1.pack_start(self.Block_7_Table,
                                    expand=True, fill=True, padding=2)
      self.H_Box_Level_1.pack_start(self.Block_8_Table,
                                    expand=True, fill=True, padding=2)
      self.H_Box_Level_1.pack_start(self.Block_9_Table,
                                    expand=True, fill=True, padding=2)

      self.H_Box_Level_1.show()
      self.H_Box_Level_1.set_size_request(width=-1, height=-1)
      #self.Slider_Knob_Control_Table.set_size_request(width=-1, height=150)
      self.V_Box_Top.pack_start(self.H_Box_Level_1,
                                expand=True, fill=True, padding=2)
      self.V_Box_Top.pack_start(self.Common_H_Box,
                                expand=False, fill=False, padding=2)
      self.V_Box_Top.pack_start(self.Slider_Knob_Control_Table,
                                expand=False, fill=False, padding=4)
      self.V_Box_Top.pack_start(self.Button_Control_Table,
                                expand=False, fill=False, padding=3)
      self.V_Box_Top.pack_start(self.Transport_Control_Table,
                                expand=False, fill=False, padding=3)
      self.V_Box_Top.pack_start(self.Status_Bar,
                                expand=False, fill=False, padding=2)
      self.V_Box_Top.show()

      self.Window.add(self.V_Box_Top)
      self.Window.show()

      self.Scene_1_Light.clicked()

   def main(self):
      Gtk.main()
