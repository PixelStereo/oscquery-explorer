#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

# append ossia_python.so and pyossia module paths
# we will use pip later on
import sys, os
sys.path.append(os.path.abspath('../../libossia/build/'))
sys.path.append(os.path.abspath('../../libossia/OSSIA/ossia-python/'))

from pyossia import *

# create the OSSIA Device with the name provided
# here for test purpose
my_device = ossia.LocalDevice('PyOssia Device')
my_device.expose(protocol='oscquery', udp_port=3456, ws_port=5678)
my_int = my_device.add_param('test/value/int', datatype='int')
my_float = my_device.add_param('test/value/float', datatype='float')
my_bool = my_device.add_param('test/value/bool', datatype='bool')
my_string = my_device.add_param('test/value/string', datatype='string')
my_string.push_value(ossia.Value(" Supa String !!"))
my_bool.push_value(ossia.Value(True))
my_float.push_value(ossia.Value(2.22))
my_int.push_value(ossia.Value(222))
while True:
	pass