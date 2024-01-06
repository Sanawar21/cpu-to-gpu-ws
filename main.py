"""
Setup: The cpu client will connect to the websocket host and let it know its a 
       cpu and upload files in a json format and then disconnect
       once a successfully uploaded message containing the session id is 
       received from the server.
       The gpu client will then connect to the websocket host and let it know its a
       gpu and download the uploaded files with the session ID then send a delete
       message to the websocket to delete the files then disconnect. 
"""
