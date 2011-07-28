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

import struct
import time
from pyalsa import alsaseq

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
      scene_list = list(struct.unpack('12B', scene_name))
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
      
   def Parse_Data(self, Data):
      """ """
      
      if (len(Data) != 307):
         return
         
      Data_List = list(Data[13:])
      for i in range(37, 0, -1):
         Data_List.pop((i-1)*8)
      
      Scene_Name = ''
      for i in range(12):
         Scene_Name += chr(Data_List[i])
      
      self.Common.Scene_Name = Scene_Name
      self.Common.Scene_Midi_Channel = Data_List[12]

      i = 0
      for b in self.Block:
         b.Block_Midi_Channel = Data_List[16+i*23]
         b.Slider_Assign_Type = Data_List[17+i*23]
         b.Slider_CC =          Data_List[18+i*23]
         b.Slider_Min_Value =   Data_List[19+i*23]
         b.Slider_Max_Value =   Data_List[20+i*23]

         b.Knob_Assign_Type =   Data_List[21+i*23]
         b.Knob_CC =            Data_List[22+i*23]
         b.Knob_Min_Value =     Data_List[23+i*23]
         b.Knob_Max_Value =     Data_List[24+i*23]

         b.SW_A_Assign_Type =   Data_List[25+i*23]
         b.SW_A_CC =            Data_List[26+i*23]
         b.SW_A_Off_Value =     Data_List[27+i*23]
         b.SW_A_On_Value =      Data_List[28+i*23]
         b.SW_A_Attack_Time =   Data_List[29+i*23]
         b.SW_A_Release_Time =  Data_List[30+i*23]
         b.SW_A_Switch_Type =   Data_List[31+i*23]

         b.SW_B_Assign_Type =   Data_List[32+i*23]
         b.SW_B_CC =            Data_List[33+i*23]
         b.SW_B_Off_Value =     Data_List[34+i*23]
         b.SW_B_On_Value =      Data_List[35+i*23]
         b.SW_B_Attack_Time =   Data_List[36+i*23]
         b.SW_B_Release_Time =  Data_List[37+i*23]
         b.SW_B_Switch_Type =   Data_List[38+i*23]
         
         i += 1
      
      self.Transport_Midi_Channel = Data_List[224]
      
      i = 0
      for b in self.Transport_Button:
         b.Assign_Type =     Data_List[225+i*5]
         b.CC =              Data_List[226+i*5]
         b.MMC_Command =     Data_List[227+i*5]
         b.MMC_Device_ID =   Data_List[228+i*5]
         b.Switch_Type =     Data_List[229+i*5]
         
         i += 1


