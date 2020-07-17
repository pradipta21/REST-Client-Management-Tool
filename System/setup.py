"""
@author: Pradipta
"""

import os
import sys
from log_module import log,Log_level
from config import Configuration

class Setup:
    
    def __init__(self,root_directory):
        #Setting up the System logs
        self.logger_object_system = log(root_directory,os.path.basename(__file__).replace(".py",""),True)
        self.system_logger = self.logger_object_system.get_system_logger()
        #Setting up Application logs
        self.logger_object_application = log(root_directory,os.path.basename(__file__).replace(".py",""),False)
        self.application_logger = self.logger_object_application.get_application_logger()
        if len(self.application_logger.handlers) < 2:
            self.logger_object_application.add_stream_handler(self.application_logger,Log_level.INFO)
    
    def system_setup(self,root_directory):
        """
            For setting up all the requirements for the application
        """
        required_directories = ["API", "Payload", "Result"]
        self.check_required_directories(root_directory,required_directories)
        try:
            config_obj = Configuration(self.system_logger,root_directory,"configuration.yaml")
            logger_metadata = config_obj.get_logging_data()
            self.check_log_cleanup(logger_metadata["log_max_size"])
            if(logger_metadata["log_console"]):
                self.application_logger.info("Console log is enabled")
            else:
                self.application_logger.warning("Console log is disabled")
            self.application_logger.info("Log Level is configured as " + str(logger_metadata["log_level"]))
            #updating the log level if not set to INFO
            if(logger_metadata["log_level"] != "INFO"):
                for level in Log_level:
                    if(logger_metadata["log_level"] == level.name):
                        self.logger_object_system.update_log_level(self.application_logger,level)
            
            return config_obj
        except Exception as e:
            print("Program exits")
            self.system_logger.error("Error from the Configuration file :\n" + str(e))
            self.application_logger.info("Error in the Configuration file. For for details check the system logs")
                            
    def check_required_directories(self,root_directory,required_directories):
        """
            Checking the required directories and 
            creating the directories if not exists
        """
        for directory in required_directories:        
            if(os.path.exists(root_directory + "/" + directory)):
                self.system_logger.info(directory + " directory exists")
            else:
                self.system_logger.info(directory + " directory not found")
                self.system_logger.info("Creating the " + directory + " directory")
                try:
                    os.mkdir(root_directory + "/" + directory)
                except OSError as e:
                    self.system_logger.error("Not able to create required directories for applications.\n" + str(e))
                    sys.exit(0)
                    
    def check_log_cleanup(self,max_size):
        system_log_size = self.logger_object_system.get_log_size()
        application_log_size = self.logger_object_application.get_log_size()
        if system_log_size >= max_size:
            print("Clean sys")
            print("sys-size : " + str(system_log_size))
            print("Max_size : " + str(max_size))
            self.logger_object_system.clean_log()
        if application_log_size >= max_size:
            self.logger_object_application.clean_log()
    
    def get_system_logger(self):
        return self.system_logger
    
    def get_application_logger(self):
        return self.application_logger

