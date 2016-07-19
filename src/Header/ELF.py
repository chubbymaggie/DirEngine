# -*- coding: utf-8 -*-
try:
    from elftools.elf.elffile import ELFFile
except ImportError:
    ELFFile = None

from error import Error
from header._header import _header
from header.Archinfo.ArchSelector import ArchSelector

class ELF(_header):
    _backend = None
    _elf = None
    def __init__(self,path,filetype,stream=None,backend=None):
        if ELFFile is None:
            raise INSTALLerror("Install the ELFFile module to use the ELF backend!") 
        super(ELF, self).__init__(path,filetype)
        self._backend = backend
        if stream is None:
            f = open(path,'rb')
            self._elf = ELFFile(f)
        else:
            self._elf = ELFFile(stream)  
        
        self._elf.stream.seek(0)
        self.bin_data = self._elf.stream.read()
        self._elf.stream.seek(0)
        self.arch_str = self._elf.header.e_machine
        self._entry = self._elf.header.e_entry
        if(self._elf.little_endian):
            self.endness = "Iend_LE"
        else:
            self.endness = "Iend_BE"
        self.set_arch(ArchSelector().search(self.arch_str,self.endness))

    def read_addr(self,addr):
        return addr