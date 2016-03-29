#! /usr/bin/env python3
#############################################################
# Title: Python Serial Wrapper Class                        #
# Description: Wrapper around Serial communications for     #
#              easy integration in projects                 #
# Version:                                                  #
#   * Version 1.0 03/29/2016 RC                             #
#                                                           #
# Author: Richard Cintorino (c) Richard Cintorino 2016      #
#############################################################

import serial
from Debug import pyDebugger

class pySerialPort:

    #to keep all our serial info clean
    spInfo = SerialPortHandler

    def __init__(self):
        #Set debugging options here!
        self.Debugger = pyDebugger(self,True,False)
        
        self.Debugger.Log("Initializing Serial Port...", endd = "")
        self.spInfo.Port = serial.Serial(self.spInfo.PortFile,)
        
        self.Debugger.Log("Starting Serial Port...")


class SerialPortHandler():

    def __init__(self,p=None,pf="/dev/ttyAMA0",pb=9600,pp=serial.PARITY_NONE,pbs=serial.EIGHTBITS,
                    psb=serial.STOPBITS_ONE,pt=5,pfc=False,phs=False):
        #Variables 
        self.Port = p
        self.PortFile = pf
        self.PortBaud = pb
        self.PortParity = pp
        self.PortBytes = pbs
        self.PortStopBits = psb
        self.PortTimeout = pt
        self.PortFlowControl = pfc
        self.PortHandshake = phs

    # a quick way to get settings loaded into the class
    def LoadSettings():
    
