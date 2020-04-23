import Config
import oci
from oci.identity import IdentityClient


# Gets all the compartments from a tenancy
class Compartment:
	def __init__(self):
		self.signer = Config.signer
		print(self.signer.tenancy_id)
		self.config = {}
		self.compartment_id = self.signer.tenancy_id
		self.identity = IdentityClient(config = {}, signer = self.signer)
		self.compartments = list()
		self.availability_domain_list = list()
		self.update_ads()
		
    # send requests to list all compartments and its child
	def list_compartments(self):
		return oci.pagination.list_call_get_all_results(self.identity.list_compartments,
            self.compartment_id,
            compartment_id_in_subtree=True).data

	# Return compartment data and store in a list		
	def store_compartments(self):
		for compartment in self.list_compartments():
			self.compartments.append(compartment)


	def list_availability_domain(self):
		return self.identity.list_availability_domains(self.signer.tenancy_id).data

	def update_ads(self):
		for i in self.list_availability_domain():
			print(i)
			self.availability_domain_list.append(i)

	def get_compartment_name(self, ids):
		return [i.name for i in self.compartments if i.id == ids][0]
			
	def get_compartment_id_list(self):
		return self.compartments
		


if __name__ == "__main__":
	comp = Compartment()
	print(comp.availability_domain_list)