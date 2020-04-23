import Config
import oci

os_client = oci.object_storage.ObjectStorageClient(config={}, signer = Config.signer)
print(os_client.get_namespace().data)