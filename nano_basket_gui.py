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
from gi.repository import Gtk, Gdk


class KontrolBlock:
    def __init__(self, index, fader_event, focus_event, button_pressed_event, button_released_event):
        self.index = index
        self.table = Gtk.Table(rows=4, columns=2)
        self.label = Gtk.Label()
        self.label.set_markup(
            '<span foreground="black"> {0} </span>'.format(self.index + 1))
        adj = Gtk.Adjustment(value=0, lower=0, upper=127,
                             step_incr=1, page_incr=5, page_size=0)
        adj.connect("value_changed", fader_event, {
                    'Block': self.index, 'Type': 'Slider'})
        self.slider = Gtk.VScale(adjustment=adj)
        self.slider.set_draw_value(draw_value=False)
        self.slider.set_inverted(setting=True)
        self.slider.connect("focus-in-event", focus_event,
                            {'Block': self.index, 'Widget': 'Slider', 'Widget_Type': 'Slider'})
        adj = Gtk.Adjustment(value=0, lower=0, upper=127,
                             step_incr=1, page_incr=5, page_size=0)
        adj.connect("value_changed", fader_event, {
                    'Block': self.index, 'Type': 'Knob'})
        self.knob = Gtk.HScale(adjustment=adj)
        self.knob.set_draw_value(draw_value=False)
        self.knob.connect("focus-in-event", focus_event,
                          {'Block': self.index, 'Widget': 'Knob', 'Widget_Type': 'Slider'})
        self.button_a = Gtk.ToggleButton(label='A')
        self.button_a.connect("focus-in-event", focus_event,
                              {'Block': self.index, 'Widget': 'Button_A', 'Widget_Type': 'Button'})
        self.button_a.connect("pressed", button_pressed_event,
                              {'Block': self.index, 'Widget': 'Button_A'})
        self.button_a.connect("released", button_released_event,
                              {'Block': self.index, 'Widget': 'Button_A'})
        self.button_b = Gtk.ToggleButton(label='B')
        self.button_b.connect("focus-in-event", focus_event,
                              {'Block': self.index, 'Widget': 'Button_B', 'Widget_Type': 'Button'})
        self.button_b.connect("pressed", button_pressed_event,
                              {'Block': self.index, 'Widget': 'Button_B'})
        self.button_b.connect("released", button_released_event,
                              {'Block': self.index, 'Widget': 'Button_B'})
        self.table.attach(child=self.label,
                          left_attach=0,
                          right_attach=1,
                          top_attach=0,
                          bottom_attach=1,
                          yoptions=Gtk.AttachOptions.FILL)
        self.label.show()
        self.table.attach(child=self.slider,
                          left_attach=1,
                          right_attach=2,
                          top_attach=1,
                          bottom_attach=3)
        self.slider.show()
        self.table.attach(child=self.knob,
                          left_attach=1,
                          right_attach=2,
                          top_attach=0,
                          bottom_attach=1,
                          yoptions=Gtk.AttachOptions.FILL)
        self.knob.show()
        self.table.attach(child=self.button_a,
                          left_attach=0,
                          right_attach=1,
                          top_attach=1,
                          bottom_attach=2)
        self.button_a.show()
        self.table.attach(child=self.button_b,
                          left_attach=0,
                          right_attach=1,
                          top_attach=2,
                          bottom_attach=3)
        self.button_b.show()
        self.table.show()


