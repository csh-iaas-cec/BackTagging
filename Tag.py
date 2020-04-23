import oci
from Volume import Volume
from Store import Store


class Tag:
    def __init__(self, compartment_id=None):
        self.storeObj = Store(compartment_id)
        self.volumeObj = Volume()
        self.initialize()

    def initialize(self):
        self.update_tags()
        


    # updates all the volume tags present in volume attachments
    def update_tags(self):
        for i in self.storeObj.volume_attachments:
            self.storeObj.store_instance_tags(i.instance_id)
            self.storeObj.store_volume_tags(i.volume_id)
        for i in self.storeObj.boot_volume_attachments:
            self.storeObj.store_boot_volume_tags(i.boot_volume_id)

    

    def list_backups_from_volume(self, volume_id):
        try:
            volume_backups = [backup_id for backup_id, vol_id in self.storeObj.volume_backups_volume.items() if vol_id==volume_id]
            # print(self.storeObj.volume_backups_volume)
        except Exception:
            print("No backups")
            volume_backups = None
        return volume_backups

    def list_backups_from_boot_volume(self, volume_id):
        try:
            boot_volume_backups = [backup_id for backup_id, boot_vol_id in self.storeObj.boot_volume_backups_boot_volume.items() if boot_vol_id==volume_id]
            # print(boot_volume_backups)
        except Exception:
            print("No backups")
            boot_volume_backups = None
        return boot_volume_backups

    # gets attached volume_ids of an instance
    def list_volumes_from_instances(self, instance_id):
        try:
            # print(self.storeObj.attached_volume)
            volumes = [volume_id for volume_id, inst_id in self.storeObj.attached_volume.items() if inst_id == instance_id]
        except Exception:
            volumes = None
        return volumes

    def list_boot_volumes_from_instances(self, instance_id):
        try:
            # print(self.storeObj.attached_volume)
            volumes = [volume_id for volume_id, inst_id in self.storeObj.attached_boot_volume.items() if inst_id == instance_id]
        except Exception:
            volumes = None
        return volumes

    
        

    # gets the volume ids and updates the volume tag
    def update_tags_from_instance(self, instance_id):
        volume_ids = self.list_volumes_from_instances(instance_id)
        boot_vol_ids = self.list_boot_volumes_from_instances(instance_id)
        for id in volume_ids:
            self.update_backup_tags_from_volume(id)
        for id in boot_vol_ids:
            self.update_backup_tags_from_boot_volume(id)

    

    # updates the volume tag
    def update_volume_tag(self, volume_id):
        try:
            self.volumeObj.update_volume_tag(volume_id, self.storeObj.get_volume_tags(volume_id))
        except Exception:
            raise KeyError


    def update_boot_volume_tag(self, volume_id):
        try:
            self.volumeObj.update_boot_volume_tag(volume_id, self.storeObj.get_boot_volume_tags(volume_id))
        except Exception:
            raise KeyError
        

    def update_volume_backup_tag(self, volume_backup_id, tag):
        self.volumeObj.update_volume_backup_tag(volume_backup_id, tag)

    def update_boot_volume_backup_tag(self, volume_backup_id, tag):
        self.volumeObj.update_boot_volume_backup_tag(volume_backup_id, tag)

    # def update_database_backup_tag(self, db_backup_id, tag):
    #     self.dbObj.update_database_backup_tag(db_backup_id, tag)

    def get_volume_from_backup(self, volume_backup_id):
        try:
            return self.storeObj.get_volume_from_backup(volume_backup_id)
        except Exception:
            raise KeyError

    def get_boot_volume_from_backup(self, volume_backup_id):
        try:
            return self.storeObj.get_boot_volume_from_backup(volume_backup_id)
        except Exception:
            raise KeyError

    #updates the volume backup tag
    def update_tags_from_block_volume_backup(self, volume_backup_id):
        try:
            vol_id = self.get_volume_from_backup(volume_backup_id)
            self.update_volume_tag(vol_id)
            self.update_volume_backup_tag(volume_backup_id, self.storeObj.get_volume_tags(vol_id))
        except Exception:
            pass

    def update_tags_from_boot_volume_backup(self, volume_backup_id):
        try:
            vol_id = self.get_boot_volume_from_backup(volume_backup_id)
            self.update_boot_volume_tag(vol_id)
            self.update_boot_volume_backup_tag(volume_backup_id, self.storeObj.get_boot_volume_tags(vol_id))
        except Exception:
            pass
        

    def update_backup_tags_from_volume(self, volume_id):
        try:
            self.update_volume_tag(volume_id)
            for backup_id in self.list_backups_from_volume(volume_id):
                # print(backup_id)
                self.update_volume_backup_tag(backup_id, self.storeObj.get_volume_tags(volume_id))
        except Exception:
            pass

    def update_backup_tags_from_boot_volume(self, volume_id):
        try:
            self.update_boot_volume_tag(volume_id)
            for backup_id in self.list_backups_from_boot_volume(volume_id):
                self.update_boot_volume_backup_tag(backup_id, self.storeObj.get_boot_volume_tags(volume_id))
        except Exception:
            pass

    # def update_tags_from_database(self, db_id):
    #     try:
    #         self.update_database_tag(volume_id)
    #         for backup_id in self.list_backups_from_boot_volume(volume_id):
    #             self.update_boot_volume_backup_tag(backup_id, self.storeObj.get_boot_volume_tags(volume_id))
    #     except Exception:
    #         pass

    # def list_db_backup_from_instances(self, db_id):
    #     try:
    #         print(self.storeObj.attached_volume)
    #         volumes = [volume_id for volume_id, inst_id in self.storeObj.attached_boot_volume.items() if inst_id == instance_id]
    #     except Exception:
    #         volumes = None
    #     return volumes
        

    def update_tags_from_compartment(self):
        for volume_id in self.storeObj.attached_volume.keys():
            self.update_backup_tags_from_volume(volume_id)
        for boot_volume_id in self.storeObj.attached_boot_volume.keys():
            self.update_backup_tags_from_boot_volume(boot_volume_id)