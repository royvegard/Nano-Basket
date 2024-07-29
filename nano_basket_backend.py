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

import struct
import time
from pyalsa import alsaseq


class NanoKontrolCommon:
    """Common parameters from TABLE 1 of 'nanoKONTROL MIDI Implementation'
    file available from Korg."""

    def __init__(self):
        self.scene_name = 'Scene 1'  # ASCII code
        self.scene_midi_channel = 0  # 0~15

    def get_list(self):
        """Return a list of the parameters in the order that they should
        appear in the sysex file."""

        # Scene name must contain exactly 12 bytes, padded with spaces.
        scene_name = (self.scene_name + '             ')[0:12]
        scene_list = list(struct.unpack('12B', scene_name.encode()))
        scene_list.append(self.scene_midi_channel)
        return scene_list


class NanoKontrolBlock:

    def __init__(self):
        self.block_midi_channel = 16  # 0~15/16~=MIDI Ch.0~15/Scene MIDI Ch.
        self.slider_assign_type = 1  # 0/1=No Assign/CC
        self.slider_cc = 1           # 0~127
        self.slider_min_value = 0    # 0~127
        self.slider_max_value = 127  # 0~127

        self.knob_assign_type = 1    # 0/1=No Assign/CC
        self.knob_cc = 1             # 0~127
        self.knob_min_value = 0      # 0~127
        self.knob_max_value = 127    # 0~127

        self.sw_a_assign_type = 1    # 0~2=No Assign/CC/Note
        self.sw_a_cc = 1             # 0~127
        self.sw_a_off_value = 0      # 0~127
        self.sw_a_on_value = 127     # 0~127
        self.sw_a_attack_time = 0    # 0~127
        self.sw_a_release_time = 0   # 0~127
        self.sw_a_switch_type = 0    # 0/1=Momentary/Toggle

        self.sw_b_assign_type = 1    # 0~2=No Assign/CC/Note
        self.sw_b_cc = 1             # 0~127
        self.sw_b_off_value = 0      # 0~127
        self.sw_b_on_value = 127     # 0~127
        self.sw_b_attack_time = 0    # 0~127
        self.sw_b_release_time = 0   # 0~127
        self.sw_b_switch_type = 0    # 0/1=Momentary/Toggle

    def set_midi_channel(self, value):
        if (value > -1 and value < 128):
            self.block_midi_channel = value

    def get_list(self):
        """Return a list of the parameters in the order that they should
        appear in the sysex file."""

        return [self.block_midi_channel,
                self.slider_assign_type,
                self.slider_cc,
                self.slider_min_value,
                self.slider_max_value,
                self.knob_assign_type,
                self.knob_cc,
                self.knob_min_value,
                self.knob_max_value,
                self.sw_a_assign_type,
                self.sw_a_cc,
                self.sw_a_off_value,
                self.sw_a_on_value,
                self.sw_a_attack_time,
                self.sw_a_release_time,
                self.sw_a_switch_type,
                self.sw_b_assign_type,
                self.sw_b_cc,
                self.sw_b_off_value,
                self.sw_b_on_value,
                self.sw_b_attack_time,
                self.sw_b_release_time,
                self.sw_b_switch_type]


class NanoKontrolTransportSwitch:
    def __init__(self):
        self.assign_type = 1   # 0~2=No Assign/CC/MMC
        self.cc = 1            # 0~127
        self.mmc_command = 1   # 0~12
        self.mmc_device_id = 1  # 0~127
        self.switch_type = 0   # 0/1=Momentary/Toggle

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

    def get_list(self):
        """Return a list of the parameters in the order that they should
        appear in the sysex file."""

        return [self.assign_type,
                self.cc,
                self.mmc_command,
                self.mmc_device_id,
                self.switch_type]


