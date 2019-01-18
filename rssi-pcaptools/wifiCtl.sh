#!/bin/bash

[ "0" != "$UID" ] && ( echo "Must run as root!" ) && exit
/etc/dbus-1/event.d/25NetworkManager $@
/etc/dbus-1/event.d/26NetworkManagerDispatcher $@
