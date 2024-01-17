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
    token_credential = TokenCredential(api_host_url=url, user_name=username, password=pw)
    client = AI_ManServiceClient(credential=token_credential)

    #3. Fetch and print all available models. 
    models:List[AI_Model] = client.get_models()
    for model in models:
        print(f"- [ID:{model.id:2}] {model.name.upper():25} - {model.shortDescription}")
    
    #4. Query the API
    send_simple_text_query(client=client, model_id=2)
    send_query_with_file_content(client=client, model_id=2)

def send_simple_text_query(client:AI_ManServiceClient, model_id:int = 1) -> None:

    query="What is the name of the current president of the united state of america?"
    result = client.prompt(model_id=model_id,query=query )
    print(f"Query: {query}")
    print(f"Answere: {result}")

def send_query_with_file_content(client:AI_ManServiceClient, model_id:int = 1) -> None:

    query="what is the sum of the ages of all entries"
    result = client.prompt(model_id=model_id,query=query, loader=Loader.EXCEL, file_path='./data/example.xlsx' )
    print(f"Query: {query}")
    print(f"Answere: {result}")

if __name__ == "__main__":
    main()