import oci
from oci.pagination import list_call_get_all_results
import Config

class Volume:
    def __init__(self):
        signer = Config.signer
        config = {}
        self.block_storage_client = oci.core.BlockstorageClient(config=config, signer=signer)
        


    #Request to list all volume backups
    def list_volume_backups(self, compartment_id):
        return list_call_get_all_results(self.block_storage_client.list_volume_backups,
            compartment_id).data

    def list_boot_volume_backups(self, compartment_id):
        return list_call_get_all_results(self.block_storage_client.list_boot_volume_backups,
            compartment_id).data

    
    def remove_volume_tag(self, volume_id):
        try:
            volume_details = oci.core.models.UpdateVolumeDetails(defined_tags = {},
                freeform_tags = {})
            self.block_storage_client.update_volume(volume_id, volume_details)
            print("Removed Volume tags", volume_id)
        except oci.exceptions.ServiceError as identifier:
            print(identifier.message)
        except Exception:
            print("Volume is not present")

    def remove_boot_volume_tag(self, volume_id):
        try:
            volume_details = oci.core.models.UpdateBootVolumeDetails(defined_tags = {},
                freeform_tags = {})
            self.block_storage_client.update_boot_volume(volume_id, volume_details)
            print("Removed Boot Volume tags", volume_id)
        except oci.exceptions.ServiceError as identifier:
            print(identifier.message)
            
        except Exception:
            print("Boot Volume is not present")

    def remove_volume_backup_tag(self, volume_backup_id):
        try:
            volume_details = oci.core.models.UpdateVolumeBackupDetails(defined_tags = {},
                freeform_tags = {})
            self.block_storage_client.update_volume_backup(volume_backup_id, volume_details)
            print("Removed Volume Backup tags", volume_backup_id)
        except oci.exceptions.ServiceError as identifier:
            print(identifier.message)
        except Exception:
            print("Volume Backup is not present")

    def remove_boot_volume_backup_tag(self, volume_backup_id):
        # print(volume_backup_id)
        try:
            volume_details = oci.core.models.UpdateBootVolumeBackupDetails(defined_tags = {},
                freeform_tags = {})
            self.block_storage_client.update_boot_volume_backup(volume_backup_id, volume_details)
            print("Removed Boot Volume Backup tags", volume_backup_id)
        except oci.exceptions.ServiceError:
            # print(identifier.message)
            print(volume_backup_id)
        except Exception:
            print("Boot Volume Backup is not present")


    # Request to update the volume tags
    def update_volume_tag(self, volume_id, tag):
        self.remove_volume_tag(volume_id)
        try:
            volume_details = oci.core.models.UpdateVolumeDetails(defined_tags = tag["defined_tags"],
                freeform_tags = tag["freeform_tags"])
            self.block_storage_client.update_volume(volume_id, volume_details)
            print("Updated Volume tags", volume_id)
        except oci.exceptions.ServiceError as identifier:
            print(identifier.message)
        except Exception:
            print("Volume is not present")
            

    def update_boot_volume_tag(self, volume_id, tag):
        self.remove_boot_volume_tag(volume_id)
        try:
            volume_details = oci.core.models.UpdateBootVolumeDetails(defined_tags = tag["defined_tags"],
                freeform_tags = tag["freeform_tags"])
            self.block_storage_client.update_boot_volume(volume_id, volume_details)
            print("Updated Boot Volume tags", volume_id)
        except oci.exceptions.ServiceError as identifier:
            print(identifier.message)
        except Exception:
            print("Boot Volume is not present")
        

    # Request to update the volume backup tags
    def update_volume_backup_tag(self, volume_backup_id, tag):
        self.remove_volume_backup_tag(volume_backup_id)
        try:
            volume_backup_details = oci.core.models.UpdateVolumeBackupDetails(defined_tags = tag["defined_tags"],
                freeform_tags = tag["freeform_tags"])
            self.block_storage_client.update_volume_backup(volume_backup_id, volume_backup_details)
            print("Updated Volume Backup tags", volume_backup_id)
        except Exception:
            print("Volume Backup is not present")

    def update_boot_volume_backup_tag(self, volume_backup_id, tag):
        self.remove_boot_volume_backup_tag(volume_backup_id)
        try:
            volume_backup_details = oci.core.models.UpdateBootVolumeBackupDetails(defined_tags = tag["defined_tags"],
                freeform_tags = tag["freeform_tags"])
            self.block_storage_client.update_boot_volume_backup(volume_backup_id, volume_backup_details)
            print("Updated Boot Volume Backup tags", volume_backup_id)
        except oci.exceptions.ServiceError as identifier:
            print(identifier.message)
        except Exception:
            print("Boot Volume Backup is not present")



