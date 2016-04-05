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
import threading
import queue
from Debug import pyDebugger
from serial import (FIVEBITS,SIXBITS,SEVENBITS,EIGHTBITS, PARITY_NONE, PARITY_EVEN,PARITY_ODD,
    PARITY_MARK,PARITY_SPACE,STOPBITS_ONE,STOPBITS_ONE_POINT_FIVE,STOPBITS_TWO)


_ISVALID = 1
_NOTVALID = 0
_UNTESTED = -1
_OPEN = 1
_CLOSED = 0
_ALREADYOPENED = 2

class pySerialPort:

    def __init__(self,p=None,pf="/dev/ttyAMA0",pb=9600,pp=PARITY_NONE,pbs=EIGHTBITS,
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
            self.Debugger.Log("...Success!",PrintName=False)
        else:
            try:
                self.Port = serial.Serial(None,pb,pbs,pp,psb,pt,pfc,phs,pt,phs)
                self.isValid = _ISVALID    
                self.Debugger.Log("...Success!",PrintName=False)
            except e as Exception:
                self.Debugger.Log("...Failed!",PrintName=False)
                self.Debugger.Log(str(e))
                self.isValid = _NOTVALID 
            
            
    def Close(self):
        self.Debugger.Log("Attempting to close port " + self.PortFile + "...", endd='')
        if self.Port == None:
            self.Debugger.Log("...Warning! Nothing to close, port is null...reporting True",PrintName=False)
            #count as true cause nothing to close!
            return True
        else:
            try:
                self.Port.close()
                self.Debugger.Log("...Port successfully closed",PrintName=False)
                #count as true cause nothing to close!
                return True
            except e as Exception:
                self.Debugger.Log("...Failed!",PrintName=False)
                self.Debugger.Log(str(e))
                return False
            

    # a quick way to get settings loaded into the class
    def LoadSettings(self,dDict, IgnoreError=False):
        self.Debugger.Log("Attempting to load settings...")
        for pK in dDict:
            if pK in self.__dict__:
                if isinstance(dDict[pK],bool):
                    if dDict[pK] == True:
                        spV = "True"
                    else:
                        spV = "False"
                else:
                    spV = str(dDict[pK])
                if isinstance(self.__dict__[pK],bool):
                    if self.__dict__[pK] == True:
                        sOpV = "True"
                    else:
                        sOpV = "False"
                else:
                    sO13pV = str(self.__dict__[pK])
                
                
                self.Debugger.Log("Updating key '" + pK + "' with value '" + spV +
                    "', old value was '" + sOpV + "'")
                self.__dict__[pK] = dDict[pK]
            else:
                #Somethings's Fucked up, Error
                self.Debugger.Log("Error! Trying to update key '" + str(pK) + 
                    "' but it doesn't exist in class!\n***Possible Hack Attack!!!!!")
     
    
    
    def Open(self):
        self.Debugger.Log("Attempting to open port " + self.PortFile + "...", endd='')
       
        if self.Port == None:
            try:
                self.Port = serial.Serial(self.PortFile,self.PortBaud,self.PortBytes,
                self.PortStopBits,self.PortParity,self.PortStopBits,self.PortTimeout,
                self.PortFlowControl,self.PortHandShake,self.PortTimeout,self.PortHandShake)
                self.isValid = _ISVALID
                self.Debugger.Log("...Success!",PrintName=False)
                return _OPEN 
            except e as Exception:
                self.Debugger.Log("...Failed!",PrintName=False)
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
                        self.Debugger.Log("...Success!")
                        return _OPEN 
                    except s as Exception:
                        self.Debugger.Log("...Failed!")
                        self.Debugger.Log(str(e))
                        self.isValid = _NOTVALID
                        return _CLOSED
                        
            except e as Exception:
                self.Debugger.Log("...Failed!")
                self.Debugger.Log(str(e))
                self.isValid = _NOTVALID
                return _CLOSED
            return _ALREADYOPENED
        

    def Read(self,bs=1,bBlocking=True,pParent=None):
        sTmp = None
        if bBlocking == False:
            self.Debugger.Log("Attempting to read '" + str(bs) + "' bytes from port '" + 
                self.PortFile + "' while not blocking...")
            threading.Thread(target=_ReadNB, args=(self,bs,pParent)).start()
        else:
            self.Debugger.Log("Attempting to read '" + str(bs) + "' bytes from port '" + 
                self.PortFile + "'...")
            try:
                sTmp = self.Port.read(bs)
                self.Debugger.Log("Read " + str(bs) + " byte: " + str(sTmp))
                return sTmp
            except e as Exception:
                self.Debugger.Log("Error: " + str(e))
                return None
                
            
            
            
            
    def _ReadNB(self,bBytes=1,cParent=None):
        if tParent == None:
            self.Debugger.Log ("Can't read non blocking because parent is 'None'")
            return
            
        self.Debugger.Log("Attempting to read '" + str(bs) + "' bytes from port '" + self.PortFile +
            "' in new thread...")
        try:
            sTmp = self.Port.read(bs)
            self.Debugger.Log("Read " + str(bs) + " byte: " + str(sTmp))
            cParent.ReadData = sTmp
        except e as Exception:
            self.Debugger.Log("Error: " + str(e))
            cParent.ReadData = None
        
        #Add our call back to our main queue
        cParent.ReadCallBack()
        
        
    def ReadLine(self,bBlocking=True,pParent=None):
        if bBlocking == False:
            self.Debugger.Log("Attempting to read line from port '" + self.PortFile + 
                "' while not blocking...")
            threading.Thread(target=_ReadLineNB, args=(self,pParent)).start()
        else:
            self.Debugger.Log("Attempting to read from port '" + self.PortFile + "'...")
            try:
                sTmp = self.Port.readline()
                self.Debugger.Log("Read: " + str(sTmp))
                return sTmp
            except e as Exception:
                self.Debugger.Log("Error: " + str(e))
                return None
                
            
            
            
            
    def _ReadLineNB(self,tParent=None):
        if tParent == None:
            self.Debugger.Log ("Can't read non blocking because parent is 'None'")
            return
        self.Debugger.Log("Attempting to read from port '" + self.PortFile + "' in new thread...")
        try:
            sTmp = self.Port.readline()
        except e as Exception:
            self.Debugger.Log("Error: " + str(e))
            tParent.ReadData = None
            
        self.Debugger.Log("Read: " + str(sTmp))
        tParent.ReadData = sTmp
        
        #Add our call back to our main queue
        tParent.ReadCallBack()
        
    def Write(self,sData, bBlocking=True,pParent=None):
        if bBlocking == False:
            self.Debugger.Log("Attempting to write to port '" + self.PortFile + 
                "' while not blocking...")
            threading.Thread(target=_WriteNB, args=(self,sData,pParent)).start()
        else:
            self.Debugger.Log("Attempting to write to port '" + self.PortFile + "'...")
            try:
                sTmp = self.Port.write(sData)
            except e as Exception:
                self.Debugger.Log("Error: " + str(e))
                return None
                
            self.Debugger.Log("Wrote '" + str(sTmp) + "' bytes")
            return sTmp
            
            
            
    def _WriteNB(self,_sData,tParent=None):
        if tParent == None:
            self.Debugger.Log ("Can't write non blocking because parent is 'None'")
            return
        self.Debugger.Log("Attempting to write to port '" + self.PortFile + "' in new thread...")
        try:
            sTmp = self.Port.write(_sData)
        except e as Exception:
            self.Debugger.Log("Error: " + str(e))
            tParent.ReadData = None
            
        self.Debugger.Log("Wrote '" + str(sTmp) + "' bytes")
        tParent.WriteData = sTmp
        
        #Add our call back to our main queue
        tParent.WriteCallBack()
        
        
        
