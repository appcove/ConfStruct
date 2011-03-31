# vim:encoding=utf-8:ts=2:sw=2:expandtab

from collections import OrderedDict

class _ClassDict(dict):
  def __init__(self):
    dict.__init__(self)
    self.SubTypes = OrderedDict() 

  def __setitem__(self, key, value):
    if isinstance(value, _Base):
      if key in self.SubTypes:
        raise AttributeError('Sub Type already defined: ' + str(key))
      self.SubTypes[key] = value
    else:
      dict.__setitem__(self, key, value)


class _Base(type):
  @classmethod
  def __prepare__(metacls, name, bases, **kwargs):
    return _ClassDict()

  def __new__(metacls, name, bases, classdict):
    self = type.__new__(metacls, name, bases, classdict)
    self._SubTypes = classdict.SubTypes
    return self


class Struct(metaclass=_Base):
  pass

class Integer(metaclass=_Base):
  pass

class String(metaclass=_Base):
  pass

class Decimal(metaclass=_Base):
  pass
 
class Boolean(metaclass=_Base):
  pass

class Sequence(metaclass=_Base):
  pass

class Map(metaclass=_Base):
  pass


class Account(Struct):
  class Account_ID(Integer): 
    Nullable=False; 
  
  class Name(String): 
    MaxLength=40; 
    Nullable=False
  
  class Users(Sequence): 
    class User(Struct):
      class Username(String): 
        pass
      class Password(String): 
        pass
  
  class Options(Map):
    class Key(String): 
      pass
    
    class Value(String): 
      pass

