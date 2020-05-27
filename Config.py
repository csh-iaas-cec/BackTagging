import oci
import configparser


# get the cloud shell delegated authentication token
# delegation_token = open('/etc/oci/delegation_token', 'r').read()

# configParser = configparser.RawConfigParser()   
# configFilePath = r'/etc/oci/config'
# configParser.read(configFilePath)

# tenancy_id = configParser.get('us-ashburn-1', 'tenancy')




# # create the api request signer
# signer = oci.auth.signers.InstancePrincipalsDelegationTokenSigner(
#    delegation_token=delegation_token
# )
from oci.config import from_file
config = from_file('~/.oci/config',"red")