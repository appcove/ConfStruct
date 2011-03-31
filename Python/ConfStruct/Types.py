# vim:encoding=utf-8:ts=2:sw=2:expandtab


from decimal import Decimal as decimal

class Type(type):
  pass




class Struct(object, metaclass=Type):
  pass

class Integer(int, metaclass=Type):
  pass

class String(str, metaclass=Type):
  pass

class Decimal(decimal, metaclass=Type):
  pass
 
class Boolean(bool, metaclass=Type):
  pass

class Sequence(list, metaclass=Type):
  pass

class Map(dict, metaclass=Type):
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

    def AddPair(self, Key, Value):
      # validate Key or Value...
      pass




