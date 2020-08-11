"""
@author: Pradipta
"""

import os
import json
import re
import requests
from requests.exceptions import HTTPError
from log_module import log
import RCMT_exception

class RequestManager:
    
    def __init__(self,root_directory,api_dir,endpint_map,application_logger):
        self.root_directory = root_directory
        self.api_dir_path = self.root_directory + "/" + api_dir
        self.endpint_map = endpint_map
        self.application_logger = application_logger
        self.logger_object_system = log(root_directory,os.path.basename(__file__).replace(".py",""),True)
        self.system_logger = self.logger_object_system.get_system_logger()
    
    def get_request_details(self,request_name):
        try:
            self.system_logger.info("Fetching API request details")
            api_file_path = self.api_dir_path + "/" + str(self.endpint_map[request_name])
            with open(api_file_path,"r") as file:
                api_files_json = json.load(file)
            request_details = api_files_json[request_name]
            return request_details
        except IOError as err:
            self.system_logger.error("Error in getting request details " + str(err))
            return None
        except KeyError as err:
            self.system_logger.error("Key not found while fetching request details\nKEY : " + str(err))
            return None
        
    def header_assemble(self,request_details,header):
        self.application_logger.info("Setting up the header")
        if isinstance(header,dict):
            header_key = header.keys()
            for key in header_key:
                request_details["header"][key] = header[key]
            return request_details
        else:
            raise RCMT_exception.argumentDataTypeError("Header argument must be of dict type")
            
    def payload_assembe(self,request_details,payload):
        if request_details["payload_type"] == "empty":
            request_details["payload"] = {}
        if isinstance(payload,dict):
            payload_key = payload.keys()
            for key in payload_key:
                request_details["payload"][key] = payload[key]
            return request_details
        else:
            raise RCMT_exception.argumentDataTypeError("Payload argument must be of dict type")
    
    def query_params_assembe(self,request_details,query_param):
        self.application_logger.info("Setting up the query params for the URL")
        request_details["query_params"] = {}
        if isinstance(query_param,dict):
            payload_key = query_param.keys()
            for key in payload_key:
                request_details["query_params"][key] = query_param[key]
            return request_details
        else:
            raise RCMT_exception.argumentDataTypeError("Query Params argument must be of dict type")
        
    def request_url_assemble(self,domain_details,request_details,request_name,url_params):
        self.application_logger.info("Assembling the request URL")
        #Domain
        if domain_details["port"] != None:
            api_domain = domain_details["host"] + ":" + str(domain_details["port"])
        else:
            api_domain = domain_details["host"]
        
        #Endpoint
        api_endpoint = request_details["endpoint"]
        params_list = re.findall(r"\{(\w+)\}",request_details["endpoint"])
        if len(params_list)>0:
            self.application_logger.info("Adding URL parameters")
            for params in params_list:
                api_endpoint = api_endpoint.replace("{"+params+"}",url_params[params])
                self.application_logger.info(params + " : " + url_params[params])
        else:
            self.application_logger.info("No parameters found in the url")
        if api_endpoint[0] == '/':
            api_endpoint = api_endpoint[1:]
        if api_endpoint[-1] == '/':
            api_endpoint = api_endpoint[:-1]
        #Https checking
        if not api_domain.startswith("http"):
            if domain_details["https"]:
                api_domain = "https://" + api_domain
                self.application_logger.info("Connection is secured")
            else:
                api_domain = "http://" + api_domain
                self.application_logger.warning("Connection is not secure")
        request_url = api_domain + "/" + api_endpoint
        request_details["url"] = request_url
        return request_details
    
    def send_request(self,request_details,auth):
        #Method for sending requests
        request_url = request_details["url"]
        headers = request_details["header"]
        method = request_details["method"]
        payload = request_details["payload"]
        query_params = request_details["query_params"]
        timeout = request_details["timeout"]
        SSL_verify = None
        if "SSL_verify" in request_details.keys():
            if request_details["SSL_verify"] != None:
                SSL_verify =  request_details["SSL_verify"]
        
        try:
            response = requests.request(
                    method,
                    request_url,
                    json = payload,
                    headers=headers,
                    params=query_params,
                    timeout=timeout,
                    verify=SSL_verify,
                    auth=auth
                )
            
            self.application_logger.info("*********   REQUEST INFORMATION   *********")
            self.application_logger.info("Request URL : " + str(response.url))
            self.application_logger.info("Method : " + str(method))
            self.application_logger.info("Header : \n" + json.dumps(headers, indent=4))
            if payload != None:
                self.application_logger.info("Payload : \n" + json.dumps(payload, indent=4))
            self.application_logger.info("Request Timout : " + str(timeout))
            self.application_logger.info("SSL Verification : " + str(SSL_verify))
            
            self.application_logger.info("*********   RESPONSE INFORMATION   *********")
            if response.status_code >= 200 and response.status_code < 300:
                self.application_logger.info("Success")
                self.application_logger.info("Response Code : " + str(response.status_code))
            elif response.status_code >= 300 and response.status_code < 400:
                self.application_logger.info("Redirection")
                self.application_logger.info("Response Code : " + str(response.status_code))
            elif response.status_code >= 400 and response.status_code < 500:
                self.application_logger.info("Client Error")
                self.application_logger.info("Response Code : " + str(response.status_code))
            else:
                self.application_logger.info("Server Error")
                self.application_logger.info("Response Code : " + str(response.status_code))
            json_formatted_str = json.dumps(json.loads(response.text), indent=4)
            self.application_logger.info("Response Text : \n" + json_formatted_str)
            return response
        except HTTPError as err:
            self.application_logger.error("Error in Sending Requests " + str(err))
        except Exception as err:
            self.application_logger.error("Error in Sending Requests " + str(err))
            
    def save_result(self,response,filename):
        self.application_logger.info("Result will be saved as JSON file")
        filename = filename + ".json"
        filepath = "Result/" + filename
        try:
            print("Response text : " + response.text)
            response_body = json.loads(response.text)
            with open(filepath,"w") as file:
                json.dump(response_body,file)
            self.application_logger.info(filename + " is saved successfully in the Result Directory")
        except IOError as err:
            self.system_logger.error("Error occured while saving result " + str(err))
        except Exception as err:
            self.application_logger.error("Error occured while saving result " + str(err))