class Nano_Kontrol_Alsa_Midi_Comm:
   """Communicates with the device."""

   def __init__(self, Midi_Port_Name='Nano Basket MIDI 1'):
      self.Seq = alsaseq.Sequencer(clientname='Nano Basket')
      self.Event = alsaseq.SeqEvent(alsaseq.SEQ_EVENT_SYSEX)
      self.Controller = alsaseq.SeqEvent(alsaseq.SEQ_EVENT_CONTROLLER)
      self.Port = self.Seq.create_simple_port(name=Midi_Port_Name,
        type=alsaseq.SEQ_PORT_TYPE_APPLICATION,
        caps=alsaseq.SEQ_PORT_CAP_SUBS_READ | \
             alsaseq.SEQ_PORT_CAP_READ | \
             alsaseq.SEQ_PORT_CAP_WRITE | \
             alsaseq.SEQ_PORT_CAP_SUBS_WRITE)
             
      self.Response_Wait = 0.2


   def Scene_Change_Request(self, Scene_Number=0):
      """Sends a scene change request to the device."""

      if (Scene_Number > 3):
         Scene_Number = 3
      elif (Scene_Number < 0):
         Scene_Number = 0

      Global_Channel = self.Search_Device_Request()[4]
      Sysex = [0xf0, 0x42] # Exclusive Header
      Sysex.extend([0x40 + Global_Channel])
      Sysex.extend([0x00, 0x01, 0x04, 0x00]) # Software Project (nanoKONTROL: 000104H)
      Sysex.extend([0x1f]) # Data Dump Command  (Host->Controller, 2Bytes Format)
      Sysex.extend([0x14]) # Scene Change Request
      Sysex.extend([Scene_Number])
      Sysex.extend([0xf7]) # End of Exclusive (EOX)

      self.Flush_Events()

      self.Event.set_data({'ext': Sysex})
      self.Seq.output_event(self.Event)
      self.Seq.drain_output()
      time.sleep(self.Response_Wait)
      Response = self.Seq.receive_events(timeout=1000, maxevents = 200)
      
      for Res in Response:
         if ('ext' in Res.get_data().keys()):
            if (Res.get_data()['ext'][9] == Scene_Number):
               print('Scene change Success!')


   def Scene_Upload_Request(self, Scene_List, Scene_Number=None):
      """Writes a scene configuration to the device.
      Note that the configuration is only temporarily stored.
      To permanently write it to the device's memory, issue
      a Scene_Write_Request."""

      # Inser a '0' every 8th index
      for i in range(37):
         Scene_List.insert(i*8, 0)

      Global_Channel = self.Search_Device_Request()[4]
      Sysex = [0xf0,  0x42] # Exclusive Header
      Sysex.extend([0x40 + Global_Channel])
      Sysex.extend([0x00,  0x01,  0x04,  0x00]) # Software Project (nanoKONTROL: 000104H)
      Sysex.extend([0x7f]) # Data Dump Command  (Host<->Controller, Variable Format)
      Sysex.extend([0x7f]) # Over 0x7F Data
      Sysex.extend([0x02]) # 2Bytes structure
      Sysex.extend([0x02]) # Num of Data MSB (1+293 bytes : B'100100110)
      Sysex.extend([0x26]) # Num of Data LSB
      Sysex.extend([0x40]) # Current Scene Data Dump
      Sysex.extend(Scene_List) # Data
      Sysex.extend([0xf7]) # End of Exclusive (EOX)

      self.Flush_Events()

      if (Scene_Number):
         self.Scene_Change_Request(Scene_Number)

      self.Event.set_data({'ext': Sysex})
      self.Seq.output_event(self.Event)
      self.Seq.drain_output()
      time.sleep(self.Response_Wait)
      Response = self.Seq.receive_events(timeout=1000, maxevents = 200)
      
      for Res in Response:
         if ('ext' in Res.get_data().keys()):
            if (Res.get_data()['ext'][9] == 0x23):
               print('Data load Success!')
            elif(Res.get_data()['ext'][9] == 0x23):
               print('Data load Fail!')


   def Scene_Dump_Request(self, Scene_Number=None):
      """Reads the scene configuration from the device."""

      if (Scene_Number):
         self.Scene_Change_Request(Scene_Number)

      Global_Channel = self.Search_Device_Request()[4]
      Sysex = [0xf0,  0x42] # Exclusive Header
      Sysex.extend([0x40 + Global_Channel])
      Sysex.extend([0x00,  0x01,  0x04,  0x00]) # Software Project (nanoKONTROL: 000104H)
      Sysex.extend([0x1f]) # Data Dump Command  (Host->Controller, 2Bytes Format)
      Sysex.extend([0x10]) # Scene Dump Request
      Sysex.extend([0x00]) # Padding
      Sysex.extend([0xf7]) # End of Exclusive (EOX)

      self.Flush_Events()

      self.Event.set_data({'ext': Sysex})
      self.Seq.output_event(self.Event)
      self.Seq.drain_output()
      time.sleep(self.Response_Wait)
      Response = self.Seq.receive_events(timeout=1000, maxevents = 200)
      
      Data = []
      for Res in Response:
         if ('ext' in Res.get_data().keys()):
            Data.extend(Res.get_data()['ext'])
      return Data

   def Scene_Write_Request(self, Scene_Number=0):
      """Writes the current scene data into the internal memory.
      Normally used after a Scene_Upload_Request to permanently
      store the new scene configuration."""

      if (Scene_Number > 3):
         Scene_Number = 3
      elif (Scene_Number < 0):
         Scene_Number = 0

      Global_Channel = self.Search_Device_Request()[4]
      Sysex = [0xf0,  0x42] # Exclusive Header
      Sysex.extend([0x40 + Global_Channel])
      Sysex.extend([0x00,  0x01,  0x04,  0x00]) # Software Project (nanoKONTROL: 000104H)
      Sysex.extend([0x1f]) # Data Dump Command  (Host->Controller, 2Bytes Format)
      Sysex.extend([0x11]) # Scene Write Request
      Sysex.extend([Scene_Number])
      Sysex.extend([0xf7]) # End of Exclusive (EOX)

      self.Flush_Events()

      self.Event.set_data({'ext': Sysex})
      self.Seq.output_event(self.Event)
      self.Seq.drain_output()
      time.sleep(self.Response_Wait)
      Response = self.Seq.receive_events(timeout=1000, maxevents = 200)
      
      for Res in Response:
         if ('ext' in Res.get_data().keys()):
            if (Res.get_data()['ext'][9] == 0x23):
               print('Data load Success!')
            elif(Res.get_data()['ext'][9] == 0x23):
               print('Data load Fail!')


   def Search_Device_Request(self):
      Sysex = [0xf0,  0x42,  0x50] # Exclusive Header
      Sysex.extend([0x00,  0x01])
      Sysex.extend([0xf7]) # End of Exclusive (EOX)

      self.Flush_Events()

      self.Event.set_data({'ext': Sysex})
      self.Seq.output_event(self.Event)
      self.Seq.drain_output()
      time.sleep(self.Response_Wait)
      Response = self.Seq.receive_events(timeout=1000, maxevents = 200)
      
      for Res in Response:
         if ('ext' in Res.get_data().keys()):
            if (Res.get_data()['ext'][0:4] == [0xf0,  0x42,  0x50,  0x01]):
               print('Got device')
               return Res.get_data()['ext']
      
      print('no response device request')

   def Flush_Events(self):
      while (self.Seq.receive_events(maxevents = 200)):
         pass

   def Send_Midi_CC(self, Channel=0, CC=0, Value=0):
      self.Controller.set_data({'control.channel':Channel, 'control.param':CC, 'control.value':Value})
      self.Seq.output_event(self.Controller)
      self.Seq.drain_output()

if (__name__ == '__main__'):
   Nano_Scene = Nano_Kontrol_Scene()
   Midi_Comm = Nano_Kontrol_Alsa_Midi_Comm()
   Midi_Comm.Scene_Change_Request(0)
   #Nano_Scene.Parse_Data(Midi_Comm.Scene_Dump_Request())
