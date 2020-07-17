"""
@author: Pradipta
"""
import os
import json
import hashlib
from log_module import log

class APIManger:
    
    def __init__(self,root_directory,api_dir,system_dir,system_information_filename,application_logger):
        self.root_directory = root_directory
        self.api_path = self.root_directory + "/" + api_dir
        self.system_metadata_file_path = self.root_directory + "/" + system_dir + "/" + system_information_filename
        self.logger_object_system = log(root_directory,os.path.basename(__file__).replace(".py",""),True)
        self.system_logger = self.logger_object_system.get_system_logger()
        self.application_logger = application_logger
        self.check_metadata_file()
    
    def extract_json_file(self):
        try:
            if(os.path.isdir(self.api_path)):
                #Filtering out only json file and ignoring other files
                json_file_list = list(filter(lambda file:file.endswith('.json'),os.listdir(self.api_path)))
                try:
                    system_metadata_data = {}
                    with open(self.system_metadata_file_path,"r") as file:
                        system_metadata_data = json.load(file)
                        
                    if len(system_metadata_data["filenames"])>0:
                        hash_digest_list = system_metadata_data["hash_list"]
                        filename_list = system_metadata_data["filenames"]
                        for files in filename_list:
                            if files not in json_file_list:
                                system_metadata_data = self.remove_record(system_metadata_data,files)
                                self.system_logger.info(files + " has been removed and cleaned")
                                self.application_logger.warning(files + " is not avialable anymore")
                    else:
                        self.system_logger.info("System metadata information doesnot have any files")
                        hash_digest_list = []
                        filename_list = []
                        
                    for json_file in json_file_list:
                        #calculating size of the file
                        json_filepath = self.api_path + "/" + json_file
                        file_stats = os.stat(json_filepath)
                        file_size = file_stats.st_size / (1024 * 1024)   #size in MB
                        with open(json_filepath,"rb") as file:
                            hash_read = file.read()
                            
                        #For already existing file
                        if json_file in system_metadata_data["filenames"]:
                            if file_size == system_metadata_data["api_files"][json_file]["file_size"]:
                                system_metadata_data["api_files"][json_file]["activity"] = "no_change"
                                self.application_logger.info(json_file + " is available")
                            else:
                                readable_hash = hashlib.md5(hash_read).hexdigest();
                                hash_digest_list.remove(system_metadata_data["api_files"][json_file]["checksum"])
                                system_metadata_data["api_files"][json_file]["checksum"] = readable_hash
                                system_metadata_data["api_files"][json_file]["activity"] = "updated"
                                system_metadata_data["api_files"][json_file]["file_size"] = file_size
                                hash_digest_list.append(readable_hash)
                                self.application_logger.info(json_file + " is modified")
                        else:
                            #For a file with new name
                            self.application_logger.info("A new file is detected : " + json_file)
                            readable_hash = hashlib.md5(hash_read).hexdigest();
                            if readable_hash in hash_digest_list:
                                self.application_logger.info(json_file + " is found to be a duplicate file" )
                                self.duplicate_file_handler(json_file)
                            else:
                                #Adding metadata
                                self.application_logger.info("New file has been added")
                                system_metadata_data["api_files"][json_file] = {}
                                system_metadata_data["api_files"][json_file]["file_size"] = file_size 
                                system_metadata_data["api_files"][json_file]["checksum"] = readable_hash
                                system_metadata_data["api_files"][json_file]["activity"] = "newly_added"
                                hash_digest_list.append(readable_hash)
                                filename_list.append(json_file)                       
                        
                    if(len(json_file_list) < 1):
                        self.application_logger.info("No JSON files founds in the API directory")
                        system_metadata_data = self.generate_template()
                    else:
                        system_metadata_data["count"] = len(filename_list)
                        system_metadata_data["filenames"] = filename_list
                        system_metadata_data["hash_list"] = hash_digest_list
                    #Dumping in the JSON file
                    with open(self.system_metadata_file_path,"w") as file:
                        json.dump(system_metadata_data,file)
                        
                except Exception as err:
                    self.system_logger.error("Error occured " + str(err))      
        except OSError as err:
            self.system_logger.error("Error occured " + str(err))
        
    def check_metadata_file(self):
        try:
            if not os.path.isfile(self.system_metadata_file_path):
                self.system_logger.info("System information file not found, creating the file from template")
                system_metadata_dict = self.generate_template() 
                with open(self.system_metadata_file_path,"w") as system_metadata:
                    json.dump(system_metadata_dict, system_metadata)
                self.system_logger.info("System information file has been created")
        except OSError as err:
            self.system_logger.error("Error in system information file " + str(err))
            
    def duplicate_file_handler(self,file):
        duplicate_dir_path = self.api_path + "/Duplicate"
        #Directory checking
        try:
            if(not os.path.exists(duplicate_dir_path)):
                self.system_logger.debug("Duplicate directory is not found")
                os.mkdir(duplicate_dir_path)
                self.system_logger.inf("Duplicate directory is created")
            #Moving the duplicate files
            os.rename(self.api_path+"/"+file, duplicate_dir_path+"/"+file)
            self.application_logger.info(file + " file is tagged as duplicate and can be found in duplicate directory")
        except OSError:
            self.system_logger.error("Error occured in handling duplicate file" + str(OSError))
            
    def extract_endpoints(self):
        #Scan all the files and fetch the endpoints
        try:
            with open(self.system_metadata_file_path,"r") as file:
                system_metadata_data = json.load(file)
            self.system_logger.info("Extracting endpoints")
            filename_list = system_metadata_data["filenames"]
            for files in filename_list:
                json_filepath = self.api_path + "/" + files
                with open(json_filepath,"r") as api_file:
                    api_file_json = json.load(api_file)
                system_metadata_data["api_files"][files]["endpoints"] = (list(api_file_json.keys()))
            #Dumping in the JSON file
            with open(self.system_metadata_file_path,"w") as file:
                json.dump(system_metadata_data,file)
            self.system_logger.info("Endpoints are added successfully")
        except IOError as err:
            self.system_logger.error("Error in endpoint extraction " + str(err))
            
    def get_endpont_mapping(self):
        #This will generate the mappping for the endpint and returns as a dictionary
        try:
            with open(self.system_metadata_file_path,"r") as file:
                system_metadata_data = json.load(file)
                
            if(len(list(system_metadata_data["api_files"].keys())) < 1):
                self.system_logger.warning("No API files found for generating endpoint mapping")
                return False
            self.system_logger.info("Generating endpoint mapping")
            enpoint_mapping = {}
            #iterating through all the api files
            for api_files in system_metadata_data["api_files"]:
                for endpoint in system_metadata_data["api_files"][api_files]["endpoints"]:
                    enpoint_mapping[endpoint] = api_files
            self.system_logger.info("Endpoint mapping generated successfully")
            return enpoint_mapping
        except IOError as err:
            self.system_logger.error("Error in fetching endpoint mapping " + str(err))
            
    def add_new_api(self,name,endpoint,method,header,payload,query_params,SSL_verify,timeout):
        api_add = {}
        api_add["endpoint"] = endpoint
        api_add["method"] = method
        api_add["header"] = header
        api_add["payload"] = payload
        api_add["query_params"] = query_params
        api_add["SSL_verify"] = SSL_verify
        api_add["timeout"] = timeout
        self.system_logger.info("JSON object created for add request")
        return api_add
        
    def add_api_in_file(self,api_object,name,filename):
        add_json_object = {}
        try:
            if filename is None:
                self.application_logger.info("No filename is provided, API will be saved as default")
                default_filepath = self.api_path + "/" + "Default.json"
                if(os.path.exists(default_filepath)):
                    with open(default_filepath,"r") as file:
                        add_json_object = json.load(file)
                add_json_object[name] = api_object
                with open(default_filepath,"w") as file:
                    json.dump(add_json_object,file,indent=4)
                self.application_logger.info("API will be saved in Default.json file")
            else:
                user_filepath = self.api_path + "/" + filename
                if(os.path.exists(user_filepath)):
                    with open(user_filepath,"r") as file:
                        add_json_object = json.load(file)
                else:
                    self.application_logger.debug(filename + " not found and will be created newly")
                add_json_object[name] = api_object
                with open(user_filepath,"w") as file:
                    json.dump(add_json_object,file,indent=4)
                self.application_logger.info("API added to " + filename)
        except IOError as err:
            self.application_logger.error("Unable to add the new API")
            self.system_logger.error("Error in Adding new API " + str(err))
            
    def get_api_payload(self,api_name,filename):
        try:
            filepath = self.api_path + "/" + filename
            with open(filepath,"r") as file:
                api_json_object = json.load(file)
            if not "payload" in api_json_object[api_name].keys():
                self.application_logger.debug("Payload is not available for the " + api_name + " API")
                return None
            if api_json_object[api_name]["payload"] == None:
                self.application_logger.debug("Payload is not available for the " + api_name + " API")
                return None
            return api_json_object[api_name]["payload"]
        except IOError as err:
            self.application_logger.error("Unable to get the payload details from the API file")
            self.system_logger.error("Error in while trying to get payload details for the API " + api_name + " from " + filename + " :" + str(err))
    
    def fetch_api(self,api_name,filename):
        try:
            filepath = self.api_path + "/" + filename
            with open(filepath,"r") as file:
                api_json_object = json.load(file)
            api_json_object[api_name]["path"] = filepath
            return api_json_object[api_name]
        except IOError as err:
            self.application_logger.error("Unable to get the API details")
            self.system_logger.error("Error occured while trying to details for the API " + api_name + " from " + filename + " :" + str(err))
    
    def fetch_api_from_file(self,filename):
        try:
            with open(self.system_metadata_file_path,"r") as file:
                system_metadata_data = json.load(file)
            if filename in system_metadata_data["filenames"]:
                try:
                    filepath = self.api_path + "/" + filename
                    with open(filepath,"r") as file:
                        api_json_object = json.load(file)
                    api_json_object["path"] = filepath
                    return api_json_object
                except IOError as err:
                    self.application_logger.error("Unable to get the API details")
                    self.system_logger.error("Error occured while trying to get the details for the APIs from " + filename + " :" + str(err))
            else:
                return None
        except Exception as err:
            self.system_logger.error("Error occured while trying to get all the api from the file " + filename + " :\n " + str(err))
    
    def fetch_all_api(self):
        try:
            with open(self.system_metadata_file_path,"r") as file:
                system_metadata_data = json.load(file)
            result = {}
            for files in system_metadata_data["filenames"]:
                result[files] = {}
                try:
                    filepath = self.api_path + "/" + files
                    with open(filepath,"r") as file:
                        api_json_object = json.load(file)
                    result[files] = api_json_object
                    result[files]["path"] = filepath
                except IOError as err:
                    self.application_logger.error("Unable to get the API details")
                    self.system_logger.error("Error occured while trying to get the details for the APIs from " + files + " :" + str(err))
            return result
        except Exception as err:
            self.system_logger.error("Error occured while trying to get all the api from the file :\n " + str(err))
        
    def delete_api(self,api_name,filename):
        try:
            filepath = self.api_path + "/" + filename
            with open(filepath,"r") as file:
                delete_json_object = json.load(file)
            del delete_json_object[api_name]
            with open(filepath,"w") as file:
                json.dump(delete_json_object,file,indent=4)
            self.application_logger.info(api_name + " API deleted successfully")
        except IOError as err:
            self.application_logger.error("Unable to delete the API " + api_name + " from " + filename)
            self.system_logger.error("Error in deleting the API " + api_name + " from " + filename + " :" + str(err))
        
        
    def generate_template(self):
        system_metadata_dict = {}
        system_metadata_dict["api_files"] = {}
        system_metadata_dict["count"] = 0
        system_metadata_dict["filenames"] = []
        system_metadata_dict["hash_list"] = []
        return system_metadata_dict
    
    def remove_record(self,system_metadata_data,file):
        "For removing the record of a file from the metadata"
        system_metadata_data["count"] -= 1
        system_metadata_data["filenames"].remove(file)
        system_metadata_data["hash_list"].remove(system_metadata_data["api_files"][file]["checksum"])
        del system_metadata_data["api_files"][file]
        return system_metadata_data
            
    def cleanup(self,cleanup_files = []):
        #This method is used for cleaning up deleted API's  
        try:
            self.system_logger.info("Clean up is started")
            with open(self.system_metadata_file_path,"r") as file:
                 system_metadata_data = json.load(file)
            for files in system_metadata_data["api_files"].keys():
                if not files in system_metadata_data["filenames"]:
                    cleanup_files.append(files)
            self.system_logger.warning("This list " + str(cleanup_files) + " will be cleaned up")
            #Cleaning files from the list
            for files in cleanup_files:
                del system_metadata_data["api_files"][files]
            
            with open(self.system_metadata_file_path,"w") as file:
                json.dump(system_metadata_data,file)
            self.system_logger.info("Clean up process has been completed successfully")
        except Exception:
            self.system_logger.error("Error in cleanup process " +str(Exception))
        