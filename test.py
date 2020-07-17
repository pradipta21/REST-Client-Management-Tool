"""
@author: Pradipta
"""

"""
    This is a demo python application to demostrate the usage of RESTClientManagementTool
    with different use-case.Currently this tool supports 5 methods. The below use cases will
    demostrate the use of all five methods.
"""

#Import the application (RESTClientManagementTool)
import RESTClientManagementTool as RCMT

"""
    Send method (For sending any request)
    For details of the method arguments refers to the README file
"""
'''
#GET Request
RCMT.send(domain_name = "sample_environment",
          url_params = {"post_id" : "1"}, 
          request_name = "demo_GET",
          filename = "GET_RESULT"
          )
'''
#POST Request
RCMT.send(domain_name = "sample_environment", 
          request_name = "demo_POST",
          filename = "POST_RESULT"
          )
