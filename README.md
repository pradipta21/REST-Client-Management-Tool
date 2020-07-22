# REST Client Management Tool
This tool can be used for managing the REST APIs with different parameter and can be configured to exceute in multiple environment.All the APIs and its corresponding payload can be organized and exceuted seamlessly with the help of this tool. 
This tools can be used for below scenarios - 
1. Testing a large set of the APIs in different environment.
2. Create Automation using REST API.
3. Quick look up of the API response during UI development.

# Objective
1. To Create a tool for organizing REST APIs.
2. Support multi-environment execution of APIs.
3. Support runtime parameter for the APIs.
4. Provide searching capabilities for the existing APIs.
5. Handling the API operations promatically from the tool itself.

# Installation
## Clone
- Clone this repo to your local machine using : SSH: `git@github.com:pradipta21/REST-Client-Management-Tool.git` or HTTPS: `https://github.com/pradipta21/REST-Client-Management-Tool.git`
## Setup
- Open a python terminal
- Install the requirement.txt file using pip
``` 
pip install -r requirement.text
```
- Execute `RESTClientManagementTool.py` to initialize the tools.
```
python RESTClientManagementTool.py
```
# Features
- APIs are stored in json format.
- All the APIs and Payload can be categorized.
- Same payload can be used for multiple API.
- Add/Delete API can be done programtically.
- API/JSON files can be searched.
- Payload for specific API can be fetched.
- Values of the parameters used in the API can be assigned dynamically.
- Any properties of the API can be overridden during run-time.
- Self-repairing for certain scenarios.
- Logging available in two different levels for better tracking.
- Supports execution in multiple environmnents.
# Documentation
## Configuration
The most important step is to set up configuration file.
- Open the `configuration.yaml` using any text editior.
- Add the details of your environment under `domain` property (Refer to the sample given in the `configuration.yaml`).
- Structure of domains :
  - [Name of your enviroment ]: 
    - host: [String]
    - port: [Integer]
    - https: [Boolean]
- Log configuration will be avialable by default.If you want, you can change it.
- Structure of log :
  - log:
    - log_level: [debug/info/warning]
    - log_console: [Boolean]
    - log_max_size: [Number (calculate size in MB)]
- Once all the configurations are setup, tool will be ready to use. 

## How to Start
- Create a new python file with any name.
- import the tool
```
import RESTClientManagementTool as RCMT
```
- The above import will work for any sub-directory inside the parent directory (for other directories outside the parent directory import the tool using its path).
- Add APIs to the Tools. (for details of adding API check below)
- Add Payload if required. (for details of adding Payload check below)
- Use the supported method as per your requirements.
- Execute your script
## Supported Methods
- **send** : send method can be used for sending request to the APIs.It will return the response in the form of python response object.Even the response can be saved in JSON format if filename is passed in the method arguments. All the saved responses can be found under `Result` directory.
  - **Arguments**:
    - **domain_name**: `[String],[required]` The Domain you have setup in the configuration file (case-sensitive)
    - **request_name**: `[String],[required]` The name of the API you want to use (case-sensitive). The name must in be present in the API json file.
    - **url_params**: `[dict],[optional]` If the API url have some paramerters, then value the pass as key/value pairs. key will the name of the variable and value should contains the actual value.
    - **query_param**: `[dict],[optional]` If the API url supports query string, then this can be used.The value must passs as key/value pair.
    - **header**: `[dict],[optional]` If you want to add additional header properties apart from the available one in the API json file. The dict object passed will be merged with the header object from API json file.
    - **payload**: `[dict],[optional]` If you want to add additional payload properties apart from the available one in the Payload json file. The dict object passed will be merged with the payload object from Payload json file.
    - **auth**: `[auth object],[optional]` If your API need some authentication, then you can pass the authentication object.
    - **filename**: `[String],[optional]` If you want to save the response returned by the API.The response will be stored as json format with the value passed as filename inside the `Result` directory. 
 - **add_api** : add_api method can be used for adding APIs to any JSON file.If filename is not given then, it will add to a default file.
   - **Arguments**:
      - **name**: `[String],[required]` The name of the API which will be used for future reference.
      - **endpoint**:  `[String],[required]` endpoint of the API url.
      - **method**: `[String],[required]` Method of the API.
      - **header**: `[dict],[required]` Header of the API.
      - **payload**: `[dict/String],[required/optional]` Payload of the API if needed(POST/PUT). Payload can be either any json filename in the `Payload Directory` or in the form of a dictionary object for small payloads.
      - **query_param**: `[dict],[optional]` If the API url supports query string, then this can be used.The value must passs as key/value pair.
      - **SSL_verify**: `[String/boolean][optional]` If have have SSL certificate enter the path of the certificate else set it to false.
      - **timeout**: `[String],[optional]` Request timeout value.
      - **filename**: `[String],[optional]` Filename in which API should be added.If no filename is specififed then API will be added to `Default.json`
      
      If API gets added successfully, it will return `True` else `False`
  - **delete_api** : delete_api method can be used delete any API from any json file.
    - **Arguments**:
      - **api_name**: `[String],[required]` Name of the API that will be deleted.
      
      If API gets deleted successfully, it will return `True` else `False`. 
  - **search_api**: search_api method can be used for searching any API from the entire `API directory`
    - **Arguments**:
      - **api_name**: `[String],[optional]` Name of the API that will be searched (Only found API will be returned)
      - **filename**: `[String],[optional]` If filename is given then all the API in that file will be returned.
      
      If both the arguments are set to null, then all the avialable APIs will be returned.The return type will be of json object.If no API are found it will return `None`.
  - **get_payload** : get_payload methods can be used to retrieve the payload of the API which requires the use of payload.
    - **Arguments**:
      - **api_name**: `[String],[required]` The payload of the given API will be returned. 
## How to add API
All the API must be added as json object in a json file.APIs can be added in two ways
- Directly adding API in the json file : Create any json file or open any existing json file from the `API directory`.Add a json object according to the structure given below:
```
[Name of the API]: { 
     "endpoint": "",
     "method": "",
     "header": {
        "Content-Type": "application/json" 
     },
     "payload": "",
     "query_params": null,
     "SSL_verify": null,
     "timeout": null
  }
```

Fill the information properly and save the file.Using the name of the API, this object can be used.
- Adding the API programatically : To add the API from the tool itself, `add_api` method can be used (Refer to supported methods to know how to use add method).
## How to add payload
Adding payload can be quite simple.Create a json file which will contain the entire payload and drop it in the `Payload Directory`.Then update the name of the payload file in the API json object.

**Note** : For small payload, it can be directly added to the API json object while adding API to it.
## Logging
In this tool, logs are divieded into two layer for better tracing of the application.
- System log : All logs related to system processing and configuring can be found here.
- Application log : All logs related to API execution can be found here.
