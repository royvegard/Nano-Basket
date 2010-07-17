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

class Nano_Kontrol_Common:
   """Common parameters from TABLE 1 of 'nanoKONTROL MIDI Implementation'
   file available from Korg."""

   def __init__(self):
      self.Scene_Name = 'Scene 1' # ASCII code
      self.Scene_Midi_Channel = 0 # 0~15

   def Get_List(self):
      """Return a list of the parameters in the order that they should
      appear in the sysex file."""

      # Scene name must contain exactly 12 bytes, padded with spaces.
      scene_name = (self.Scene_Name + '             ')[0:12]
      scene_list = list(scene_name)
      scene_list.append(self.Scene_Midi_Channel)
      return scene_list


class Nano_Kontrol_Block:

   def __init__(self):
      self.Block_Midi_Channel = 16 # 0~15/16~=MIDI Ch.0~15/Scene MIDI Ch.
      self.Slider_Assign_Type = 1  # 0/1=No Assign/CC
      self.Slider_CC = 1           # 0~127
      self.Slider_Min_Value = 0    # 0~127
      self.Slider_Max_Value = 127  # 0~127

      self.Knob_Assign_Type = 1    # 0/1=No Assign/CC
      self.Knob_CC = 1             # 0~127
      self.Knob_Min_Value = 0      # 0~127
      self.Knob_Max_Value = 127    # 0~127

      self.SW_A_Assign_Type = 1    # 0~2=No Assign/CC/Note
      self.SW_A_CC = 1             # 0~127
      self.SW_A_Off_Value = 0      # 0~127
      self.SW_A_On_Value = 127     # 0~127
      self.SW_A_Attack_Time = 0    # 0~127
      self.SW_A_Release_Time = 0   # 0~127
      self.SW_A_Switch_Type = 0    # 0/1=Momentary/Toggle

      self.SW_B_Assign_Type = 1    # 0~2=No Assign/CC/Note
      self.SW_B_CC = 1             # 0~127
      self.SW_B_Off_Value = 0      # 0~127
      self.SW_B_On_Value = 127     # 0~127
      self.SW_B_Attack_Time = 0    # 0~127
      self.SW_B_Release_Time = 0   # 0~127
      self.SW_B_Switch_Type = 0    # 0/1=Momentary/Toggle

   def Set_Midi_Channel(Value):
      if (Value > -1 and Value < 128):
         self.Block_Midi_Channel = Value

   def Get_List(self):
      """Return a list of the parameters in the order that they should
      appear in the sysex file."""

      return [self.Block_Midi_Channel,
              self.Slider_Assign_Type,
              self.Slider_CC,
              self.Slider_Min_Value,
              self.Slider_Max_Value,
              self.Knob_Assign_Type,
              self.Knob_CC,
              self.Knob_Min_Value,
              self.Knob_Max_Value,
              self.SW_A_Assign_Type,
              self.SW_A_CC,
              self.SW_A_Off_Value,
              self.SW_A_On_Value,
              self.SW_A_Attack_Time,
              self.SW_A_Release_Time,
              self.SW_A_Switch_Type,
              self.SW_B_Assign_Type,
              self.SW_B_CC,
              self.SW_B_Off_Value,
              self.SW_B_On_Value,
              self.SW_B_Attack_Time,
              self.SW_B_Release_Time,
              self.SW_B_Switch_Type]


class Nano_Kontrol_Transport_Switch:
   def __init__(self):
      self.Assign_Type = 1   # 0~2=No Assign/CC/MMC
      self.CC = 1            # 0~127
      self.MMC_Command = 1   # 0~12
      self.MMC_Device_ID = 1 # 0~127
      self.Switch_Type = 0   # 0/1=Momentary/Toggle

      # MMC commands:
      # 0  - Stop
      # 1  - Play
      # 2  - Deffered Play
      # 3  - Fast Forward
      # 4  - Rewind
      # 5  - Record Strobe
      # 6  - Record Exit
      # 7  - Record Pause
      # 8  - Pause
      # 9  - Eject
      # 10 - Chase
      # 11 - Command Error Reset
      # 12 - MMC Reset

   def Get_List(self):
      """Return a list of the parameters in the order that they should
      appear in the sysex file."""

      return [self.Assign_Type,
              self.CC,
              self.MMC_Command,
              self.MMC_Device_ID,
              self.Switch_Type]


