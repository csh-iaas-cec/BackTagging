import oci
from oci.pagination import list_call_get_all_results
import Config
import sys
import logging
from logs import StreamToLogger

sl = StreamToLogger("STDOUT", logging.INFO)
sys.stdout = sl

# stderr_logger = logging.getLogger('STDERR')
sl = StreamToLogger("STDERR", logging.ERROR)
sys.stderr = sl


class Volume:
    def __init__(self):
        config = {}
        try:
            signer = Config.signer
            self.block_storage_client = oci.core.BlockstorageClient(
                config=config, signer=signer
            )
        except Exception:
            config = Config.config
            self.block_storage_client = oci.core.BlockstorageClient(config=config)

    # Request to list all volume backups
    def list_volume_backups(self, compartment_id):
        try:
            return list_call_get_all_results(
                self.block_storage_client.list_volume_backups, compartment_id
            ).data
        except oci.exceptions.ServiceError as identifier:
            print(identifier)
            exit()

    

    # Request to update the volume tags
    def update_volume_tag(self, volume_id, tag):
        try:
            volume_detail = self.block_storage_client.get_volume(volume_id).data
            volume_group = volume_detail.defined_tags["Block-Storage-tags"]["VolumeGroup"]
            expiration = volume_detail.defined_tags["Block-Storage-tags"]["Expiration"]
            tag = {
                "Block-Storage-tags": {
                    "InstanceName": tag["InstanceName"],
                    "VSAD": tag["VSAD"],
                    "Expiration": expiration,
                    "VolumeGroup": volume_group
                }
            }
        
            volume_details = oci.core.models.UpdateVolumeDetails(
                defined_tags=tag
            )
            self.block_storage_client.update_volume(volume_id, volume_details)
            print("Updated Volume tags", volume_id)
        except KeyError:
            if(volume_detail.lifecycle_state == "TERMINATED"):
                pass
            else:
                print("Block-Storage-tags not declared", volume_backup_id)
        except oci.exceptions.ServiceError as identifier:
            if(identifier.status == 400):
                print(volume_id+" already updated")
            else:
                print(identifier)
        except Exception:
            print("Volume is not present")

    # Request to update the volume backup tags
    def update_volume_backup_tag(self, volume_backup_id, tag):
        try:
            volume_detail = self.block_storage_client.get_volume_backup(volume_backup_id).data
            volume_group = volume_detail.defined_tags["Block-Storage-tags"]["VolumeGroup"]
            expiration = volume_detail.defined_tags["Block-Storage-tags"]["Expiration"]
            tag = {
                "Block-Storage-tags": {
                    "InstanceName": tag["InstanceName"],
                    "VSAD": tag["VSAD"],
                    "Expiration": expiration,
                    "VolumeGroup": volume_group
                }
            }
            volume_backup_details = oci.core.models.UpdateVolumeBackupDetails(
                defined_tags=tag
            )
            self.block_storage_client.update_volume_backup(
                volume_backup_id, volume_backup_details
            )
            print("Updated Volume Backup tags", volume_backup_id)
        except KeyError:
            if(volume_detail.lifecycle_state == "TERMINATED"):
                pass
            else:
                print("Block-Storage-tags not declared", volume_backup_id)
   
        except oci.exceptions.ServiceError as identifier:
            if(identifier.status == 400):
                print(volume_backup_id+" already updated")
            else:
                print(identifier)
        except Exception:
            print("Volume Backup is not present")
