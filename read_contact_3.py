
from process import Process


class Contacts:
    contact_list = [] 
    _version = "3.9.12.51"
    pointer_set = set()

    def get_tree(self, prcs:Process, head:int):
        if not head:
            raise Exception("查找内存联系人失败")
        self.pointer_set.add(head)
        l_pointer = prcs.read8ByteNumber(head)
        m_pointer = prcs.read8ByteNumber(head+0x8)
        r_pointer = prcs.read8ByteNumber(head+0x10)
        self.read_contact(prcs, m_pointer)
        self.read_contact(prcs, l_pointer)
        self.read_contact(prcs, r_pointer)
            
    def read_contact(self, prcs:Process, tree_pointer:int):
        if tree_pointer in self.pointer_set:
            return
        contact_pointer = prcs.read8ByteNumber(tree_pointer+0x40)
        if not contact_pointer:
            return
        wxid = self.read_wstring(prcs, contact_pointer + 0x18)
        if not wxid:
            return 
        wxh = self.read_wstring(prcs, contact_pointer + 0x38)
        nickname = self.read_wstring(prcs, contact_pointer + 0xA8)
        remarks1 = self.read_wstring(prcs, contact_pointer + 0x88)
        self.contact_list.append((nickname, wxh, wxid, remarks1) )
        return self.get_tree(prcs, tree_pointer)
    
    def run_head(self, prcs, head):
        self.get_tree(prcs, head)
        contactsList = self.contact_list.copy()
        self.contact_list.clear()
        return contactsList

    def read_wstring(self, prcs:Process, addr):
        len = prcs.read4ByteNumber(addr + 0x8)
        if not len or len <= 0:
            return ''
        pointer = prcs.read8ByteNumber(addr)
        s = prcs.readStringUtf16(pointer, len)
        return s


if __name__ == "__main__":
    for i in Contacts().run():
        print(i)
        pass

