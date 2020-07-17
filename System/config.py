"""
@author: Pradipta
"""

import yaml
import os
import RCMT_exception

        
class Configuration:
    
    def __init__(self,logger,root_directory,configuration_filename=None):
        try:         
            self.logger = logger
            self.logger.info("Initialization the Configuration Module")
            self.propertiesList = []
            self.configuration_filename = configuration_filename
            self.base_system_path = root_directory
            configuration_file_path = self.base_system_path + "/" + configuration_filename
            
            if(configuration_filename != None):
                self.read_from_configuration_file(configuration_file_path)
            else:
                print("Configuration filename is not provided!!")
        
        except Exception:
            self.logger.warning("Configuration filename doesnot seem to valid or may not exist")
            self.create_configuration_file()
            
    def create_configuration_file(self):
        """
            Creates a default configuration file 
            if the configuration.yaml file is not found.
        """
        self.logger.info("Creating the default configuration file")
        default_configuration_filename = "configuration.yaml"
        default_configuration_filepath = self.base_system_path + "/" + default_configuration_filename
        if(os.path.exists(default_configuration_filepath)):
            self.logger.debug("Default configuration file found to be already exists")
            self.logger.info("Default configuration file creation process aborted")
        else:
            try:
                with open(default_configuration_filepath,"w") as default_configuration_file_pointer:
                    content_config_dict = {}
                    content_config_dict["domain"]={}
                    content_config_dict["log"]={}
                    content_config_dict["domain"]["test1"]={}
                    content_config_dict["domain"]["test1"]["host"]="127.0.0.1"
                    content_config_dict["domain"]["test1"]["port"]=8080
                    content_config_dict["domain"]["test1"]["https"]=False
                    content_config_dict["log"]["log_level"]="INFO"
                    content_config_dict["log"]["log_console"]=True
                    content_config_dict["log"]["log_max_size"]=100
                    yaml.dump(content_config_dict,default_configuration_file_pointer)
            except IOError:
                self.logger.error(str(IOError))
                
    def read_from_configuration_file(self,configuration_file_path):
        self.logger.info("Reading from "+str(configuration_file_path))
        try:
            with open(configuration_file_path,"r") as file:
                configuration_dict = yaml.load_all(file, Loader=yaml.FullLoader)
                for doc in configuration_dict:
                    self.propertiesList = list(doc.keys())
                    for key,value in doc.items():
                        if key == "domain":
                            self.domains = value
                        if key == "log":
                            self.log = value
        except Exception as e:
            self.logger.error("Failed to read the configuration file : \n" +str(e))
            raise(RCMT_exception.yamlScannerError("While trying to read configuration file"))
        
    def get_domain_metadata(self):
        """
            Generates the metadata for the domains
            available in the configuration file
        """
        self.logger.info("Generating Domain metadata")
        domain_metadata = {}
        domain_metadata["names"] = list(self.domains.keys())
        domain_metadata["count"] = len(list(self.domains.keys()))
        domain_metadata["totalValid"] = 0
        for domain,attribute in self.domains.items():
            if "host" in attribute.keys():
                if attribute["host"] is not None:
                    attribute["valid"]=True
                    domain_metadata["totalValid"] += 1
                else:
                    attribute["remark"]="Host is empty"
                    attribute["valid"]=False
                    continue
            else:
                attribute["valid"]=False
                attribute["remark"]="Host is missing"
                continue
            
            if "https" not in attribute.keys():
                attribute["https"]=False
                
            if "port" not in attribute.keys():
                attribute["port"]=None
                
        domain_metadata["values"] = self.domains
        return domain_metadata
    
    def get_logging_data(self):
        logging_metadata = {}
        logging_level = ["INFO","WARNING","DEBUG","ERROR"]
        logging_metadata["properties"] = self.log.keys()
        logging_metadata["count"] = len(self.log.keys())
        if "log_level" in self.log.keys():
            if self.log["log_level"].upper() in logging_level:
                logging_metadata["log_level"] = self.log["log_level"].upper()
            else:
                logging_metadata["log_level"] = "INFO"
        else:
            logging_metadata["log_level"] = "INFO"
            
        if "log_console" in self.log.keys():
            logging_metadata["log_console"] = self.log["log_console"]
        else:
            logging_metadata["log_console"] = True
            
        if "max_log_size" in self.log.keys():
            logging_metadata["log_max_size"] = self.log["log_max_size"]
        else:
            logging_metadata["log_max_size"] = 100
        return logging_metadata
#config_obj.create_configuration_file()