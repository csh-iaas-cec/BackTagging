from Volume import Volume
from Instance import Instance
from Compartment import Compartment
from oci.database import DatabaseClient
from Config import Config
vol = Volume("orasenatdhubsred01")
ins = Instance("orasenatdhubsred01")
comp = Compartment("orasenatdhubsred01")
config = Config("orasenatdhubsred01")
db_client = DatabaseClient(config.config)
print(db_client.list_backups(compartment_id="ocid1.compartment.oc1..aaaaaaaae4364npm55dpakr5e6sfpce5su2nhj6ane27344cjsvgb2e5lkra").data)