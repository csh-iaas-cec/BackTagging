from Instance import Instance
from Volume import Volume
from Compartment import Compartment
from UniqueKeyDict import UniqueKeyDict


class Store:
    def __init__(self, compartment_id=None):
        self.volume_attachments = list()
        self.boot_volume_attachments = list()
        self.database_tags = UniqueKeyDict()
        self.database_backups = list()
        self.volume_backups = list()
        self.boot_volume_backups = list()
        self.volume_backups_volume = UniqueKeyDict()
        self.boot_volume_backups_boot_volume = UniqueKeyDict()
        self.attached_volume = UniqueKeyDict()
        self.attached_boot_volume = UniqueKeyDict()
        self.instance_tags = UniqueKeyDict()
        self.volume_tags = UniqueKeyDict()
        self.database_backup_db = UniqueKeyDict()
        self.boot_volume_tags = UniqueKeyDict()
        self.compartment_id = compartment_id
        self.instanceObj = Instance()
        self.volumeObj = Volume()
        self.compartment_list = list()
        self.compartment_obj = Compartment()
        self.initialize()

    def update_compartment_list(self):
        if(self.compartment_id):
            self.compartment_list.append(self.compartment_id)
        else:
            self.compartment_obj.store_compartments()
            self.compartment_list = [
                i.id for i in self.compartment_obj.compartments]

    def initialize(self):
        self.update_compartment_list()
        for i in self.compartment_list:
            self.store_volume_attachments(i)
            self.store_boot_volume_attachments(i)
            self.store_volume_backups_details(i)
            self.store_boot_volume_backups_details(i)
        self.store_volume_and_volume_backups()
        self.store_attached_volume_instance()
        self.store_attached_boot_volume_instance()
        self.store_boot_volume_and_boot_volume_backups()

    def get_attached_volume(self):
        return self.attached_volume

    def get_instance_tags(self, instance_id):
        try:
            return self.instance_tags[instance_id]
        except KeyError as identifier:
            print(identifier)
            print("Instance not present in the compartment")
            raise

    def get_volume_tags(self, volume_id):
        try:
            return self.volume_tags[volume_id]
        except KeyError:
            print("Volume Id Incorrect")
            print(volume_id)
            raise KeyError

    def get_boot_volume_tags(self, boot_volume_id):
        try:
            return self.boot_volume_tags[boot_volume_id]
        except KeyError:
            print("Volume Id Incorrect")
            print(boot_volume_id)
            raise KeyError

    # Store the volume attachments so that we no need to request
    # each time to get the list of volume attachments

    def store_volume_attachments(self, compartment_id):
        for i in self.instanceObj.list_volume_attachments(compartment_id):
            self.volume_attachments.append(i)

    def store_boot_volume_attachments(self, compartment_id):
        for ad in self.compartment_obj.availability_domain_list:
            for i in self.instanceObj.list_boot_volume_attachments(ad.name, compartment_id):
                self.boot_volume_attachments.append(i)

    def store_volume_backups_details(self, compartment_id):
        for i in self.volumeObj.list_volume_backups(compartment_id):
            self.volume_backups.append(i)

    def store_boot_volume_backups_details(self, compartment_id):
        for i in self.volumeObj.list_boot_volume_backups(compartment_id):
            self.boot_volume_backups.append(i)

    # def store_database_backups_details(self, compartment_id):
    #     for i in self.dbObj.list_backups(compartment_id):
    #         self.database_backups.append(i)

    def store_volume_and_volume_backups(self):
        for i in self.volume_backups:
            vol_id = i.volume_id
            backup_id = i.id
            self.volume_backups_volume.update({backup_id: vol_id})

    def store_boot_volume_and_boot_volume_backups(self):
        for i in self.boot_volume_backups:
            vol_id = i.boot_volume_id
            backup_id = i.id
            self.boot_volume_backups_boot_volume.update({backup_id: vol_id})

    def store_database_and_database_backups(self):
        for i in self.database_backups:
            db_id = i.database_id
            backup_id = i.id
            self.database_backup_db.update({backup_id: db_id})

    def get_volume_from_backup(self, volume_backup_id):
        try:
            return self.volume_backups_volume[volume_backup_id]
        except Exception:
            print("Block Volume Backup Id Incorrect")
            print(volume_backup_id)
            raise KeyError

    def get_boot_volume_from_backup(self, boot_volume_backup_id):
        try:
            return self.boot_volume_backups_boot_volume[boot_volume_backup_id]
        except Exception:
            print("Boot Volume Backup Id Incorrect")
            print(boot_volume_backup_id)
            raise KeyError

    def get_database_from_backup(self, db_backup_id):
        try:
            return self.database_backup_db[db_backup_id]
        except Exception:
            print("Database Volume Id Incorrect")
            print(db_backup_id)
            raise KeyError

    # storing the values of attached Volumes to Instance

    def store_attached_volume_instance(self):
        for i in self.volume_attachments:
            vol_id = i.volume_id
            inst_id = i.instance_id
            self.attached_volume.update({vol_id: inst_id})

    def store_attached_boot_volume_instance(self):

        for i in self.boot_volume_attachments:
            vol_id = i.boot_volume_id
            inst_id = i.instance_id
            print(vol_id, inst_id)
            self.attached_boot_volume.update({vol_id: inst_id})

    # gets the instance tag and caches the instance tags to reduce number of request
    def store_instance_tags(self, instance_id):
        try:
            tags = self.instance_tags[instance_id]
        except KeyError:
            instance_details = self.instanceObj.get_instance_details(
                instance_id)
            tags = dict()
            tags["defined_tags"] = instance_details.defined_tags
            tags["freeform_tags"] = instance_details.freeform_tags
            self.instance_tags.update({instance_id: tags})

    # def store_database_tags(self, db_id):
    #     try:
    #         tags = self.database_tags[db_id]
    #     except KeyError:
    #         db_details = self.dbObj.get_db_details(db_id)
    #         tags = dict()
    #         tags["defined_tags"] = db_details.defined_tags
    #         tags["freeform_tags"] = db_details.freeform_tags
    #         self.database_tags.update({db_id:tags})

    # caches the volume tags to reduce the number of request while udpating volume backup
    def store_volume_tags(self, volume_id):
        try:
            self.volume_tags[volume_id] = self.instance_tags[self.attached_volume[volume_id]]
        except KeyError:
            print("Volume is not attached to any instance")

    def store_boot_volume_tags(self, boot_volume_id):
        try:
            self.boot_volume_tags[boot_volume_id] = self.instance_tags[self.attached_boot_volume[boot_volume_id]]
        except KeyError:
            print("Boot Volume is not attached to any instance")
