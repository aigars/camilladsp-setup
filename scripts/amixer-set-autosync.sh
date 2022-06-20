#!/bin/bash

sleep 5

amixer -c0 cset iface=MIXER,name='Preferred Sync Reference' 0
amixer -c1 cset iface=MIXER,name='Preferred Sync Reference' 9
amixer -c2 cset iface=MIXER,name='Preferred Sync Reference' 9

amixer -c0 cset iface=MIXER,name='System Clock Mode' 0
amixer -c1 cset iface=MIXER,name='System Clock Mode' 1
amixer -c2 cset iface=MIXER,name='System Clock Mode' 1
