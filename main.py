import os
import argparse
import configparser


if __name__ == "__main__":
    description = "\n".join(["This updates the tags of volumes and volume groups","pip install -r requirements.txt","python main.py <config_profile>"])
    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--all", help="Update all the tags in the tenancy", action="store_true")
    parser.add_argument('--compartment_id',
                        help="Updates all the volume and backups tag from instances in the specified compartment ")
    parser.add_argument('--instance_id',
                        help="Updates the volume and backups tags from the given instance id")
    parser.add_argument('--volume_id',
                        help="Updates the volume and volume group tags from the given volume id")
    parser.add_argument('--volume_backup_id',
                        help="Updates the volume and volume group tags from the given volume backup id")
    args = parser.parse_args()
    if(args.all):
        from Tag import Tag
        tagObj = Tag()
        tagObj.update_tags_from_compartment()
    else:
        if(args.compartment_id):
            from Tag import Tag
            compartment_id = str(args.compartment_id)
            tagObj = Tag(compartment_id)
            if(args.instance_id):
                instance_id = str(args.instance_id)
                tagObj.update_tags_from_instance(instance_id)
            elif(args.volume_id):
                volume_id = args.volume_id
                tagObj.update_backup_tags_from_volume(volume_id)
            elif(args.volume_backup_id):
                volume_backup_id = args.volume_backup_id
                tagObj.update_tags_from_block_volume_backup(volume_backup_id)
            else:
                tagObj.update_tags_from_compartment()
        else:
            print("Please provide compartment ID or --all. For further run --help")