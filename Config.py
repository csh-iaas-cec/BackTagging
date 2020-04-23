from oci.config import from_file

class Config:
    def __init__(self, tenancy_name):
        self.config = from_file('~/.oci/config',tenancy_name)
