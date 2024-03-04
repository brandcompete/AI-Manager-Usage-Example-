import json
from typing import List
from brandcompete.core.credentials import TokenCredential
from brandcompete.core.classes import Loader
from brandcompete.client import AI_ManServiceClient
from brandcompete.client._ai_man_client import AI_Model
from pathlib import Path

def main():

    #1. Reading config.json values
    config_path: str = f"{Path(__file__).parent}/config/config.json"
    config_content = None
    with open(f"{config_path}", "r") as jsonfile:
            config_content = json.load(jsonfile)        
    
    url = config_content["api_url"]
    username = config_content["user_name"]
    pw = config_content["password"]

    #2. Authorize and AI_ManServiceClient initiation
    token_credential:TokenCredential = TokenCredential(api_host_url=url, user_name=username, password=pw)

    print(token_credential.access)
    client = AI_ManServiceClient(credential=token_credential)

    #3. Fetch and print all available models. 
    models:List[AI_Model] = client.get_models()
    for model in models:
        print(f"- [ID:{model.id:2}] {model.name.upper():25} - {model.shortDescription}")
      
    
    #4. Query the API
    #4.1 Simple query
    result = client.prompt(model_id=1,query="Please tell me the name of the current president of the usa" )
    print(f"result for 4.1: {result['ResponseText']}")
    
    #4.2 Query and append file content to query
    result = client.prompt(model_id=1, query="From the given CSV file, how many rows are there?", loader=Loader.CSV, file_append_to_query='./data/example_customers.csv' )
    print(f"result for 4.2: {result['ResponseText']}")

    #4.3 Query and append file content to query, ragging files
    result = client.prompt(
         model_id=1, 
         query="From the given excel sheet content, please give me the value of the column named 'first name' and 'last name' where the column 'id' has the value 8.",
         loader=Loader.EXCEL, 
         file_append_to_query='./data/example_customers.xlsx', 
         files_to_rag=["./data/example_customers.xlsx"] )
    print(f"result for 4.3: {result['ResponseText']}")

    #4.4 Query with ragging files only 
    result = client.prompt(
         model_id=1, 
         query="From the given excel sheet content, please give me the value of the column named 'first name' and 'last name' where the column 'id' has the value 10.", 
         loader=Loader.EXCEL, 
         files_to_rag=["./data/example_customers.xlsx"] )
    print(f"result for 4.4: {result['ResponseText']}")

if __name__ == "__main__":
    main()