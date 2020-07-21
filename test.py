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
    For more details of the method arguments refer to the README file
"""
#GET Request
RCMT.send(domain_name = "sample_environment",
          url_params = {"post_id" : "1"}, 
          request_name = "demo_GET",
          filename = "GET_RESULT"
          )

#POST Request
RCMT.send(domain_name = "sample_environment", 
          request_name = "demo_POST",
          filename = "POST_RESULT"
          )

"""
    add_api method (used for adding API to the json files in the API directory)
"""
RCMT.add_api(name = "demo_ADD_API",
             endpoint = "/posts/{post_id}",
             method = "PUT",
             header = { "Content-type": "application/json" },
             payload = {"id": 1,
                        "title": 'Vegetables',
                        "body": 'Carrot,Pumpkin',
                        "userId": 1},
             filename = "Sample.json")

"""
    delete_api method (used for deleting API from the json files in the API directory)
"""
#Adding an api for delete demo
delete_api_name = "demo_API_For_delete"
RCMT.add_api(name = delete_api_name,
             endpoint = "/comments",
             method = "GET",
             header = { "Content-type": "application/json" },
             query_params = {"postId":"{post_id}"},
             filename = "Sample.json")
#Deleting the above API
RCMT.delete_api(delete_api_name)

"""
    search_api method (used for searching API in the API directory)
"""
#Getting all the API
print("\n\n\t\tSEARCH RESULT\n")
print("\nAll the avialable APIs\n")
search_result = RCMT.search_api()
print(search_result)

print("\nResult for specific API\n")
#Search specific api
search_result = RCMT.search_api("demo_POST")
print(search_result)

"""
    get_payload method (used for fetching the payload for a specific API)
"""
print("\n\n\t\tPAYLOAD SEARCH RESULT\n")
payload = RCMT.get_payload("demo_POST")
print(payload)