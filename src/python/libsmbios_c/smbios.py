# vim:tw=0:expandtab:autoindent:tabstop=4:shiftwidth=4:filetype=python:

  #############################################################################
  #
  # Copyright (c) 2005 Dell Computer Corporation
  # Dual Licenced under GNU GPL and OSL
  #
  #############################################################################
"""
smbios:
    python interface to functions in libsmbios_c  obj/smbios.h
"""

# imports (alphabetical)
import ctypes
import exceptions

from _common import *

__all__ = ["SmbiosAccess", "SMBIOS_DEFAULTS", "SMBIOS_GET_SINGLETON", "SMBIOS_GET_NEW", "SMBIOS_UNIT_TEST_MODE"]

SMBIOS_DEFAULTS      =0x0000
SMBIOS_GET_SINGLETON =0x0001
SMBIOS_GET_NEW       =0x0002
SMBIOS_UNIT_TEST_MODE=0x0004

class SmbiosStructure(ctypes.Structure): 
    def getString(self, off):
        return _libsmbios_c.smbios_struct_get_string_from_offset(self, off)

    def getStringNumber(self, num):
        return _libsmbios_c.smbios_struct_get_string_number(self, num)

    def getType(self):
        return _libsmbios_c.smbios_struct_get_type(self)

    def getLength(self):
        return _libsmbios_c.smbios_struct_get_length(self)

    def getHandle(self):
        return _libsmbios_c.smbios_struct_get_handle(self)

    # use struct module to pull data out
    def getData(self, offset, len):
        buf = ctypes.create_string_buffer(len)
        _libsmbios_c.smbios_struct_get_data(self, buf, offset, len)
        return buf.raw

def SmbiosTable(flags=SMBIOS_GET_SINGLETON, factory_args=None):
    if factory_args is None: factory_args = []
    if _SmbiosTable._instance is None:
        _SmbiosTable._instance = _SmbiosTable( flags, *factory_args)
    return _SmbiosTable._instance

class _SmbiosTable(object):
    _instance = None
    def __init__(self, *args):
        self._tableobj = None
        self._tableobj = _libsmbios_c.smbios_table_factory(*args)

    def __del__(self):
        _libsmbios_c.smbios_table_free(self._tableobj)

    def __iter__(self):
        cur = ctypes.POINTER(SmbiosStructure)()
        while 1:
            cur =_libsmbios_c.smbios_table_get_next_struct( self._tableobj, cur )
            if bool(cur):
                yield cur.contents
            else:
                raise exceptions.StopIteration("hit end of table.")

    def iterByType(self, t):
        cur = ctypes.POINTER(SmbiosStructure)()
        while 1:
            cur =_libsmbios_c.smbios_table_get_next_struct( self._tableobj, cur )
            if bool(cur):
                if cur.contents.getType() == t:
                    yield cur.contents
            else:
                raise exceptions.StopIteration("hit end of table.")

    def getStructureByHandle(self, handle):
        cur = ctypes.POINTER(SmbiosStructure)()
        cur =_libsmbios_c.smbios_table_get_next_struct_by_handle( self._tableobj, cur, handle )
        if not bool(cur):
            raise exceptions.Exception("no such handle %s" % handle)
        return cur.contents

    def getStructureByType(self, t):
        cur = ctypes.POINTER(SmbiosStructure)()
        cur =_libsmbios_c.smbios_table_get_next_struct_by_type( self._tableobj, cur, t )
        if not bool(cur):
            raise exceptions.Exception("no such type %s" % t)
        return cur.contents

# initialize libsmbios lib
_libsmbios_c = ctypes.cdll.LoadLibrary("libsmbios_c.so.2")

#struct smbios_table;
class _smbios_table(ctypes.Structure): pass

#// format error string
#const char *smbios_table_strerror(const struct smbios_table *m);
# define strerror first so we can use it in error checking other functions.
_libsmbios_c.smbios_table_strerror.argtypes = [ ctypes.POINTER(_smbios_table) ]
_libsmbios_c.smbios_table_strerror.restype = ctypes.c_char_p
def _strerror(obj):
    return Exception(_libsmbios_c.smbios_table_strerror(obj))