class Nano_Kontrol_Scene:
   """Contains a complete nanoKONTROL scene."""

   def __init__(self):
      self.Common = Nano_Kontrol_Common()

      self.Block_1 = Nano_Kontrol_Block()
      self.Block_2 = Nano_Kontrol_Block()
      self.Block_3 = Nano_Kontrol_Block()
      self.Block_4 = Nano_Kontrol_Block()
      self.Block_5 = Nano_Kontrol_Block()
      self.Block_6 = Nano_Kontrol_Block()
      self.Block_7 = Nano_Kontrol_Block()
      self.Block_8 = Nano_Kontrol_Block()
      self.Block_9 = Nano_Kontrol_Block()

      self.Block = [self.Block_1, self.Block_2, self.Block_3,
                    self.Block_4, self.Block_5, self.Block_6,
                    self.Block_7, self.Block_8, self.Block_9]

      self.Transport_Midi_Channel = 16 # 0~15/16~=MIDI Ch.0~15/Scene MIDI Ch.
      self.Transport_1 = Nano_Kontrol_Transport_Switch() # REW
      self.Transport_2 = Nano_Kontrol_Transport_Switch() # PLAY
      self.Transport_3 = Nano_Kontrol_Transport_Switch() # FF
      self.Transport_4 = Nano_Kontrol_Transport_Switch() # LOOP
      self.Transport_5 = Nano_Kontrol_Transport_Switch() # STOP
      self.Transport_6 = Nano_Kontrol_Transport_Switch() # REC

      self.Transport_Button = [self.Transport_1, self.Transport_2,
                               self.Transport_3, self.Transport_4,
                               self.Transport_5, self.Transport_6]

   def Get_List(self):
      """Return a list of the parameters in the order that they should
      appear in the sysex file."""

      Parameter_List = self.Common.Get_List() + \
      [0, 0, 0] + \
      self.Block_1.Get_List() + \
      self.Block_2.Get_List() + \
      self.Block_3.Get_List() + \
      self.Block_4.Get_List() + \
      self.Block_5.Get_List() + \
      self.Block_6.Get_List() + \
      self.Block_7.Get_List() + \
      self.Block_8.Get_List() + \
      self.Block_9.Get_List() + \
      [0,] + \
      [self.Transport_Midi_Channel,] + \
      self.Transport_1.Get_List() + \
      self.Transport_2.Get_List() + \
      self.Transport_3.Get_List() + \
      self.Transport_4.Get_List() + \
      self.Transport_5.Get_List() + \
      self.Transport_6.Get_List() + \
      [0,]

      return Parameter_List

   def Get_Sysex_String(self):
      """Return a sysex string that can be sent to the nanoKONTROL
      device"""

      import struct
      Sysex_List = self.Get_List()
      # Inser a '0' every 8th index
      for i in range(37):
         Sysex_List.insert(i*8, 0)

      Sysex_String = '\xf0\x42\x40' # Exclusive Header
      Sysex_String = Sysex_String + '\x00\x01\x04\x00' # Software Project (nanoKONTROL: 000104H)
      Sysex_String = Sysex_String + '\x7f' # Data Dump Command  (Host<->Controller, Variable Format)
      Sysex_String = Sysex_String + '\x7f' # Over 0x7F Data
      Sysex_String = Sysex_String + '\x02' # 2Bytes structure
      Sysex_String = Sysex_String + '\x02' # Num of Data MSB (1+293 bytes : B'100100110)
      Sysex_String = Sysex_String + '\x26' # Num of Data LSB
      Sysex_String = Sysex_String + '\x40' # Current Scene Data Dump
      Sysex_String = Sysex_String + struct.pack('b7cb5c279b', *(Sysex_List)) # Data
      Sysex_String = Sysex_String + '\xf7' # End of Exclusive (EOX)

      return Sysex_String
