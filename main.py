from scan_memory import scan_and_match_value
from process import Process
from read_contact_3 import Contacts


pid = 41316  
prcs = Process(pid)
wechat_win = prcs.getModuleBaseAddress('WeChatWin.dll')
value_to_search = wechat_win + 0x4F70A98  # 要查找的值

def match_func1(addr):
    _wxid = prcs.readWstring(addr + 0x18)
    if "wxid_" in _wxid:
        return True

contact_head = scan_and_match_value(prcs, value_to_search, match_func=match_func1)
print(hex(contact_head))

wxid = prcs.readWstring(contact_head + 0x18)
def match_func2(addr):
    _wxid = prcs.readWstring(addr - 0x20)
    if _wxid == wxid:
        return True

node_head = scan_and_match_value(prcs, contact_head, match_func=match_func2)
node_head = node_head - 0x40
print(hex(node_head))
for i in Contacts().run_head(prcs, node_head):
    print(i)