class NanoKontrolScene:
    """Contains a complete nanoKONTROL scene."""

    def __init__(self):
        self.common = NanoKontrolCommon()

        self.block_1 = NanoKontrolBlock()
        self.block_2 = NanoKontrolBlock()
        self.block_3 = NanoKontrolBlock()
        self.block_4 = NanoKontrolBlock()
        self.block_5 = NanoKontrolBlock()
        self.block_6 = NanoKontrolBlock()
        self.block_7 = NanoKontrolBlock()
        self.block_8 = NanoKontrolBlock()
        self.block_9 = NanoKontrolBlock()

        self.block = [self.block_1, self.block_2, self.block_3,
                      self.block_4, self.block_5, self.block_6,
                      self.block_7, self.block_8, self.block_9]

        # 0~15/16~=MIDI Ch.0~15/Scene MIDI Ch.
        self.transport_midi_channel = 16
        self.transport_1 = NanoKontrolTransportSwitch()  # REW
        self.transport_2 = NanoKontrolTransportSwitch()  # PLAY
        self.transport_3 = NanoKontrolTransportSwitch()  # FF
        self.transport_4 = NanoKontrolTransportSwitch()  # LOOP
        self.transport_5 = NanoKontrolTransportSwitch()  # STOP
        self.transport_6 = NanoKontrolTransportSwitch()  # REC

        self.transport_button = [self.transport_1, self.transport_2,
                                 self.transport_3, self.transport_4,
                                 self.transport_5, self.transport_6]

    def get_list(self):
        """Return a list of the parameters in the order that they should
        appear in the sysex file."""

        parameter_list = self.common.get_list() + \
            [0, 0, 0] + \
            self.block_1.get_list() + \
            self.block_2.get_list() + \
            self.block_3.get_list() + \
            self.block_4.get_list() + \
            self.block_5.get_list() + \
            self.block_6.get_list() + \
            self.block_7.get_list() + \
            self.block_8.get_list() + \
            self.block_9.get_list() + \
            [0,] + \
            [self.transport_midi_channel,] + \
            self.transport_1.get_list() + \
            self.transport_2.get_list() + \
            self.transport_3.get_list() + \
            self.transport_4.get_list() + \
            self.transport_5.get_list() + \
            self.transport_6.get_list() + \
            [0,]

        return parameter_list

    def parse_data(self, data):
        """ """

        if len(data) != 307:
            return

        data_list = list(data[13:])
        for i in range(37, 0, -1):
            data_list.pop((i-1)*8)

        scene_name = ''
        for i in range(12):
            scene_name += chr(data_list[i])

        self.common.scene_name = scene_name
        self.common.scene_midi_channel = data_list[12]

        i = 0
        for b in self.block:
            b.block_midi_channel = data_list[16+i*23]
            b.slider_assign_type = data_list[17+i*23]
            b.slider_cc = data_list[18+i*23]
            b.slider_min_value = data_list[19+i*23]
            b.slider_max_value = data_list[20+i*23]

            b.knob_assign_type = data_list[21+i*23]
            b.knob_cc = data_list[22+i*23]
            b.knob_min_value = data_list[23+i*23]
            b.knob_max_value = data_list[24+i*23]

            b.sw_a_assign_type = data_list[25+i*23]
            b.sw_a_cc = data_list[26+i*23]
            b.sw_a_off_value = data_list[27+i*23]
            b.sw_a_on_value = data_list[28+i*23]
            b.sw_a_attack_time = data_list[29+i*23]
            b.sw_a_release_time = data_list[30+i*23]
            b.sw_a_switch_type = data_list[31+i*23]

            b.sw_b_assign_type = data_list[32+i*23]
            b.sw_b_cc = data_list[33+i*23]
            b.sw_b_off_value = data_list[34+i*23]
            b.sw_b_on_value = data_list[35+i*23]
            b.sw_b_attack_time = data_list[36+i*23]
            b.sw_b_release_time = data_list[37+i*23]
            b.sw_b_switch_type = data_list[38+i*23]

            i += 1

        self.transport_midi_channel = data_list[224]

        i = 0
        for b in self.transport_button:
            b.assign_type = data_list[225+i*5]
            b.cc = data_list[226+i*5]
            b.mmc_command = data_list[227+i*5]
            b.mmc_device_id = data_list[228+i*5]
            b.switch_type = data_list[229+i*5]

            i += 1


