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
import queue
from Debug import pyDebugger

_ISVALID = 1
_NOTVALID = 0
_UNTESTED = -1
_OPEN = 1
_CLOSED = 0
_ALREADYOPENED = 2

class pySerialPort:

    def __init__(self,p=None,pf="/dev/ttyAMA0",pb=9600,pp=serial.PARITY_NONE,pbs=serial.EIGHTBITS,
                    psb=serial.STOPBITS_ONE,pt=5,pfc=False,phs=False,Debug=True,LogToFile=False):
        #Set debugging options here!
        self.Debugger = pyDebugger(self,True,False)
        self.Debugger.Log("Initializing Serial Port...", endd = "")
        try:
            self.spH = SerialPortHandler(p,pf,pb,pp,pbs,psb,pt,pfc,phs,Debug,LogToFile)
            self.Debugger.Log("...Success!")
        except e as Exception:
            self.Debugger.Log("...Failed!\n" + str(e))



class SerialPortHandler():

    def __init__(self,p=None,pf="/dev/ttyAMA0",pb=9600,pp=serial.PARITY_NONE,pbs=serial.EIGHTBITS,
                    psb=serial.STOPBITS_ONE,pt=None,pfc=False,phs=False,Debug=True,LogToFile=False,
                    AutoConnect=False):
        self.isValid = _UNTESTED
        self.Debugger = pyDebugger(self,Debug,LogToFile)
        self.Debugger.Log("Initializing Handler...", endd = "")
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
        
        #check if our port is already there
        if p == None and AutoConnect == True:
            self.Port = serial.Serial(pf,pb,pbs,pp,psb,pt,pfc,phs,pt,phs)
            self.Port.port = pf
            self.isValid = _UNTESTED
            self.Debugger.Log("...Success!)
        else:
            try:
                self.Port = serial.Serial(None,pb,pbs,pp,psb,pt,pfc,phs,pt,phs)
                self.isValid = _ISVALID    
                self.Debugger.Log("...Success!)
            except e as serial.SerialException:
                self.Debugger.Log("...Failed!)
                self.Debugger.Log(str(e))
                self.isValid = _NOTVALID 
            
            
    def Close(self):
        try:
            self.Debugger.Log("Attempting to close port " + self.PortFile + "...", endd='')
            if self.Port == None:
                self.Debugger.Log("...Warning! Nothing to close, port is null...reporting True")
                #count as true cause nothing to close!
                return True
            else:
                try:
                    self.Port.close()
                    self.Debugger.Log("...Port successfully closed")
                    #count as true cause nothing to close!
                    return True
                except e as serial.SerialException:
                    self.Debugger.Log("...Failed!")
                    self.Debugger.Log(str(e))
                    return False
                    
            
    # a quick way to get settings loaded into the class
    def LoadSettings(self,dDict):
        self.Debugger.Log("Attempting to load settings...")
        for pK,pV in enumerate(dDict):
            if pK in self.__dict__:
                self.Debugger.Log("Updating key '" + pK + "' with value '" + pV +
                    "', old value was '" + self.__dict__[pK] + "'")
                self.__dict__[pK] = pV
            else:
                #Somethings's Fucked up, Error
                self.Debugger.Log("Error! Trying to update key '" + pK + 
                    "' but it doesn't exist in class!\n***Possible Hack Attack!!!!!")
     
    
    
    def Open(self):
        self.Debugger.Log("Attempting to open port " + self.PortFile + "...", endd='')
       
        if self.Port == None:
            try:
                self.Port = serial.Serial(self.PortFile,self.PortBaud,self.PortBytes,
                self.PortStopBits,self.PortParity,self.PortStopBits,self.PortTimeout,
                self.PortFlowControl,self.PortHandShake,self.PortTimeout,self.PortHandShake)
                self.isValid = _ISVALID
                self.Debugger.Log("...Success!)
                return _OPEN 
            except e as serial.SerialException:
                self.Debugger.Log("...Failed!)
                self.Debugger.Log(str(e))
                self.isValid = _NOTVALID
                return _CLOSED
        else:
            try:
                if self.Port.isOpen() == True:
                    self.Debugger.Log("...Warning! Port already opened")
                    self.isValid = _ISVALID
                    return _ALREADYOPENED
                else:
                    try:
                        self.Port.open()
                        self.isValid = _ISVALID
                        self.Debugger.Log("...Success!)
                        return _OPEN 
                    except s as serial.SerialException:
                        self.Debugger.Log("...Failed!)
                        self.Debugger.Log(str(e))
                        self.isValid = _NOTVALID
                        return _CLOSED
                        
            except e as Exception:
                self.Debugger.Log("...Failed!)
                self.Debugger.Log(str(e))
                self.isValid = _NOTVALID
                return _CLOSED
            return _ALREADYOPENED
        else:
        

    def Read(self,bs=1,bBlocking=True,pParent=None):
        if bBlocking == False:
            self.Debugger.Log("Attempting to read line from port '" + self.PortFile + "' while not blocking...")
        else:
            self.Debugger.Log("Attempting to read from port '" + self.PortFile + "'...", endd="")
            sTmp = self.Port.read(bs)
            self.Debugger.Log("Read " + str(bs) + " byte: " + str(sTmp)
            return sTmp
            
            
            
        
        
        
        
        
        
        
