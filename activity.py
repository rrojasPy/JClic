#!/usr/bin/env python

# Copyright (C) 2009, Simon Schampijer
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import sys, os, platform

from gi.repository import Gtk
from gi.repository import Vte
from gi.repository import GLib

from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityButton
from sugar3.activity.widgets import TitleEntry
from sugar3.activity.widgets import StopButton

class JclicActivity(activity.Activity):
    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

        self.max_participants = 1

        toolbar_box = ToolbarBox()

        activity_button = ActivityButton(self)
        toolbar_box.toolbar.insert(activity_button, 0)
        activity_button.show()

        title_entry = TitleEntry(self)
        toolbar_box.toolbar.insert(title_entry, -1)
        title_entry.show()
        
        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()
        
        vt = Vte.Terminal()
        vt.connect("child-exited", self.exit)
        vt.spawn_sync(Vte.PtyFlags.DEFAULT, os.environ["HOME"],
            ["/bin/bash"], [], GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None, None)
        if not os.path.exists(os.environ["SUGAR_ACTIVITIES_PATH"]+"/Java.activity"):
            label = Gtk.Label("Please install Java activity")
            self.set_canvas(label)
            label.show()
            return
        self.set_canvas(vt)
        vt.show()

        vt.feed_child("cd $SUGAR_BUNDLE_PATH\n", -1)
        if platform.machine().startswith('arm'):
                vt.feed_child("export JAVA_HOME=$SUGAR_ACTIVITIES_PATH/Java.activity/jre_arm\n", -1)
        else:
            if platform.architecture()[0] == '64bit':
                vt.feed_child("export JAVA_HOME=$SUGAR_ACTIVITIES_PATH/Java.activity/jre_64\n", -1)
            else:
                vt.feed_child("export JAVA_HOME=$SUGAR_ACTIVITIES_PATH/Java.activity/jre_32\n", -1)
        vt.feed_child("export PATH=$JAVA_HOME/bin:$PATH\n", -1)
        vt.feed_child("java -jar jclic.jar; exit\n", -1)

    def exit(self, vt, data):
        self.close()