class NanoKontrolAlsaMidiComm:
    """Communicates with the device."""

    def __init__(self, midi_port_name='Nano Basket MIDI 1'):
        self.seq = alsaseq.Sequencer(clientname='Nano Basket')
        self.event = alsaseq.SeqEvent(alsaseq.SEQ_EVENT_SYSEX)
        self.controller = alsaseq.SeqEvent(alsaseq.SEQ_EVENT_CONTROLLER)
        self.port = self.seq.create_simple_port(name=midi_port_name,
                                                type=alsaseq.SEQ_PORT_TYPE_APPLICATION,
                                                caps=alsaseq.SEQ_PORT_CAP_SUBS_READ |
                                                alsaseq.SEQ_PORT_CAP_READ |
                                                alsaseq.SEQ_PORT_CAP_WRITE |
                                                alsaseq.SEQ_PORT_CAP_SUBS_WRITE)

        self.response_wait = 0.2
        self.connect_midi_ports()

    def scene_change_request(self, scene_number=0):
        """Sends a scene change request to the device."""

        if scene_number > 3:
            scene_number = 3
        elif scene_number < 0:
            scene_number = 0

        global_channel = self.search_device_request()[4]
        sysex = [0xf0, 0x42]  # Exclusive Header
        sysex.extend([0x40 + global_channel])
        # Software Project (nanoKONTROL: 000104H)
        sysex.extend([0x00, 0x01, 0x04, 0x00])
        # Data Dump Command  (Host->Controller, 2Bytes Format)
        sysex.extend([0x1f])
        sysex.extend([0x14])  # Scene Change Request
        sysex.extend([scene_number])
        sysex.extend([0xf7])  # End of Exclusive (EOX)

        self.flush_events()

        self.event.set_data({'ext': sysex})
        self.seq.output_event(self.event)
        self.seq.drain_output()
        time.sleep(self.response_wait)
        response = self.seq.receive_events(timeout=1000, maxevents=200)

        for res in response:
            if 'ext' in res.get_data().keys():
                print("Reply " + " ".join("{:02x}".format(x)
                      for x in res.get_data()['ext']))
                if res.get_data()['ext'][9] == scene_number:
                    print('Scene change Success!')
                    return True

    def scene_upload_request(self, scene_list, scene_number=None):
        """Writes a scene configuration to the device.
        Note that the configuration is only temporarily stored.
        To permanently write it to the device's memory, issue
        a Scene_Write_Request."""

        # Inser a '0' every 8th index
        for i in range(37):
            scene_list.insert(i*8, 0)

        global_channel = self.search_device_request()[4]
        sysex = [0xf0,  0x42]  # Exclusive Header
        sysex.extend([0x40 + global_channel])
        # Software Project (nanoKONTROL: 000104H)
        sysex.extend([0x00,  0x01,  0x04,  0x00])
        # Data Dump Command  (Host<->Controller, Variable Format)
        sysex.extend([0x7f])
        sysex.extend([0x7f])  # Over 0x7F Data
        sysex.extend([0x02])  # 2Bytes structure
        sysex.extend([0x02])  # Num of Data MSB (1+293 bytes : B'100100110)
        sysex.extend([0x26])  # Num of Data LSB
        sysex.extend([0x40])  # Current Scene Data Dump
        sysex.extend(scene_list)  # Data
        sysex.extend([0xf7])  # End of Exclusive (EOX)

        self.flush_events()

        if scene_number:
            self.scene_change_request(scene_number)

        self.event.set_data({'ext': sysex})
        self.seq.output_event(self.event)
        self.seq.drain_output()
        time.sleep(self.response_wait)
        response = self.seq.receive_events(timeout=1000, maxevents=200)

        for res in response:
            if 'ext' in res.get_data().keys():
                print("Reply " + " ".join("{:02x}".format(x)
                      for x in res.get_data()['ext']))
                if res.get_data()['ext'][8] == 0x23:
                    print('Data load Success!')
                elif res.get_data()['ext'][8] == 0x24:
                    print('Data load Fail!')

    def scene_dump_request(self, scene_number=None):
        """Reads the scene configuration from the device."""

        if scene_number:
            self.scene_change_request(scene_number)

        global_channel = self.search_device_request()[4]
        sysex = [0xf0,  0x42]  # Exclusive Header
        sysex.extend([0x40 + global_channel])
        # Software Project (nanoKONTROL: 000104H)
        sysex.extend([0x00,  0x01,  0x04,  0x00])
        # Data Dump Command  (Host->Controller, 2Bytes Format)
        sysex.extend([0x1f])
        sysex.extend([0x10])  # Scene Dump Request
        sysex.extend([0x00])  # Padding
        sysex.extend([0xf7])  # End of Exclusive (EOX)

        self.flush_events()

        self.event.set_data({'ext': sysex})
        self.seq.output_event(self.event)
        self.seq.drain_output()
        time.sleep(self.response_wait)
        response = self.seq.receive_events(timeout=1000, maxevents=200)

        data = []
        for res in response:
            if 'ext' in res.get_data().keys():
                print("Reply " + " ".join("{:02x}".format(x)
                      for x in res.get_data()['ext']))
                data.extend(res.get_data()['ext'])
        return data

    def scene_write_request(self, scene_number=0):
        """Writes the current scene data into the internal memory.
        Normally used after a Scene_Upload_Request to permanently
        store the new scene configuration."""

        if scene_number > 3:
            scene_number = 3
        elif scene_number < 0:
            scene_number = 0

        global_channel = self.search_device_request()[4]
        sysex = [0xf0,  0x42]  # Exclusive Header
        sysex.extend([0x40 + global_channel])
        # Software Project (nanoKONTROL: 000104H)
        sysex.extend([0x00,  0x01,  0x04,  0x00])
        # Data Dump Command  (Host->Controller, 2Bytes Format)
        sysex.extend([0x1f])
        sysex.extend([0x11])  # Scene Write Request
        sysex.extend([scene_number])
        sysex.extend([0xf7])  # End of Exclusive (EOX)

        self.flush_events()

        self.event.set_data({'ext': sysex})
        self.seq.output_event(self.event)
        self.seq.drain_output()
        time.sleep(self.response_wait)
        response = self.seq.receive_events(timeout=1000, maxevents=200)

        for res in response:
            if 'ext' in res.get_data().keys():
                print("Reply " + " ".join("{:02x}".format(x)
                      for x in res.get_data()['ext']))
                if res.get_data()['ext'][8] == 0x21:
                    print('Data write Success!')
                elif res.get_data()['ext'][8] == 0x22:
                    print('Data write Fail!')
                elif res.get_data()['ext'][8] == 0x4f:
                    print('Scene change')

    def search_device_request(self):
        sysex = [0xf0,  0x42,  0x50]  # Exclusive Header
        sysex.extend([0x00,  0x01])
        sysex.extend([0xf7])  # End of Exclusive (EOX)

        self.flush_events()

        self.event.set_data({'ext': sysex})
        self.seq.output_event(self.event)
        self.seq.drain_output()
        time.sleep(self.response_wait)
        response = self.seq.receive_events(timeout=1000, maxevents=200)

        for res in response:
            if 'ext' in res.get_data().keys():
                print("Reply " + " ".join("{:02x}".format(x)
                      for x in res.get_data()['ext']))
                if (res.get_data()['ext'][0:4] == [0xf0,  0x42,  0x50,  0x01]):
                    print('Got device')
                    return res.get_data()['ext']

        print('no response device request')

    def flush_events(self):
        while self.seq.receive_events(maxevents=200):
            pass

    def send_midi_cc(self, channel=0, cc=0, value=0):
        self.controller.set_data(
            {'control.channel': channel, 'control.param': cc, 'control.value': value})
        self.seq.output_event(self.controller)
        self.seq.drain_output()

    def send_midi_mmc(self, device_id=0, command=1):
        mmc_message = [0xf0, 0x7f, device_id, 0x06, command, 0xf7]
        self.event.set_data({'ext': mmc_message})
        self.seq.output_event(self.event)
        self.seq.drain_output()

    def connect_midi_ports(self):
        clients = self.seq.connection_list()
        client_name = ""
        nano_kontrol_client = None
        nano_kontrol_port = None
        for client in clients:
            client_name = client[0]
            if client_name.find("nanoKONTROL") > -1:
                nano_kontrol_client = client
                print("Found client", client_name)
                port_name = ""
                for port in nano_kontrol_client[2]:
                    port_name = port[0]
                    if port_name.find("CTRL") > -1:
                        print("Found port:", port_name)
                        nano_kontrol_port = port
                        break
                break

        if (nano_kontrol_client and nano_kontrol_port):
            self.seq.connect_ports(
                (nano_kontrol_client[1], nano_kontrol_port[1]), (self.seq.client_id, self.port))
            self.seq.connect_ports((self.seq.client_id, self.port),
                (nano_kontrol_client[1], nano_kontrol_port[1]))
            print("Connected")


if __name__ == '__main__':
    Nano_Scene = NanoKontrolScene()
    Midi_Comm = NanoKontrolAlsaMidiComm()
    Midi_Comm.scene_change_request(0)
    # Nano_Scene.Parse_Data(Midi_Comm.Scene_Dump_Request())
