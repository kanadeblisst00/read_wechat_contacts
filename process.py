from ctypes import *
from ctypes.wintypes import *
from winapi import *


class Process:
    def __init__(self, pid):
        self._pid = pid
        self._handle = OpenProcess(0x1F0FFF, False, self._pid)
        if not self._handle:
            raise Exception(f"获取微信进程句柄失败, 可能原因：pid不存在")
        
    def readMemoryAddr(self, addr, buffer, len=1):
        if not ReadProcessMemory(self._handle, addr, buffer, len, None):
            err = get_last_error()
            raise Exception(f"读取进程地址失败, 错误代码: {err}")
        
    def readString(self, addr, len=1, decode=True):
        buffer = create_string_buffer(len+10)
        self.readMemoryAddr(addr, buffer, len)
        value = buffer.value.decode() if decode else buffer.value
        return value
    
    def readStringUtf16(self, addr, len=1):
        buffer = create_unicode_buffer(len+10)
        self.readMemoryAddr(addr, buffer, len*2)
        return buffer.value

    def readWstring(self, addr):
        len = self.read4ByteNumber(addr + 0x8)
        if not len:
            return None
        pointer = self.read8ByteNumber(addr)
        return self.readStringUtf16(pointer, len)
    
    def read8ByteNumber(self, addr, len=8):
        buffer = c_int64()
        self.readMemoryAddr(addr, byref(buffer), len)
        return buffer.value

    def read4ByteNumber(self, addr, len=4):
        buffer = c_int32()
        self.readMemoryAddr(addr, byref(buffer), len)
        return buffer.value
    
    def readBytes(self, addr, len=1):
        buffer = create_string_buffer(len+10)
        self.readMemoryAddr(addr, buffer, len)
        return buffer.raw[:len]

    def getModuleBaseAddress(self, moduleName):
        return getModuleBaseAddress(moduleName, self._pid)
