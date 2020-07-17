"""
@author: Pradipta
"""
import logging
import os
import sys
import enum

class Log_level(enum.Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR

class log:
    
    #system_logger = None
    #application_logger = None
    def __init__(self,root_directory,module_name,system=False):    
        self.base_system_path = root_directory
        self.log_directory = "Log"
        self.system_logger = logging.getLogger(module_name)
        self.check_log_directory()
        self.system = system
        if(system == True):
            self.system_logger.setLevel(logging.DEBUG)
            if not self.system_logger.handlers:
                self.add_file_handler(self.system_logger,"System.log",logging.DEBUG,"a")                
        else:
            self.application_logger = logging.getLogger("Application")
            self.application_logger.setLevel(logging.DEBUG)
            if not self.application_logger.handlers:
                self.add_file_handler(self.application_logger,"Application.log",logging.INFO,"a")
                              
    def add_file_handler(self,logger,logfile,level,mode):
        log_directory_path = self.base_system_path + "/" + self.log_directory + "/" + logfile
        file_handler = logging.FileHandler(log_directory_path,mode)
        file_handler.setLevel(level)
        file_formatter = logging.Formatter('%(asctime)s | %(name)-15s | %(levelname)-8s - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
           
    def add_stream_handler(self,logger,level):
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level.value)
        stream_formatter = logging.Formatter('%(asctime)s : %(name)s : %(levelname)s - %(message)s')
        stream_handler.setFormatter(stream_formatter)
        logger.addHandler(stream_handler)
        
    def update_log_level(self,logger,level):
        for handler in logger.handlers:
            handler.setLevel(level.value)
            
    def get_log_size(self):
        if self.system == True:
            #system logger
            logfile = "System.log"
            log_directory_path = self.base_system_path + "/" + self.log_directory + "/" + logfile
        else:
            #Application
            logfile = "Application.log"
            log_directory_path = self.base_system_path + "/" + self.log_directory + "/" + logfile
        file_stats = os.stat(log_directory_path)
        file_size = file_stats.st_size / (1024 * 1024)   #size in MB
        return file_size
    def clean_log(self):
        if self.system == True:
            #system logger
            logfile = "System.log"
            log_directory_path = self.base_system_path + "/" + self.log_directory + "/" + logfile
        else:
            #Application
            logfile = "Application.log"
            log_directory_path = self.base_system_path + "/" + self.log_directory + "/" + logfile
        try:
            with open(log_directory_path, "w") as f1:
                pass
            self.system_logger.info("Log has been Cleaned up for " + logfile)
        except OSError as err:
            self.system_logger.error("Error occured in cleaning log file : " +str(err))
               
    def check_log_directory(self):
        log_directory_path = self.base_system_path + "/" + self.log_directory
        if(not os.path.exists(log_directory_path)):
            try:
                os.mkdir(log_directory_path)
            except OSError:
                self.system_logger.error(OSError)
                sys.exit(0)
        
    def get_application_logger(self):
        return self.application_logger
        
    def get_system_logger(self):
        return self.system_logger
        