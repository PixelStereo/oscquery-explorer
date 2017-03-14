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
my_device.add_param('test/value/int', datatype='int')
my_device.add_param('test/value/float', datatype='float')
my_device.add_param('test/value/bool', datatype='bool')
my_device.add_param('test/value/string', datatype='string')
