import os
import argparse
import configparser


if __name__ == "__main__":
    description = "\n".join(["This updates the tags of volumes and volume groups. Logs out on out.log","pip install -r requirements.txt","python main.py <config_profile>"])
    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--all", help="Update all the tags in the tenancy", action="store_true")
    parser.add_argument('--compartment_id',
                        help="Updates all the volume and backups tag from instances in the specified compartment ")
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
            tagObj.update_tags_from_compartment()
        else:
            print("Please provide --compartment_id or --all. For further run --help")