#! /usr/bin/env python3
# -*- coding: utf-8 -*-

class ZeroConfListener(object):

    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        print("Service %s added, service info: %s" % (name, info))
        print(info.properties['Description'])
        print(info.properties['LocalPort'])