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
# Configuration
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

# Usage
- Create a new python file with any name.
- import the tool
```
import RESTClientManagementTool as RCMT
```
- The above import will work for any sub-directory inside the parent directory (for other directories outside the parent directory import the tool using its path).
- Now, use the any supported methods by the tool and execute your script.
