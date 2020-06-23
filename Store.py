from Instance import Instance
from Volume import Volume
from Compartment import Compartment
from UniqueKeyDict import UniqueKeyDict
import logging
import sys
from logs import StreamToLogger

sl = StreamToLogger("STDOUT", logging.INFO)
sys.stdout = sl

sl = StreamToLogger("STDERR", logging.ERROR)
sys.stderr = sl


class Store:
    def __init__(self, compartment_id=None, instance_id=None):
        self.volume_attachments = list()
        self.volume_backups = list()
        self.volume_backups_volume = UniqueKeyDict()
        self.attached_volume = UniqueKeyDict()
        self.instance_tags = UniqueKeyDict()
        self.volume_tags = UniqueKeyDict()
        self.compartment_id = compartment_id
        self.instanceObj = Instance()
        self.volumeObj = Volume()
        self.compartment_list = list()
        self.compartment_obj = Compartment()
        self.initialize()

    def update_compartment_list(self):
        if self.compartment_id:
            self.compartment_list.append(self.compartment_id)
        else:
            self.compartment_obj.store_compartments()
            self.compartment_list = [i.id for i in self.compartment_obj.compartments]

    def initialize(self):
        self.update_compartment_list()
        for i in self.compartment_list:
            self.store_volume_attachments(i)
            self.store_volume_backups_details(i)
        self.store_volume_and_volume_backups()
        self.store_attached_volume_instance()

    def get_attached_volume(self):
        return self.attached_volume

    def get_instance_tags(self, instance_id):
        try:
            return self.instance_tags[instance_id]
        except KeyError as identifier:
            print(identifier)
            # logger.error(identifier)
            # logger.error("Instance not present in the compartment")
            print("Instance not present in the compartment" + instance_id)
            raise

    def get_volume_tags(self, volume_id):
        try:
            return self.volume_tags[volume_id]
        except KeyError:
            print("Volume Id Incorrect " + volume_id)
            # logger.error("Volume Id Incorrect")
            # logger.error(volume_id)
            raise KeyError

    # Store the volume attachments so that we no need to request
    # each time to get the list of volume attachments
    def store_volume_attachments(self, compartment_id):
        for i in self.instanceObj.list_volume_attachments(compartment_id):
            self.volume_attachments.append(i)

    def store_volume_backups_details(self, compartment_id):
        for i in self.volumeObj.list_volume_backups(compartment_id):
            self.volume_backups.append(i)

    def store_volume_and_volume_backups(self):
        for i in self.volume_backups:
            vol_id = i.volume_id
            backup_id = i.id
            self.volume_backups_volume.update({backup_id: vol_id})

    def get_volume_from_backup(self, volume_backup_id):
        try:
            return self.volume_backups_volume[volume_backup_id]
        except Exception:
            print("Block Volume Backup Id Incorrect " + volume_backup_id)
            raise KeyError

    # storing the values of attached Volumes to Instance
    def store_attached_volume_instance(self):
        for i in self.volume_attachments:
            vol_id = i.volume_id
            inst_id = i.instance_id
            self.attached_volume.update({vol_id: inst_id})

    # gets the instance tag and caches the instance tags to reduce number of request
    def store_instance_tags(self, instance_id):
        try:
            tags = self.instance_tags[instance_id]
        except KeyError:
            instance_details = self.instanceObj.get_instance_details(instance_id)
            tags = dict()
            defined_tags = instance_details.defined_tags
            tags["InstanceName"] = defined_tags["Compute-Tag"]["InstanceName"]
            tags["VSAD"] = instance_details.defined_tags["Compute-Tag"]["VSAD"]
            self.instance_tags.update({instance_id: tags})

    # caches the volume tags to reduce the number of request while udpating volume backup
    def store_volume_tags(self, volume_id):
        try:
            self.volume_tags[volume_id] = self.instance_tags[
                self.attached_volume[volume_id]
            ]
        except KeyError:
            print("Volume is not attached to any instance " + volume_id)

