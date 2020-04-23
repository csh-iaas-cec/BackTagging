import oci


# get the cloud shell delegated authentication token
delegation_token = open('/etc/oci/delegation_token', 'r').read()


# create the api request signer
signer = oci.auth.signers.InstancePrincipalsDelegationTokenSigner(
   delegation_token=delegation_token
)