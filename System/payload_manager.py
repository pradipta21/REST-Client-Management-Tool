"""
@author: Pradipta
"""

import json
import os
from log_module import log

class PayloadManager:
    
    def __init__(self,root_directory,payload_path,application_logger):
        self.root_directory = root_directory
        self.payload_path = self.root_directory + "/" + payload_path
        self.application_logger = application_logger
        self.logger_object_system = log(root_directory,os.path.basename(__file__).replace(".py",""),True)
        self.system_logger = self.logger_object_system.get_system_logger()
    
    def check_payload(self,request_detail):
        if "payload" in request_detail.keys():
            if isinstance(request_detail["payload"],dict):
                request_detail["payload_type"] = "data"
            else:
                request_detail["payload_type"] = "file"
        else:
           request_detail["payload"] = None
           request_detail["payload_type"] = "empty"
        return request_detail
        
    
    def get_payload(self,request_detail):
        if(request_detail["payload_type"] == "file"):
            payload_file_path = self.payload_path + "/" + request_detail["payload"]
            if(os.path.exists(payload_file_path)):
                try:
                    with open(payload_file_path,"r") as file:
                        payload_json = json.load(file)
                    request_detail["payload"] = payload_json
                except IOError as err:
                    self.system_logger.error("Error occured while fetching payload file " + str(err))
                except Exception as err:
                    self.system_logger.error("Error occured while fetching payload file " + str(err))
            else:
                self.application_logger.error("Payload file not found in the Payload Directory")
        return request_detail
        
    def search_payload_for_api(self,filename):
        payload_filepath = self.payload_path + "/" + filename
        if(os.path.exists(payload_filepath)):
            try:
                with open(payload_filepath,"r") as file:
                    payload_json = json.load(file)
                    return payload_json
            except IOError as err:
                self.system_logger.error("Error occured while fetching payload file " + str(err))
        else:
            return None
            