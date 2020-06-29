from oci.core import ComputeClient
from oci.exceptions import ServiceError
from oci.pagination import list_call_get_all_results
import sys
import Config
import logging
import logs

class Instance:
    def __init__(self):
        config = {}
        try:
            signer = Config.signer
            self.compute_client = ComputeClient(config=config, signer=signer)
        except Exception:
            config = Config.config
            self.compute_client = ComputeClient(config)
        
        

    # Request to list all volume attachments
    def list_volume_attachments(self, compartment_id):
        try:
            return list_call_get_all_results(self.compute_client.list_volume_attachments,
                                             compartment_id).data
        except ServiceError as identifier:
            logging.error(identifier+" "+compartment_id)
            # logger.error(identifier.message)
            exit()


    def get_instance_details(self, instance_id):
        try:
            instance_data = self.compute_client.get_instance(instance_id).data
        except Exception as e:
            if(e.status == 404):
                logging.error(f"Instance Id {instance_id} is incorrect; Status: 404")
                # logger.error(f"Instance Id {instance_id} is incorrect; Status: 404")
            else:
                logging.error(f"Not authorized for {instance_id}; Status: {str(e.status)}")
                # logger.error(f"Not authorized for {instance_id}; Status: {str(e.status)}")

            raise
        return instance_data

    # gets the instance tag and caches the instance tags to reduce number of request