#struct smbios_table *smbios_table_factory(int flags, ...);
# dont define argtypes because this is a varargs function...
#_libsmbios_c.smbios_table_factory.argtypes = [ctypes.c_int, ]
_libsmbios_c.smbios_table_factory.restype = ctypes.POINTER(_smbios_table)
_libsmbios_c.smbios_table_factory.errcheck = errorOnNullPtrFN(lambda r,f,a: _strerror(r))

#void   smbios_table_free(struct smbios_table *);
_libsmbios_c.smbios_table_free.argtypes = [ ctypes.POINTER(_smbios_table) ]
_libsmbios_c.smbios_table_free.restype = None

#struct smbios_struct *smbios_table_get_next_struct(const struct smbios_table *, const struct smbios_struct *cur);
_libsmbios_c.smbios_table_get_next_struct.argtypes = [ ctypes.POINTER(_smbios_table), ctypes.POINTER(SmbiosStructure) ]
_libsmbios_c.smbios_table_get_next_struct.restype = ctypes.POINTER(SmbiosStructure)

#struct smbios_struct *smbios_table_get_next_struct_by_type(const struct smbios_table *, const struct smbios_struct *cur);
_libsmbios_c.smbios_table_get_next_struct_by_type.argtypes = [ ctypes.POINTER(_smbios_table), ctypes.POINTER(SmbiosStructure), ctypes.c_uint8 ]
_libsmbios_c.smbios_table_get_next_struct_by_type.restype = ctypes.POINTER(SmbiosStructure)

#struct smbios_struct *smbios_table_get_next_struct_by_handle(const struct smbios_table *, const struct smbios_struct *cur);
_libsmbios_c.smbios_table_get_next_struct_by_handle.argtypes = [ ctypes.POINTER(_smbios_table), ctypes.POINTER(SmbiosStructure), ctypes.c_uint16 ]
_libsmbios_c.smbios_table_get_next_struct_by_handle.restype = ctypes.POINTER(SmbiosStructure)

#u8 DLL_SPEC smbios_struct_get_type(const struct smbios_struct *);
_libsmbios_c.smbios_struct_get_type.argtypes = [ ctypes.POINTER(SmbiosStructure) ]
_libsmbios_c.smbios_struct_get_type.restype = ctypes.c_uint8

#u8 DLL_SPEC smbios_struct_get_length(const struct smbios_struct *);
_libsmbios_c.smbios_struct_get_length.argtypes = [ ctypes.POINTER(SmbiosStructure) ]
_libsmbios_c.smbios_struct_get_length.restype = ctypes.c_uint8

#u16 DLL_SPEC smbios_struct_get_handle(const struct smbios_struct *);
_libsmbios_c.smbios_struct_get_handle.argtypes = [ ctypes.POINTER(SmbiosStructure) ]
_libsmbios_c.smbios_struct_get_handle.restype = ctypes.c_uint16

#const char * DLL_SPEC smbios_struct_get_string_from_offset(const struct smbios_struct *s, u8 offset);
_libsmbios_c.smbios_struct_get_string_from_offset.argtypes = [ ctypes.POINTER(SmbiosStructure), ctypes.c_uint8 ]
_libsmbios_c.smbios_struct_get_string_from_offset.restype = ctypes.c_char_p
_libsmbios_c.smbios_table_factory.errcheck = errorOnNullPtrFN(lambda r,f,a: exceptions.Exception("String from offset %d doesnt exist" % a[1]))

#const char * DLL_SPEC smbios_struct_get_string_number(const struct smbios_struct *s, u8 which);
_libsmbios_c.smbios_struct_get_string_number.argtypes = [ ctypes.POINTER(SmbiosStructure), ctypes.c_uint8 ]
_libsmbios_c.smbios_struct_get_string_number.restype = ctypes.c_char_p
_libsmbios_c.smbios_struct_get_string_number.errcheck = errorOnNullPtrFN(lambda r,f,a: exceptions.Exception("String number %d doesnt exist" % a[1]))

#int DLL_SPEC smbios_struct_get_data(const struct smbios_struct *s, void *dest, u8 offset, size_t len);
_libsmbios_c.smbios_struct_get_data.argtypes = [ ctypes.POINTER(SmbiosStructure), ctypes.c_void_p, ctypes.c_uint8, ctypes.c_size_t ]
_libsmbios_c.smbios_struct_get_data.restype = ctypes.c_int
_libsmbios_c.smbios_struct_get_data.errcheck = errorOnNegativeFN(lambda r,f,a: exceptions.Exception("something bad happened"))



