"""
@author: Pradipta
"""
import os
import sys
import json

current_abs_path = os.path.dirname(__file__)
if current_abs_path not in sys.path:
    sys.path.append(current_abs_path)
Setup_path = current_abs_path + "/" + "System"
if(os.path.isdir(Setup_path)):
    if Setup_path not in sys.path:
        sys.path.append(Setup_path)
try:      
    from System.setup import Setup
    from System.api_manager import APIManger
    from System.request_manager import RequestManager
    from System.payload_manager import PayloadManager
    import RCMT_exception
except ImportError:
    sys.exit(0)
#setup
setup = Setup(current_abs_path)
configuration = setup.system_setup(current_abs_path)
domain_metadata = configuration.get_domain_metadata()
application_logger = setup.get_application_logger()
#API object
apiManager = APIManger(current_abs_path,"API","System","system_information.json",application_logger)
apiManager.extract_json_file()
apiManager.extract_endpoints()
apiManager.cleanup()
endpoint_map = apiManager.get_endpont_mapping()
payloadManager = PayloadManager(current_abs_path,"Payload",application_logger)

def send(domain_name,request_name,url_params=None,query_param=None,header=None,payload=None,auth=None,filename=None):
    """
        This method can be used for sending request to the APIs. All the optional arguments are not 
        necessary to use if all the properties are already specified in the API JSON files(Inside API directory)
        
        @Arguments
          domain_name [String][required*] Must be same as given in the API json files (case-sesitive)
          request_name [String][required*] (case-sensitive)
          url_params [dict][optional] if need new params need to be added
          query_param [dict][optional] if need query params need to be added
          header [dict][optional] if new properties in header needs to be added
          payload [dict][optional] if key/value pair in payload needs to be added/updated
          auth [auth object][optional] if have any other authentication, send the auth object
          filename [String][optional] If result needs to save in a file, else leave it as blank
          
        @Returns
          Response object recieved by the API
    """
    
    if domain_name in domain_metadata["names"]:
        domain_details = domain_metadata["values"][domain_name]
        try:
            requestManager = RequestManager(current_abs_path,"API",endpoint_map,application_logger)
            request_details = requestManager.get_request_details(request_name)
            request_details = payloadManager.check_payload(request_details)
            print(request_details)
            if request_details != None:
                #Fetch payload
                if(request_details["payload_type"] == "file"):
                    payloadManager.get_payload(request_details)
                #Merge header
                if(header != None):
                    request_details = requestManager.header_assemble(request_details, header)
                #Merge payload
                if(payload != None):
                    request_details = requestManager.payload_assembe(request_details, payload)
                #Merge query params    
                if(query_param != None):
                    request_details = requestManager.query_params_assembe(request_details, query_param)
                request_details = requestManager.request_url_assemble(domain_details,request_details,request_name,url_params)
                reponse = requestManager.send_request(request_details,auth)
                if filename != None and reponse.text != None:
                    requestManager.save_result(reponse,filename)
                return reponse
            else:
                application_logger.error("Not able to create the Request")
        except Exception as err:
            application_logger.error(str(err))
    else:
        application_logger.error("Domain (" + domain_name + ") is not available in the configuration file")
        
def add_api(name,endpoint,method,header,payload=None,query_params=None,SSL_verify=None,timeout=None,filename=None):
    """
        This method can be used to add new api to any files, if file specified is not already present then
        new file will created and stored the api as json object.Filename is an optional argument so, if 
        filename not provided so API will be added in the Default.json file
        
        @Arguments
          name  [String][required*]  Name of the API.(Must be unique)
          endpoint  [String][required*]  endpoints
          method  [String][required*]   "GET/PUT/POST/DELETE"
          header  [dict][required*]   "headers in the form of a dictionary"
          payload  [dict][required*/optional]   "Required for PUT and POST"
          query_params  [dict][optional]  "query params of the url"
          SSL_verify  [String/boolean][optional]  "SSL path or false for no certificate check"
          timeout  [String][optional]  "timeout value"
          filename  [String][optional]  "filename where API should be added.(Default : Default.json)"
    """
    
    if name in endpoint_map.keys():
        application_logger.error("API already exists with same name as " + name)
    else:
        if(method.upper() == "POST" or method.upper() == "PUT"):
            if(payload == None):
                raise RCMT_exception.apiAddArgumentError("API with method PUT or POST must have paload")
            else:
                if(not isinstance(payload,dict)):
                    raise RCMT_exception.apiAddArgumentError("payload must be of type dict")
        if(not isinstance(header,dict)):
            raise RCMT_exception.apiAddArgumentError("Header must be of type dict")
        if(query_params != None):
            if(not isinstance(query_params,dict)):
                raise RCMT_exception.apiAddArgumentError("query_params must be of type dict")
        api_object = apiManager.add_new_api(name,endpoint,method,header,payload,query_params,SSL_verify,timeout)
        apiManager.add_api_in_file(api_object,name,filename)
        if filename != None:
            endpoint_map[name] = filename
        else:
            endpoint_map[name] = "Default.json"
    
def delete_api(api_name):
    """
        This method can be used to delete any existing API in the API directory
        
        @Arguments
            api_name : Name of the API to be deleted(API must be present in the API directory)
    """
    
    if api_name in endpoint_map.keys():
        apiManager.delete_api(api_name,endpoint_map[api_name])
    else:
        application_logger.error("No API found with the name " + api_name)

def search_api(api_name=None,filename=None):
    """
        This method can be used to search any api or fetch all the api from a file or 
        fetch all the existing api from all the files
        
        
        @Arguments
            api_name : Name of the API to be search 
            filename : Name of the file for which all the api will be fetched.
            
        @Returns
            a json object containing the details of the API.
    """
    
    result = {}
    if api_name != None:
        if api_name in endpoint_map.keys():
            result["api"] = apiManager.fetch_api(api_name,endpoint_map[api_name])
            result["api"]["file"] = endpoint_map[api_name]
        else:
            application_logger.error("No API found with the name " + api_name)        
    
    if filename != None:
        result["file"] = apiManager.fetch_api_from_file(filename)
        if result["file"] == None:
            application_logger.debug("No such file found")
    if api_name == None and filename == None:
        result = apiManager.fetch_all_api()
    return result 

def get_payload(api_name):
    """
        This method can be used to get the api for any API
        
        @Arguments
            api_name : Name of the API to be deleted(API must be present in the API directory)
        return
    """
    
    if api_name in endpoint_map.keys():
        payload = apiManager.get_api_payload(api_name,endpoint_map[api_name])
        if isinstance(payload,dict):
            application_logger.info("Payload : \n" + json.dumps(payload, indent=4))
            return payload
        else:
            if payload != None:
                payload = payloadManager.search_payload_for_api(payload)
                application_logger.info("Payload : \n" + json.dumps(payload, indent=4))
            else:
                application_logger.info("Payload : " + payload)
            return payload
    else:
        application_logger.error("No API found with the name " + api_name)       