class NanoKontrolGui:
    def delete_event(self, widget, event, data=None):
        Gtk.main_quit()
        return False

    def focus_event(self, widget, event, data=None):
        """Triggered when the focus-in-event is sent, i.e. whenever we need to change
        the control widgets."""

        print('Focus_Event')
        self.current_widget = data['Widget']
        self.current_widget_type = data['Widget_Type']

        # Show the appropriate control widgets.
        if self.current_widget_type == 'Slider':
            self.current_block = data['Block']
            self.button_control_table.hide()
            self.transport_control_table.hide()
            self.slider_knob_control_table.show()
            self.block_midi_channel.set_active(
                self.scene[self.current_scene].block[self.current_block].block_midi_channel)
        elif self.current_widget_type == 'Button':
            self.current_block = data['Block']
            self.slider_knob_control_table.hide()
            self.transport_control_table.hide()
            self.button_control_table.show()
            self.block_midi_channel.set_active(
                self.scene[self.current_scene].block[self.current_block].block_midi_channel)
        elif self.current_widget_type == 'Transport':
            self.slider_knob_control_table.hide()
            self.button_control_table.hide()
            self.transport_control_table.show()

        # Read values from the backend datastore into the control widgets.
        self.scene_midi_channel.set_active(
            self.scene[self.current_scene].common.scene_midi_channel)
        self.scene_name.set_text(
            text=self.scene[self.current_scene].common.scene_name)
        self.transport_midi_channel.set_active(
            self.scene[self.current_scene].transport_midi_channel)

        if self.current_widget == 'Slider':
            self.slider_assign_type.set_active(
                self.scene[self.current_scene].block[self.current_block].slider_assign_type)
            self.slider_cc.set_value(
                self.scene[self.current_scene].block[self.current_block].slider_cc)
            self.slider_min_value.set_value(
                self.scene[self.current_scene].block[self.current_block].slider_min_value)
            self.slider_max_value.set_value(
                self.scene[self.current_scene].block[self.current_block].slider_max_value)
        elif self.current_widget == 'Knob':
            self.slider_assign_type.set_active(
                self.scene[self.current_scene].block[self.current_block].knob_assign_type)
            self.slider_cc.set_value(
                self.scene[self.current_scene].block[self.current_block].knob_cc)
            self.slider_min_value.set_value(
                self.scene[self.current_scene].block[self.current_block].knob_min_value)
            self.slider_max_value.set_value(
                self.scene[self.current_scene].block[self.current_block].knob_max_value)
        elif self.current_widget == 'Button_A':
            self.button_assign_type.set_active(
                self.scene[self.current_scene].block[self.current_block].sw_a_assign_type)
            self.button_cc.set_value(
                self.scene[self.current_scene].block[self.current_block].sw_a_cc)
            self.button_off_value.set_value(
                self.scene[self.current_scene].block[self.current_block].sw_a_off_value)
            self.button_on_value.set_value(
                self.scene[self.current_scene].block[self.current_block].sw_a_on_value)
            self.button_attack_time.set_value(
                self.scene[self.current_scene].block[self.current_block].sw_a_attack_time)
            self.button_release_time.set_value(
                self.scene[self.current_scene].block[self.current_block].sw_a_release_time)
            self.button_switch_type.set_active(
                self.scene[self.current_scene].block[self.current_block].sw_a_switch_type)
        elif self.current_widget == 'Button_B':
            self.button_assign_type.set_active(
                self.scene[self.current_scene].block[self.current_block].sw_b_assign_type)
            self.button_cc.set_value(
                self.scene[self.current_scene].block[self.current_block].sw_b_cc)
            self.button_off_value.set_value(
                self.scene[self.current_scene].block[self.current_block].sw_b_off_value)
            self.button_on_value.set_value(
                self.scene[self.current_scene].block[self.current_block].sw_b_on_value)
            self.button_attack_time.set_value(
                self.scene[self.current_scene].block[self.current_block].sw_b_attack_time)
            self.button_release_time.set_value(
                self.scene[self.current_scene].block[self.current_block].sw_b_release_time)
            self.button_switch_type.set_active(
                self.scene[self.current_scene].block[self.current_block].sw_b_switch_type)
        elif self.current_widget in range(6):
            self.transport_assign_type.set_active(
                self.scene[self.current_scene].transport_button[self.current_widget].assign_type)
            self.transport_cc.set_value(
                self.scene[self.current_scene].transport_button[self.current_widget].cc)
            self.transport_mmc_command.set_active(
                self.scene[self.current_scene].transport_button[self.current_widget].mmc_command)
            self.transport_mmc_dev_id.set_value(
                self.scene[self.current_scene].transport_button[self.current_widget].mmc_device_id)
            self.transport_switch_type.set_active(
                self.scene[self.current_scene].transport_button[self.current_widget].switch_type)

        # Emphasize the current widget.
        if widget:
            highlight_color = Gdk.Color(red=0, green=65535, blue=0)
            normal_color = self.scene_button.get_style().white

            for child in self.transport_table.get_children():
                child.modify_bg(state=Gtk.StateType.NORMAL, color=normal_color)

            for block in self.kontrol_blocks:
                for child in block.table.get_children():
                    child.modify_bg(state=Gtk.StateType.NORMAL,
                                    color=normal_color)

            widget.modify_bg(state=Gtk.StateType.NORMAL, color=highlight_color)

    def spin_event(self, widget, data=None):
        """Triggered when a spinbox widget's value is changed. The changed value
        is stored in the backend datastore."""

        print('Spin_Event')
        value = widget.get_value_as_int()
        input_widget = data['Widget']

        # Read value from widget, and store the value in the backend datastore.
        if self.current_widget == 'Slider':
            if input_widget == 'CC':
                self.scene[self.current_scene].block[self.current_block].slider_cc = value
            elif input_widget == 'Min_Value':
                self.scene[self.current_scene].block[self.current_block].slider_min_value = value
            elif input_widget == 'Max_Value':
                self.scene[self.current_scene].block[self.current_block].slider_max_value = value

        elif self.current_widget == 'Knob':
            if input_widget == 'CC':
                self.scene[self.current_scene].block[self.current_block].knob_cc = value
            elif input_widget == 'Min_Value':
                self.scene[self.current_scene].block[self.current_block].knob_min_value = value
            elif input_widget == 'Max_Value':
                self.scene[self.current_scene].block[self.current_block].knob_max_value = value

        elif self.current_widget == 'Button_A':
            if input_widget == 'CC':
                self.scene[self.current_scene].block[self.current_block].sw_a_cc = value
            elif input_widget == 'Off_Value':
                self.scene[self.current_scene].block[self.current_block].sw_a_off_value = value
            elif input_widget == 'On_Value':
                self.scene[self.current_scene].block[self.current_block].sw_a_on_value = value
            elif input_widget == 'Attack_Time':
                self.scene[self.current_scene].block[self.current_block].sw_a_attack_time = value
            elif input_widget == 'Release_Time':
                self.scene[self.current_scene].block[self.current_block].sw_a_release_time = value

        elif self.current_widget == 'Button_B':
            if input_widget == 'CC':
                self.scene[self.current_scene].block[self.current_block].sw_b_cc = value
            elif input_widget == 'Off_Value':
                self.scene[self.current_scene].block[self.current_block].sw_b_off_value = value
            elif input_widget == 'On_Value':
                self.scene[self.current_scene].block[self.current_block].sw_b_on_value = value
            elif input_widget == 'Attack_Time':
                self.scene[self.current_scene].block[self.current_block].sw_b_attack_time = value
            elif input_widget == 'Release_Time':
                self.scene[self.current_scene].block[self.current_block].sw_b_release_time = value

        elif self.current_widget in range(6):
            if input_widget == 'CC':
                self.scene[self.current_scene].transport_button[self.current_widget].cc = value
            elif input_widget == 'MMC_Dev_ID':
                self.scene[self.current_scene].transport_button[self.current_widget].mmc_device_id = value

    def combo_event(self, widget, data=None):
        """Triggered when combobox widget's value (index) is changed.
        The changed value (index) is stored in the backend datastore."""

        print('Combo_Event')
        value = widget.get_active()
        input_widget = data['Widget']

        # Read value from widget, and store the value in the backend datastore.
        if input_widget == 'Scene_Midi_Channel':
            self.scene[self.current_scene].common.scene_midi_channel = value

        elif input_widget == 'Block_Midi_Channel':
            self.scene[self.current_scene].block[self.current_block].block_midi_channel = value

        elif input_widget == 'Transport_Midi_Channel':
            self.scene[self.current_scene].transport_midi_channel = value

        elif self.current_widget == 'Slider':
            if input_widget == 'Assign_Type':
                self.scene[self.current_scene].block[self.current_block].slider_assign_type = value

        elif self.current_widget == 'Knob':
            if input_widget == 'Assign_Type':
                self.scene[self.current_scene].block[self.current_block].knob_assign_type = value

        elif self.current_widget == 'Button_A':
            if input_widget == 'Assign_Type':
                self.scene[self.current_scene].block[self.current_block].sw_a_assign_type = value
            elif input_widget == 'Switch_Type':
                self.scene[self.current_scene].block[self.current_block].sw_a_switch_type = value

        elif self.current_widget == 'Button_B':
            if input_widget == 'Assign_Type':
                self.scene[self.current_scene].block[self.current_block].sw_b_assign_type = value
            elif input_widget == 'Switch_Type':
                self.scene[self.current_scene].block[self.current_block].sw_b_switch_type = value

        elif self.current_widget in range(6):
            if input_widget == 'Assign_Type':
                self.scene[self.current_scene].transport_button[self.current_widget].assign_type = value
            elif input_widget == 'MMC_Command':
                self.scene[self.current_scene].transport_button[self.current_widget].mmc_command = value
            elif input_widget == 'Switch_Type':
                self.scene[self.current_scene].transport_button[self.current_widget].switch_type = value

        return False

    def entry_event(self, widget, event, data=None):
        print('Entry_Event')
        value = widget.get_text()
        input_widget = data['Widget']

        # Read value from widget, and store the value in the backend datastore.
        if input_widget == 'Scene_Name':
            self.scene[self.current_scene].common.scene_name = value

        return False

    def scene_cycle_event(self, widget, data=None):
        """Triggered when the Scene button is pressed. The current scene is cycled
        through the scenes."""

        print('Scene_Cycle_Event')
        radio_buttons = self.scene_1_light.get_group()
        # Sort the list so that they are in the correct order.
        radio_buttons.sort(key=Gtk.RadioButton.get_name)

        for i in range(len(radio_buttons)):
            if i == len(radio_buttons)-1:
                # If we come this far, we need to wrap around to the first.
                radio_buttons[0].set_active(is_active=True)
                break
            elif radio_buttons[i].get_active():
                radio_buttons[i+1].set_active(is_active=True)
                break

        return False

    def scene_change_event(self, widget, data=None):
        """Triggered when any of the scene radio buttons are clicked.
        Sets the current scene to the clicked radio button."""

        # TODO: This gets triggered several times when the scene
        # or the scene radio buttons are clicked.
        # PRIORITY: LOW

        print('Scene_Change_Event')
        radio_buttons = self.scene_1_light.get_group()
        radio_buttons.sort(key=Gtk.RadioButton.get_name)

        for i in range(len(radio_buttons)):
            if radio_buttons[i].get_active():
                self.current_scene = i

        # Fire off the Focus_Event so that the control widgets
        # get populated with values from the new scene.
        self.focus_event(widget=None, event=None,
                         data={'Block': self.current_block, 'Widget': self.current_widget, 'Widget_Type': self.current_widget_type})
        return False

    def upload_scene_event(self, widget, data=None):
        try:
            self.midi_comm.scene_change_request(
                Scene_Number=self.current_scene)
            scene_list = self.scene[self.current_scene].get_list()
            self.midi_comm.scene_upload_request(
                Scene_List=scene_list, Scene_Number=self.current_scene)
            self.midi_comm.scene_write_request(Scene_Number=self.current_scene)
        except:
            self.status_bar.push(
                context_id=self.status_bar_context_id, text='Error:Upload Scene failed')
            return False

        self.status_bar.push(
            context_id=self.status_bar_context_id, text='Uploaded Scene to device')
        return False

    def download_scene_event(self, widget, data=None):
        try:
            self.midi_comm.scene_change_request(
                scene_number=self.current_scene)
            scene_data = self.midi_comm.scene_dump_request()
            self.scene[self.current_scene].parse_data(scene_data)
        except:
            self.status_bar.push(
                context_id=self.status_bar_context_id, text='Error: Download Scene failed')
            return False
        # Fire off the Focus_Event so that the control widgets
        # get populated with values from the new scene.
        self.focus_event(widget=None, event=None,
                         data={'Block': self.current_block, 'Widget': self.current_widget, 'Widget_Type': self.current_widget_type})
        self.status_bar.push(
            context_id=self.status_bar_context_id, text='Downloaded Scene from device')
        return False

    def copy_scene_event(self, widget, data=None):
        self.scene[-1] = copy.deepcopy(self.scene[self.current_scene])
        return False

    def paste_scene_event(self, widget, data=None):
        self.scene[self.current_scene] = copy.deepcopy(self.scene[-1])
        # Fire off the Focus_Event so that the control widgets
        # get populated with values from the new scene.
        self.focus_event(widget=None, event=None,
                         data={'Block': self.current_block, 'Widget': self.current_widget, 'Widget_Type': self.current_widget_type})
        return False

    def fader_event(self, widget, data=None):
        print('Fader Event')
        print(widget.get_value())
        print('Block: ' + str(data['Block']))
        if data['Type'] == 'Slider':
            assign_type = self.scene[self.current_scene].block[data['Block']
                                                               ].slider_assign_type
            cc_number = self.scene[self.current_scene].block[data['Block']].slider_cc
            min_value = self.scene[self.current_scene].block[data['Block']
                                                             ].slider_min_value
            max_value = self.scene[self.current_scene].block[data['Block']
                                                             ].slider_max_value
        elif data['Type'] == 'Knob':
            assign_type = self.scene[self.current_scene].block[data['Block']
                                                               ].knob_assign_type
            cc_number = self.scene[self.current_scene].block[data['Block']].knob_cc
            min_value = self.scene[self.current_scene].block[data['Block']
                                                             ].knob_min_value
            max_value = self.scene[self.current_scene].block[data['Block']
                                                             ].knob_max_value

        block_midi_channel = self.scene[self.current_scene].block[data['Block']
                                                                  ].block_midi_channel
        midi_channel = block_midi_channel
        if midi_channel == 16:
            midi_channel = self.scene[self.current_scene].common.scene_midi_channel

        print('Max value: ' + str(max_value))
        print('Min value: ' + str(min_value))
        print('CC number: ' + str(cc_number))
        print('Assign type: ' + str(assign_type))
        print('Midi Channel: ' + str(midi_channel))
        midi_value = int((widget.get_value()/127.0 *
                         (max_value - min_value) + min_value) + 0.5)
        print('Midi Value: ' + str(midi_value))

        if assign_type == 1:
            self.midi_comm.send_midi_cc(
                channel=midi_channel, cc=cc_number, value=midi_value)

        return False

    def button_pressed_event(self, widget, data=None):
        print('Button Pressed Event')
        if data['Widget'] == 'Button_A':
            assign_type = self.scene[self.current_scene].block[data['Block']
                                                               ].sw_a_assign_type
            cc_number = self.scene[self.current_scene].block[data['Block']].sw_a_cc
            off_value = self.scene[self.current_scene].block[data['Block']
                                                             ].sw_a_off_value
            on_value = self.scene[self.current_scene].block[data['Block']].sw_a_on_value
            switch_type = self.scene[self.current_scene].block[data['Block']
                                                               ].sw_a_switch_type
        elif data['Widget'] == 'Button_B':
            assign_type = self.scene[self.current_scene].block[data['Block']
                                                               ].sw_b_assign_type
            cc_number = self.scene[self.current_scene].block[data['Block']].sw_b_cc
            off_value = self.scene[self.current_scene].block[data['Block']
                                                             ].sw_b_off_value
            on_value = self.scene[self.current_scene].block[data['Block']].sw_b_on_value
            switch_type = self.scene[self.current_scene].block[data['Block']
                                                               ].sw_b_switch_type

        block_midi_channel = self.scene[self.current_scene].block[data['Block']
                                                                  ].block_midi_channel
        midi_channel = block_midi_channel
        if midi_channel == 16:
            midi_channel = self.scene[self.current_scene].common.scene_midi_channel

        print('On value: ' + str(on_value))
        print('Off value: ' + str(off_value))
        print('CC number: ' + str(cc_number))
        print('Assign type: ' + str(assign_type))
        print('Midi Channel: ' + str(midi_channel))
        print('Switch Type: ' + str(switch_type))
        print(widget.get_active())

        if assign_type == 1:
            if switch_type == 0:
                self.midi_comm.send_midi_cc(
                    channel=midi_channel, cc=cc_number, value=on_value)
                widget.set_active(True)
            elif switch_type == 1:
                toggle_state = widget.get_active()
                if toggle_state:
                    self.midi_comm.send_midi_cc(
                        channel=midi_channel, cc=cc_number, value=off_value)
                elif not toggle_state:
                    self.midi_comm.send_midi_cc(
                        channel=midi_channel, cc=cc_number, value=on_value)

        return False

    def button_released_event(self, widget, data=None):
        print('Button Released Event')
        if data['Widget'] == 'Button_A':
            assign_type = self.scene[self.current_scene].block[data['Block']
                                                               ].sw_a_assign_type
            cc_number = self.scene[self.current_scene].block[data['Block']].sw_a_cc
            off_value = self.scene[self.current_scene].block[data['Block']
                                                             ].sw_a_off_value
            on_value = self.scene[self.current_scene].block[data['Block']].sw_a_on_value
            switch_type = self.scene[self.current_scene].block[data['Block']
                                                               ].sw_a_switch_type
        elif data['Widget'] == 'Button_B':
            assign_type = self.scene[self.current_scene].block[data['Block']
                                                               ].sw_b_assign_type
            cc_number = self.scene[self.current_scene].block[data['Block']].sw_b_cc
            off_value = self.scene[self.current_scene].block[data['Block']
                                                             ].sw_b_off_value
            on_value = self.scene[self.current_scene].block[data['Block']].sw_b_on_value
            switch_type = self.scene[self.current_scene].block[data['Block']
                                                               ].sw_b_switch_type

        block_midi_channel = self.scene[self.current_scene].block[data['Block']
                                                                  ].block_midi_channel
        midi_channel = block_midi_channel
        if midi_channel == 16:
            midi_channel = self.scene[self.current_scene].common.scene_midi_channel

        print('On value: ' + str(on_value))
        print('Off value: ' + str(off_value))
        print('CC number: ' + str(cc_number))
        print('Assign type: ' + str(assign_type))
        print('Midi Channel: ' + str(midi_channel))
        print('Switch Type: ' + str(switch_type))

        if (assign_type == 1 and switch_type == 0):
            self.midi_comm.send_midi_cc(
                channel=midi_channel, cc=cc_number, value=off_value)

        return False

    def transport_button_pressed_event(self, widget, data=None):
        print('Transport_Button_Pressed_Event')
        assign_type = self.scene[self.current_scene].transport_button[data['Button']].assign_type
        cc_number = self.scene[self.current_scene].transport_button[data['Button']].cc
        mmc_command = self.scene[self.current_scene].transport_button[data['Button']].mmc_command + 1
        mmc_device_id = self.scene[self.current_scene].transport_button[data['Button']].mmc_device_id
        switch_type = self.scene[self.current_scene].transport_button[data['Button']].switch_type

        print('Assign type: ' + str(assign_type))
        print('CC: ' + str(cc_number))
        print('MMC Command: ' + str(mmc_command))
        print('MMC Device ID: ' + str(mmc_device_id))
        print('Switch Type: ' + str(switch_type))

        if assign_type == 1:
            transport_midi_channel = self.scene[self.current_scene].transport_midi_channel
            midi_channel = transport_midi_channel
            if midi_channel == 16:
                midi_channel = self.scene[self.current_scene].common.scene_midi_channel
            if switch_type == 0:
                self.midi_comm.send_midi_cc(
                    channel=midi_channel, cc=cc_number, value=127)
                widget.set_active(True)
            elif switch_type == 1:
                toggle_state = widget.get_active()
                if toggle_state:
                    self.midi_comm.send_midi_cc(
                        channel=midi_channel, cc=cc_number, value=0)
                elif not toggle_state:
                    self.midi_comm.send_midi_cc(
                        channel=midi_channel, cc=cc_number, value=127)

        elif assign_type == 2:
            self.midi_comm.send_midi_mmc(
                device_id=mmc_device_id, command=mmc_command)
            widget.set_active(True)

        return False

    def transport_button_released_event(self, widget, data=None):
        assign_type = self.scene[self.current_scene].transport_button[data['Button']].assign_type
        cc_number = self.scene[self.current_scene].transport_button[data['Button']].cc
        mmc_command = self.scene[self.current_scene].transport_button[data['Button']].mmc_command + 1
        mmc_device_id = self.scene[self.current_scene].transport_button[data['Button']].mmc_device_id
        switch_type = self.scene[self.current_scene].transport_button[data['Button']].switch_type

        print('Assign type: ' + str(assign_type))
        print('CC: ' + str(cc_number))
        print('MMC Command: ' + str(mmc_command))
        print('MMC Device ID: ' + str(mmc_device_id))
        print('Switch Type: ' + str(switch_type))

        transport_midi_channel = self.scene[self.current_scene].transport_midi_channel
        midi_channel = transport_midi_channel
        if midi_channel == 16:
            midi_channel = self.scene[self.current_scene].common.scene_midi_channel

        if (assign_type == 1 and switch_type == 0):
            self.midi_comm.send_midi_cc(
                channel=midi_channel, cc=cc_number, value=0)

        return False

    def __init__(self, scene, midi_device):
        self.scene = scene
        self.current_scene = scene
        self.midi_comm = midi_device
        self.current_block = 0
        self.current_widget = None
        self.current_widget_type = None

        self.window = Gtk.ApplicationWindow(title="Nano")
        self.window.connect("delete_event", self.delete_event, None)

        # # # # Menu # # # #
        ####################
        self.menu_bar = Gtk.MenuBar()
        self.file_menu = Gtk.Menu()
        self.file_open = Gtk.MenuItem(label='Open...')
        self.file_save = Gtk.MenuItem(label='Save...')
        self.file_upload_scene = Gtk.MenuItem(label='Upload Scene to Device')
        self.file_upload_scene.connect("activate", self.upload_scene_event)
        self.file_download_scene = Gtk.MenuItem(
            label='Download Scene from Device')
        self.file_download_scene.connect("activate", self.download_scene_event)

        self.file_quit = Gtk.MenuItem(label='Quit')
        self.file_quit.connect("activate", lambda w: Gtk.main_quit())

        self.file_menu.append(child=self.file_open)
        self.file_open.show()
        self.file_menu.append(child=self.file_save)
        self.file_save.show()
        self.file_menu.append(child=self.file_upload_scene)
        self.file_upload_scene.show()
        self.file_menu.append(child=self.file_download_scene)
        self.file_download_scene.show()
        self.file_menu.append(child=self.file_quit)
        self.file_quit.show()

        self.file_menu_item = Gtk.MenuItem(label='File')
        self.file_menu_item.show()
        self.file_menu_item.set_submenu(submenu=self.file_menu)

        self.edit_menu = Gtk.Menu()
        self.edit_copy = Gtk.MenuItem(label='Copy Scene')
        self.edit_copy.connect("activate", self.copy_scene_event)
        self.edit_paste = Gtk.MenuItem(label='Paste Scene')
        self.edit_paste.connect("activate", self.paste_scene_event)

        self.edit_menu.append(child=self.edit_copy)
        self.edit_menu.append(child=self.edit_paste)
        self.edit_copy.show()
        self.edit_paste.show()

        self.edit_menu_item = Gtk.MenuItem(label='Edit')
        self.edit_menu_item.show()
        self.edit_menu_item.set_submenu(submenu=self.edit_menu)

        self.menu_bar.append(child=self.file_menu_item)
        self.menu_bar.append(child=self.edit_menu_item)
        self.menu_bar.show()

        self.v_box_top = Gtk.VBox()
        self.v_box_top.pack_start(
            child=self.menu_bar, expand=False, fill=False, padding=2)
        self.h_box_level_1 = Gtk.HBox()

        # # # # Transport and Scene Buttons # # # #
        ###########################################
        self.transport_table = Gtk.Table(rows=3, columns=3)
        self.transport_rewind = Gtk.ToggleButton(label='REW')
        self.transport_rewind.connect("focus-in-event", self.focus_event,
                                      {'Widget': 0, 'Widget_Type': 'Transport'})
        self.transport_rewind.connect("pressed", self.transport_button_pressed_event,
                                      {'Widget': 'Transport', 'Button': 0})
        self.transport_rewind.connect("released", self.transport_button_released_event,
                                      {'Widget': 'Transport', 'Button': 0})

        self.transport_play = Gtk.ToggleButton(label='PLAY')
        self.transport_play.connect("focus-in-event", self.focus_event,
                                    {'Widget': 1, 'Widget_Type': 'Transport'})
        self.transport_play.connect("pressed", self.transport_button_pressed_event,
                                    {'Widget': 'Transport', 'Button': 1})
        self.transport_play.connect("released", self.transport_button_released_event,
                                    {'Widget': 'Transport', 'Button': 1})

        self.transport_fast_forward = Gtk.ToggleButton(label='FF')
        self.transport_fast_forward.connect("focus-in-event", self.focus_event,
                                            {'Widget': 2, 'Widget_Type': 'Transport'})
        self.transport_fast_forward.connect("pressed", self.transport_button_pressed_event,
                                            {'Widget': 'Transport', 'Button': 2})
        self.transport_fast_forward.connect("released", self.transport_button_released_event,
                                            {'Widget': 'Transport', 'Button': 2})

        self.transport_loop = Gtk.ToggleButton(label='LOOP')
        self.transport_loop.connect("focus-in-event", self.focus_event,
                                    {'Widget': 3, 'Widget_Type': 'Transport'})
        self.transport_loop.connect("pressed", self.transport_button_pressed_event,
                                    {'Widget': 'Transport', 'Button': 3})
        self.transport_loop.connect("released", self.transport_button_released_event,
                                    {'Widget': 'Transport', 'Button': 3})

        self.transport_stop = Gtk.ToggleButton(label='STOP')
        self.transport_stop.connect("focus-in-event", self.focus_event,
                                    {'Widget': 4, 'Widget_Type': 'Transport'})
        self.transport_stop.connect("pressed", self.transport_button_pressed_event,
                                    {'Widget': 'Transport', 'Button': 4})
        self.transport_stop.connect("released", self.transport_button_released_event,
                                    {'Widget': 'Transport', 'Button': 4})

        self.transport_record = Gtk.ToggleButton('REC')
        self.transport_record.connect("focus-in-event", self.focus_event,
                                      {'Widget': 5, 'Widget_Type': 'Transport'})
        self.transport_record.connect("pressed", self.transport_button_pressed_event,
                                      {'Widget': 'Transport', 'Button': 5})
        self.transport_record.connect("released", self.transport_button_released_event,
                                      {'Widget': 'Transport', 'Button': 5})

        self.scene_h_box = Gtk.HBox()
        self.scene_button = Gtk.Button('SCENE')
        self.scene_button.connect(
            "clicked", self.scene_cycle_event, {'Type': 'Cyclic', })
        self.scene_1_light = Gtk.RadioButton(
            group=None, label='1', use_underline=False)
        self.scene_1_light.set_name(name='Scene_1')
        self.scene_1_light.connect(
            "clicked", self.scene_change_event, {'Type': 'Direct', })
        self.scene_2_light = Gtk.RadioButton(
            group=self.scene_1_light, label='2', use_underline=False)
        self.scene_2_light.set_name(name='Scene_2')
        self.scene_2_light.connect(
            "clicked", self.scene_change_event, {'Type': 'Direct', })
        self.scene_3_light = Gtk.RadioButton(
            group=self.scene_1_light, label='3', use_underline=False)
        self.scene_3_light.set_name(name='Scene_3')
        self.scene_3_light.connect(
            "clicked", self.scene_change_event, {'Type': 'Direct', })
        self.scene_4_light = Gtk.RadioButton(
            group=self.scene_1_light, label='4', use_underline=False)
        self.scene_4_light.set_name(name='Scene_4')
        self.scene_4_light.connect(
            "clicked", self.scene_change_event, {'Type': 'Direct', })
        self.scene_h_box.pack_start(self.scene_button,
                                    expand=True, fill=True, padding=0)
        self.scene_h_box.pack_start(self.scene_1_light,
                                    expand=True, fill=True, padding=0)
        self.scene_h_box.pack_start(self.scene_2_light,
                                    expand=True, fill=True, padding=0)
        self.scene_h_box.pack_start(self.scene_3_light,
                                    expand=True, fill=True, padding=0)
        self.scene_h_box.pack_start(self.scene_4_light,
                                    expand=True, fill=True, padding=0)
        self.scene_button.show()
        self.scene_1_light.show()
        self.scene_2_light.show()
        self.scene_3_light.show()
        self.scene_4_light.show()
        self.scene_h_box.show()

        self.transport_table.attach(child=self.transport_rewind,
                                    left_attach=0,
                                    right_attach=1,
                                    top_attach=0,
                                    bottom_attach=1)
        self.transport_rewind.show()
        self.transport_table.attach(child=self.transport_play,
                                    left_attach=1,
                                    right_attach=2,
                                    top_attach=0,
                                    bottom_attach=1)
        self.transport_play.show()
        self.transport_table.attach(child=self.transport_fast_forward,
                                    left_attach=2,
                                    right_attach=3,
                                    top_attach=0,
                                    bottom_attach=1)
        self.transport_fast_forward.show()
        self.transport_table.attach(child=self.transport_loop,
                                    left_attach=0,
                                    right_attach=1,
                                    top_attach=1,
                                    bottom_attach=2)
        self.transport_loop.show()
        self.transport_table.attach(child=self.transport_stop,
                                    left_attach=1,
                                    right_attach=2,
                                    top_attach=1,
                                    bottom_attach=2)
        self.transport_stop.show()
        self.transport_table.attach(child=self.transport_record,
                                    left_attach=2,
                                    right_attach=3,
                                    top_attach=1,
                                    bottom_attach=2)
        self.transport_record.show()
        self.transport_table.attach(child=self.scene_h_box,
                                    left_attach=0,
                                    right_attach=3,
                                    top_attach=2,
                                    bottom_attach=3)
        self.transport_table.show()

        self.kontrol_blocks = []
        for i in range(9):
            block = KontrolBlock(index=i,
                                 fader_event=self.fader_event,
                                 focus_event=self.focus_event,
                                 button_pressed_event=self.button_pressed_event,
                                 button_released_event=self.button_released_event)
            self.kontrol_blocks.append(block)

        # # # # Common controls # # # #
        ###############################
        self.common_h_box = Gtk.HBox()
        self.transport_midi_channel_label = Gtk.Label.new(
            str='Transport MIDI Channel:')
        self.transport_midi_channel = Gtk.ComboBoxText()
        self.transport_midi_channel.connect("changed", self.combo_event,
                                            {'Widget': 'Transport_Midi_Channel', 'Widget_Type': 'Slider'})
        self.block_midi_channel_label = Gtk.Label(label='Block MIDI Channel:')
        self.block_midi_channel = Gtk.ComboBoxText()
        self.block_midi_channel.connect("changed", self.combo_event,
                                        {'Widget': 'Block_Midi_Channel', 'Widget_Type': 'Slider'})
        self.scene_name_label = Gtk.Label(label='Scene Name:')
        self.scene_name = Gtk.Entry()
        self.scene_name.connect("focus-out-event", self.entry_event,
                                {'Widget': 'Scene_Name', 'Widget_Type': 'Entry'})
        self.scene_midi_channel_label = Gtk.Label(label='Scene MIDI Channel:')
        self.scene_midi_channel = Gtk.ComboBoxText()

        for i in range(1, 17):
            channel = '{}'.format(i)
            self.transport_midi_channel.append_text(channel)
            self.block_midi_channel.append_text(channel)
            self.scene_midi_channel.append_text(channel)

        self.transport_midi_channel.append_text('Scene')
        self.block_midi_channel.append_text('Scene')

        self.scene_midi_channel.connect("changed", self.combo_event,
                                        {'Widget': 'Scene_Midi_Channel', 'Widget_Type': 'Slider'})

        self.common_h_box.pack_start(self.transport_midi_channel_label,
                                     expand=True, fill=True, padding=2)
        self.common_h_box.pack_start(self.transport_midi_channel,
                                     expand=True, fill=True, padding=2)
        self.common_h_box.pack_start(self.block_midi_channel_label,
                                     expand=True, fill=True, padding=2)
        self.common_h_box.pack_start(self.block_midi_channel,
                                     expand=True, fill=True, padding=2)
        self.common_h_box.pack_start(self.scene_name_label,
                                     expand=True, fill=True, padding=2)
        self.common_h_box.pack_start(self.scene_name,
                                     expand=True, fill=True, padding=2)
        self.common_h_box.pack_start(self.scene_midi_channel_label,
                                     expand=True, fill=True, padding=2)
        self.common_h_box.pack_start(self.scene_midi_channel,
                                     expand=True, fill=True, padding=2)
        self.transport_midi_channel_label.show()
        self.transport_midi_channel.show()
        self.block_midi_channel_label.show()
        self.block_midi_channel.show()
        self.scene_name_label.show()
        self.scene_name.show()
        self.scene_midi_channel_label.show()
        self.scene_midi_channel.show()
        self.common_h_box.show()

        # # # # Transport controls # # # #
        ##################################
        self.transport_control_table = Gtk.Table(rows=4, columns=4)
        self.transport_assign_type_label = Gtk.Label(label='Assign Type:')
        self.transport_assign_type = Gtk.ComboBoxText()
        self.transport_assign_type.append_text('No Assign')
        self.transport_assign_type.append_text('CC')
        self.transport_assign_type.append_text('MMC')
        self.transport_assign_type.connect("changed", self.combo_event,
                                           {'Widget': 'Assign_Type', 'Widget_Type': 'Transport'})
        self.transport_cc_label = Gtk.Label(label='CC Number:')
        adj = Gtk.Adjustment(value=0, lower=0, upper=127,
                             step_incr=1, page_incr=5, page_size=0)
        self.transport_cc = Gtk.SpinButton(
            adjustment=adj, climb_rate=0.0, digits=0)
        self.transport_cc.set_range(min=0, max=127)
        self.transport_cc.set_numeric(numeric=True)
        self.transport_cc.connect("value-changed", self.spin_event,
                                  {'Widget': 'CC', 'Widget_Type': 'Transport'})
        self.transport_mmc_command_label = Gtk.Label(label='MMC Command:')
        self.transport_mmc_command = Gtk.ComboBoxText()
        self.transport_mmc_command.append_text('Stop')
        self.transport_mmc_command.append_text('Play')
        self.transport_mmc_command.append_text('Deffered Play')
        self.transport_mmc_command.append_text('Fast Forward')
        self.transport_mmc_command.append_text('Rewind')
        self.transport_mmc_command.append_text('Record Strobe')
        self.transport_mmc_command.append_text('Record Exit')
        self.transport_mmc_command.append_text('Record Pause')
        self.transport_mmc_command.append_text('Pause')
        self.transport_mmc_command.append_text('Eject')
        self.transport_mmc_command.append_text('Chase')
        self.transport_mmc_command.append_text('Command Error Reset')
        self.transport_mmc_command.append_text('MMC Reset')
        self.transport_mmc_command.connect("changed", self.combo_event,
                                           {'Widget': 'MMC_Command', 'Widget_Type': 'Transport'})
        self.transport_mmc_dev_id_label = Gtk.Label(label='MMC Device ID:')
        adj = Gtk.Adjustment(value=0, lower=0, upper=127,
                             step_incr=1, page_incr=5, page_size=0)
        self.transport_mmc_dev_id = Gtk.SpinButton(
            adjustment=adj, climb_rate=0.0, digits=0)
        self.transport_mmc_dev_id.set_range(min=0, max=127)
        self.transport_mmc_dev_id.set_numeric(numeric=True)
        self.transport_mmc_dev_id.connect("value-changed", self.spin_event,
                                          {'Widget': 'MMC_Dev_ID', 'Widget_Type': 'Transport'})
        self.transport_switch_type_label = Gtk.Label(label='Switch Type:')
        self.transport_switch_type = Gtk.ComboBoxText()
        self.transport_switch_type.append_text('Momentary')
        self.transport_switch_type.append_text('Toggle')
        self.transport_switch_type.connect("changed", self.combo_event,
                                           {'Widget': 'Switch_Type', 'Widget_Type': 'Transport'})

        self.transport_control_table.attach(child=self.transport_assign_type_label,
                                            left_attach=0,
                                            right_attach=1,
                                            top_attach=0,
                                            bottom_attach=1)
        self.transport_assign_type_label.show()
        self.transport_control_table.attach(child=self.transport_assign_type,
                                            left_attach=1,
                                            right_attach=2,
                                            top_attach=0,
                                            bottom_attach=1)
        self.transport_assign_type.show()
        self.transport_control_table.attach(child=self.transport_cc_label,
                                            left_attach=0,
                                            right_attach=1,
                                            top_attach=1,
                                            bottom_attach=2)
        self.transport_cc_label.show()
        self.transport_control_table.attach(child=self.transport_cc,
                                            left_attach=1,
                                            right_attach=2,
                                            top_attach=1,
                                            bottom_attach=2)
        self.transport_cc.show()
        self.transport_control_table.attach(child=self.transport_mmc_command_label,
                                            left_attach=0,
                                            right_attach=1,
                                            top_attach=2,
                                            bottom_attach=3)
        self.transport_mmc_command_label.show()
        self.transport_control_table.attach(child=self.transport_mmc_command,
                                            left_attach=1,
                                            right_attach=2,
                                            top_attach=2,
                                            bottom_attach=3)
        self.transport_mmc_command.show()
        self.transport_control_table.attach(child=self.transport_mmc_dev_id_label,
                                            left_attach=0,
                                            right_attach=1,
                                            top_attach=3,
                                            bottom_attach=4)
        self.transport_mmc_dev_id_label.show()
        self.transport_control_table.attach(child=self.transport_mmc_dev_id,
                                            left_attach=1,
                                            right_attach=2,
                                            top_attach=3,
                                            bottom_attach=4)
        self.transport_mmc_dev_id.show()
        self.transport_control_table.attach(child=self.transport_switch_type_label,
                                            left_attach=2,
                                            right_attach=3,
                                            top_attach=0,
                                            bottom_attach=1)
        self.transport_switch_type_label.show()
        self.transport_control_table.attach(child=self.transport_switch_type,
                                            left_attach=3,
                                            right_attach=4,
                                            top_attach=0,
                                            bottom_attach=1)
        self.transport_switch_type.show()

        # # # # Slider and Knob controls # # # #
        ########################################
        self.slider_knob_control_table = Gtk.Table(rows=4, columns=2)
        self.slider_assign_type_label = Gtk.Label(label='Assign type:')
        self.slider_assign_type = Gtk.ComboBoxText()
        self.slider_assign_type.append_text('No Assign')
        self.slider_assign_type.append_text('CC')
        self.slider_assign_type.connect("changed", self.combo_event,
                                        {'Widget': 'Assign_Type', 'Widget_Type': 'Slider'})
        self.slider_cc_label = Gtk.Label(label='CC number:')
        adj = Gtk.Adjustment(value=0, lower=0, upper=127,
                             step_incr=1, page_incr=5, page_size=0)
        self.slider_cc = Gtk.SpinButton(
            adjustment=adj, climb_rate=0.0, digits=0)
        self.slider_cc.set_range(min=0, max=127)
        self.slider_cc.set_numeric(numeric=True)
        self.slider_cc.connect("value-changed", self.spin_event,
                               {'Widget': 'CC', 'Widget_Type': 'Slider'})
        self.slider_min_value_label = Gtk.Label(label='Min value:')
        adj = Gtk.Adjustment(value=0, lower=0, upper=127,
                             step_incr=1, page_incr=5, page_size=0)
        self.slider_min_value = Gtk.SpinButton(
            adjustment=adj, climb_rate=0.0, digits=0)
        self.slider_min_value.set_range(min=0, max=127)
        self.slider_min_value.set_numeric(numeric=True)
        self.slider_min_value.connect("value-changed", self.spin_event,
                                      {'Widget': 'Min_Value', 'Widget_Type': 'Slider'})
        self.slider_max_value_label = Gtk.Label(label='Max value:')
        adj = Gtk.Adjustment(value=0, lower=0, upper=127,
                             step_incr=1, page_incr=5, page_size=0)
        self.slider_max_value = Gtk.SpinButton(
            adjustment=adj, climb_rate=0.0, digits=0)
        self.slider_max_value.set_range(min=0, max=127)
        self.slider_max_value.set_numeric(numeric=True)
        self.slider_max_value.connect("value-changed", self.spin_event,
                                      {'Widget': 'Max_Value', 'Widget_Type': 'Slider'})

        self.slider_knob_control_table.attach(child=self.slider_assign_type_label,
                                              left_attach=0,
                                              right_attach=1,
                                              top_attach=0,
                                              bottom_attach=1)
        self.slider_assign_type_label.show()
        self.slider_knob_control_table.attach(child=self.slider_assign_type,
                                              left_attach=1,
                                              right_attach=2,
                                              top_attach=0,
                                              bottom_attach=1)
        self.slider_assign_type.show()
        self.slider_knob_control_table.attach(child=self.slider_cc_label,
                                              left_attach=0,
                                              right_attach=1,
                                              top_attach=1,
                                              bottom_attach=2)
        self.slider_cc_label.show()
        self.slider_knob_control_table.attach(child=self.slider_cc,
                                              left_attach=1,
                                              right_attach=2,
                                              top_attach=1,
                                              bottom_attach=2)
        self.slider_cc.show()
        self.slider_knob_control_table.attach(child=self.slider_min_value_label,
                                              left_attach=0,
                                              right_attach=1,
                                              top_attach=2,
                                              bottom_attach=3)
        self.slider_min_value_label.show()
        self.slider_knob_control_table.attach(child=self.slider_min_value,
                                              left_attach=1,
                                              right_attach=2,
                                              top_attach=2,
                                              bottom_attach=3)
        self.slider_min_value.show()
        self.slider_knob_control_table.attach(child=self.slider_max_value_label,
                                              left_attach=0,
                                              right_attach=1,
                                              top_attach=3,
                                              bottom_attach=4)
        self.slider_max_value_label.show()
        self.slider_knob_control_table.attach(child=self.slider_max_value,
                                              left_attach=1,
                                              right_attach=2,
                                              top_attach=3,
                                              bottom_attach=4)
        self.slider_max_value.show()

        # # # # Button controls # # # #
        ###############################
        self.button_control_table = Gtk.Table(rows=4, columns=4)
        self.button_assign_type_label = Gtk.Label(label='Assign type:')
        self.button_assign_type = Gtk.ComboBoxText()
        self.button_assign_type.append_text('No Assign')
        self.button_assign_type.append_text('CC')
        self.button_assign_type.append_text('Note')
        self.button_assign_type.connect("changed", self.combo_event,
                                        {'Widget': 'Assign_Type', 'Widget_Type': 'Button'})
        self.button_cc_label = Gtk.Label(label='CC/Note number:')
        adj = Gtk.Adjustment(value=0, lower=0, upper=127,
                             step_incr=1, page_incr=5, page_size=0)
        self.button_cc = Gtk.SpinButton(
            adjustment=adj, climb_rate=0.0, digits=0)
        self.button_cc.set_range(min=0, max=127)
        self.button_cc.connect("value-changed", self.spin_event,
                               {'Widget': 'CC', 'Widget_Type': 'Button'})
        self.button_off_value_label = Gtk.Label(label='Off value:')
        adj = Gtk.Adjustment(value=0, lower=0, upper=127,
                             step_incr=1, page_incr=5, page_size=0)
        self.button_off_value = Gtk.SpinButton(
            adjustment=adj, climb_rate=0.0, digits=0)
        self.button_off_value.set_range(min=0, max=127)
        self.button_off_value.connect("value-changed", self.spin_event,
                                      {'Widget': 'Off_Value', 'Widget_Type': 'Button'})
        self.button_on_value_label = Gtk.Label(label='On value:')
        adj = Gtk.Adjustment(value=0, lower=0, upper=127,
                             step_incr=1, page_incr=5, page_size=0)
        self.button_on_value = Gtk.SpinButton(
            adjustment=adj, climb_rate=0.0, digits=0)
        self.button_on_value.set_range(min=0, max=127)
        self.button_on_value.connect("value-changed", self.spin_event,
                                     {'Widget': 'On_Value', 'Widget_Type': 'Button'})
        self.button_attack_time_label = Gtk.Label(label='Attack time:')
        adj = Gtk.Adjustment(value=0, lower=0, upper=127,
                             step_incr=1, page_incr=5, page_size=0)
        self.button_attack_time = Gtk.SpinButton(
            adjustment=adj, climb_rate=0.0, digits=0)
        self.button_attack_time.set_range(min=0, max=127)
        self.button_attack_time.connect("value-changed", self.spin_event,
                                        {'Widget': 'Attack_Time', 'Widget_Type': 'Button'})
        self.button_release_time_label = Gtk.Label(label='Release time:')
        adj = Gtk.Adjustment(value=0, lower=0, upper=127,
                             step_incr=1, page_incr=5, page_size=0)
        self.button_release_time = Gtk.SpinButton(
            adjustment=adj, climb_rate=0.0, digits=0)
        self.button_release_time.set_range(min=0, max=127)
        self.button_release_time.connect("value-changed", self.spin_event,
                                         {'Widget': 'Release_Time', 'Widget_Type': 'Button'})
        self.button_switch_type_label = Gtk.Label(label='Switch type:')
        self.button_switch_type = Gtk.ComboBoxText()
        self.button_switch_type.append_text('Momentary')
        self.button_switch_type.append_text('Toggle')
        self.button_switch_type.connect("changed", self.combo_event,
                                        {'Widget': 'Switch_Type', 'Widget_Type': 'Button'})

        self.button_control_table.attach(child=self.button_assign_type_label,
                                         left_attach=0,
                                         right_attach=1,
                                         top_attach=0,
                                         bottom_attach=1)
        self.button_assign_type_label.show()
        self.button_control_table.attach(child=self.button_assign_type,
                                         left_attach=1,
                                         right_attach=2,
                                         top_attach=0,
                                         bottom_attach=1)
        self.button_assign_type.show()
        self.button_control_table.attach(child=self.button_cc_label,
                                         left_attach=0,
                                         right_attach=1,
                                         top_attach=1,
                                         bottom_attach=2)
        self.button_cc_label.show()
        self.button_control_table.attach(child=self.button_cc,
                                         left_attach=1,
                                         right_attach=2,
                                         top_attach=1,
                                         bottom_attach=2)
        self.button_cc.show()
        self.button_control_table.attach(child=self.button_off_value_label,
                                         left_attach=0,
                                         right_attach=1,
                                         top_attach=2,
                                         bottom_attach=3)
        self.button_off_value_label.show()
        self.button_control_table.attach(child=self.button_off_value,
                                         left_attach=1,
                                         right_attach=2,
                                         top_attach=2,
                                         bottom_attach=3)
        self.button_off_value.show()
        self.button_control_table.attach(child=self.button_on_value_label,
                                         left_attach=0,
                                         right_attach=1,
                                         top_attach=3,
                                         bottom_attach=4)
        self.button_on_value_label.show()
        self.button_control_table.attach(child=self.button_on_value,
                                         left_attach=1,
                                         right_attach=2,
                                         top_attach=3,
                                         bottom_attach=4)
        self.button_on_value.show()
        self.button_control_table.attach(child=self.button_attack_time_label,
                                         left_attach=2,
                                         right_attach=3,
                                         top_attach=0,
                                         bottom_attach=1)
        self.button_attack_time_label.show()
        self.button_control_table.attach(child=self.button_attack_time,
                                         left_attach=3,
                                         right_attach=4,
                                         top_attach=0,
                                         bottom_attach=1)
        self.button_attack_time.show()
        self.button_control_table.attach(child=self.button_release_time_label,
                                         left_attach=2,
                                         right_attach=3,
                                         top_attach=1,
                                         bottom_attach=2)
        self.button_release_time_label.show()
        self.button_control_table.attach(child=self.button_release_time,
                                         left_attach=3,
                                         right_attach=4,
                                         top_attach=1,
                                         bottom_attach=2)
        self.button_release_time.show()
        self.button_control_table.attach(child=self.button_switch_type_label,
                                         left_attach=2,
                                         right_attach=3,
                                         top_attach=2,
                                         bottom_attach=3)
        self.button_switch_type_label.show()
        self.button_control_table.attach(child=self.button_switch_type,
                                         left_attach=3,
                                         right_attach=4,
                                         top_attach=2,
                                         bottom_attach=3)
        self.button_switch_type.show()

        self.status_bar = Gtk.Statusbar()
        self.status_bar.show()
        self.status_bar_context_id = self.status_bar.get_context_id('Message')
        self.status_bar.push(self.status_bar_context_id, 'Status Bar')

        self.h_box_level_1.pack_start(self.transport_table,
                                      expand=True, fill=True, padding=2)
        for block in self.kontrol_blocks:
            self.h_box_level_1.pack_start(
                block.table, expand=True, fill=True, padding=2)

        self.h_box_level_1.show()
        self.h_box_level_1.set_size_request(width=-1, height=-1)
        # self.Slider_Knob_Control_Table.set_size_request(width=-1, height=150)
        self.v_box_top.pack_start(self.h_box_level_1,
                                  expand=True, fill=True, padding=2)
        self.v_box_top.pack_start(self.common_h_box,
                                  expand=False, fill=False, padding=2)
        self.v_box_top.pack_start(self.slider_knob_control_table,
                                  expand=False, fill=False, padding=4)
        self.v_box_top.pack_start(self.button_control_table,
                                  expand=False, fill=False, padding=3)
        self.v_box_top.pack_start(self.transport_control_table,
                                  expand=False, fill=False, padding=3)
        self.v_box_top.pack_start(self.status_bar,
                                  expand=False, fill=False, padding=2)
        self.v_box_top.show()

        self.window.add(self.v_box_top)
        self.window.show()

        self.scene_1_light.clicked()

    def main(self):
        Gtk.main()
