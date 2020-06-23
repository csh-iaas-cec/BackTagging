import oci
import configparser


from oci.config import from_file
config = from_file('~/.oci/config',"red")