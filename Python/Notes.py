# vim:encoding=utf-8:ts=2:sw=2:expandtab



class Struct():
  pass

class Integer():
  pass

class String():
  pass

class Decimal():
  pass
 
class Boolean():
  pass

class Sequence():
  pass

class Map():
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
      self...(key, value)





=== GLOBAL NAMESPACE ===
  ServerName
  ServerAddr
  Database











=== INCLUDED FILES AND WHAT THEY CONTAIN ===

      
>>>>
~/Project1/.ConfStruct.py
  1. define required structures and defaults
  2. override with /etc/ConfStrcut.py
  3. override with ~/.ConfStruct.py
<<<<


~/.ConfStruct.py
  Project['CouponExtreme'].Database = 'another'



/etc/ConfStruct.py
  ServerName = 'foo.bar.com'
  ServerAddr = '1.2.3.4'

  Database = Core.DatabaseMap()
  Database['CouponExtreme_2'].Password = 'bababa'





=== HELLO HUMAN ===

Project['SoAndSo'].Mysql.Username (default is 'foo')?
Project['SoAndSo'].MySQL.Password (default is 'pass')?










================ IN PROJECT ============================

----------------------------
ConfStruct-Definition.py

  ID = Core.String()
  MySQL = Core.Database.MySQL(), Required = True
  Rewrite = Core.Apache.RewriteSet(), Required = False
  Path
  And so on...

  class FooBaz(Struct):
    TempServerIP = String()
    TempServerName = String()
      Required = True

  TempServer = FooBaz()


---------------------------------------------------------
ConfStruct-Data.py
  
  Rewrite.Add('...')
  Path = Dirname(.)
  

----------------------------
.ConfStruct.py
  #Override anything on a per-install basis


=================  /etc/ConfStruct.py ====================

Project['CouponExtreme'].MySQL.Database = 'CouponExtreme_2'
Project['CouponExtreme'].MySQL.Host = 'localhost'


=================  ~/.ConfStruct.py ====================

# you the opportunity to override anything you wanted








##########################################################

Step 1: download package / git repo / svn repo / etc...
Step 2: run `confs-human`
Step 3: it will ask you for all "missing" information
Step 4: it will write said information to the project level .ConfStruct file
Step 5: it will run `confs-update` which will build the conf tree and execute actions

Later, when an update is made to the project which requires config changes, then the user can 
  edit /path/to/project/.ConfStruct and make the change
and then run 
  `confs-update`
which will rebuild everything


--
Every ConfStruct target consists of:
1. a set of key=value pairs defining what it is... (user, projectid, server, devlevel, etc...)
2. a file which defines the target structures and provides default values
3. a file which defines actual values (target-specific-values) (NEVER COMMITTED TO SOURCE CONTROL)

/etc/ConfStruct will contain server wide configuration (and config for specific targets)

~/.ConfStruct will contain user wide configuration (and config for specific targets)

--
The order is:
1. include /path/to/target/confstruct, which defines structures and defaults
2. include /etc/confstruct, which directives are applied as applicable to the current target
3. include ~/.confstruct (if applicable), which directives are applied as applicable to current target
4. current target is validated, and errors are raised here
5. actions are run, which could be anything (these are defined in projects confstruct file)

--
What defines an applicable setting?
- all attributes defined on the setting must be an exact match for attributes on the target



###########################################################
# /home/jason/DevLevel.2/MyProject/confstruct

from ConfStruct.Util import *
from os.path import abspath

# ---------------------------------------------------------
# Define Schema

Target        = Types.WB4Target()

Postgres      = Types.Database.MySQL()

AmazonS3      = Types.AWS.S3()

FileHashMap   = Types.Dict()

NginxServer   = Types.Nginx.Server()

VirtualHost   = Types.Apache.VirtualHost()

GoogleMapKey  = Types.String(Required=True, Length=64)

FileServer    = Types.WB4.FileServer()

# ---------------------------------------------------------
# Define Actions

def Action():
  




# ---------------------------------------------------------
# Define Default Values

Target.ProjectIdentifier = 'CouponVillage'
Target.Path = abspath('.')
Target.DevLevel.AutoSet()
Target.User.AutoSet()
Target.Path.AutoSet()

FileHashMap['Web/Static/Foo.js'] = sha1file('Web/Static/Foo.js')
FileHashMap['Web/Static/Bar.js'] = sha1file('Web/Static/Bar.js')

NginxServer.ServerName = 'www.couponvillageusa.com'
NginxServer.ServerAlias.Add('couponvillageusa.com')
NginxServer.EnableCaching(86400*365*10, ['*.jpg', '*.css', '*.js'])

NginxServer.Location[0].Path = '/Static'
NginxServer.Location[0].ServeFrom = join(Target.Path, 'Web', 'Static')

VirtualHost.Rewrite.AddRule('^/content/([0-9]+)$', '/main/content.php$1', '[PSA,R=302,L]')
VirtualHost.Rewrite.AddRule('^/admin$', '/main/adminlogin.php')






###########################################################
# /etc/confstruct
# these settings apply to every invocation of confs-* on this server

# convenience to auto-set database and database username to sensible defaults
if isset('Postgres'):
  Postgres.Database = "{0}_{1}".format(Target.ProjectIdentifier, Target.DevLevel)
  Postgres.Username = Target.ProjectIdentifier
  Postgres.Host = 'dc40.appcove.net'

# convenience to auto-set database and database username to sensible defaults
if isset('MySQL'):
  MySQL.Database = "{0}_{1}".format(Target.ProjectIdentifier, Target.DevLevel)
  MySQL.Username = Target.ProjectIdentifier
  MySQL.Host = 'dc40.appcove.net'

# auto-set fileserver on this host
if isset('FileServer'):
  FileServer.Host = 'file.izrm.net'
  FileServer.Database = Instance.ProjectIdentifier

# Project Settings for ALL CouponVillage
if match(Target, ProjectIdentifier='CouponVillage'):
  Postgres.Password = '23iu2309rjf9284hn23f'

# Project settings for PRODUCTION CouponVillage
if match(Target, ProjectIdentifier='CouponVillage', DevLevel=0):
  GoogleMapKey = '3jd2093mvn9u23nfcedsunofvvmsdicm02mc0imi9ewnv9n9unc0m3cn0ejcmc2'

# Project settings for PREVIEW CouponVillage
if match(Target, ProjectIdentifier='CouponVillage', DevLevel=1):
  GoogleMapKey = 'nc9nc8cn9n39cn9b9fbn398dn93cn9cn39c93ndc9n9ewn9cn2390cn239cn2nc'


###########################################################
# /home/jason/.confstruct

# login to my personal databases with my username and password
if isset('Postgres'):
  Postgres.Database = "jason_{0}".format(Postgres.Database)
  Postgres.Username = "jason"
  Postgres.Password = "fsjd9fu2f3"


###########################################################
# /home/jason/DevLevel.2/CouponVillage/confstruct.local
# This file is designed to not be committed to the repo, so it merely exists
# as a "final" place for settings to reside.

GoogleMapKey = '03u02jf3029jc0v03vn04n98nv9n4v934nv94nfc934cn9vn94nv9348n9vnv49'
  
###########################################################



























