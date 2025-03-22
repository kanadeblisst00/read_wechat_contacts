import ctypes
from ctypes import wintypes
from winapi import *
from process import Process

sys_info = SYSTEM_INFO()
GetSystemInfo(ctypes.byref(sys_info))

def read_contact(prcs:Process, head_pointer):
    wxid = prcs.readWstring(head_pointer + 0x18)
    wxh = prcs.readWstring(head_pointer + 0x38)
    nickname = prcs.readWstring(head_pointer + 0xA8)
    print(wxid, wxh, nickname)

def scan_and_match_value(prcs:Process, value, max_result_len=1000, match_func=None):
    result = []
    min_addr = ctypes.cast(sys_info.lpMinimumApplicationAddress, ctypes.c_void_p).value
    max_addr = ctypes.cast(sys_info.lpMaximumApplicationAddress, ctypes.c_void_p).value

    current_addr = min_addr

    while current_addr < max_addr:
        mem_info = MEMORY_BASIC_INFORMATION()
        VirtualQueryEx(prcs._handle, ctypes.cast(current_addr, wintypes.LPVOID), 
                                                ctypes.byref(mem_info), ctypes.sizeof(MEMORY_BASIC_INFORMATION))
        region_size = mem_info.RegionSize
        if region_size <= 0:
            break
        
        if mem_info.Type & MEM_PRIVATE and \
            mem_info.State & MEM_COMMIT and \
            mem_info.Protect == PAGE_READWRITE and \
            mem_info.AllocationProtect == PAGE_READWRITE:
            for i in range(0, region_size, 8):
                _addr = current_addr + i
                _value = prcs.read8ByteNumber(_addr)
                if _value == value:
                    if match_func and match_func(_addr): # 匹配函数
                        return _addr
                    print(f"找到匹配值, 地址：0x{_addr:x}")
                    result.append(_addr)
        if len(result) >= max_result_len:  
            break
        current_addr += region_size

    CloseHandle(prcs._handle)
    
    return result

