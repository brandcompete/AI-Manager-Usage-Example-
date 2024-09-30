import json, traceback
from typing import List
from brandcompete.core.credentials import TokenCredential
from brandcompete.core.classes import Loader, PromptOptions, DataSource
from brandcompete.client import AI_ManServiceClient
from brandcompete.client._ai_man_client import AI_Model
from pathlib import Path

def main():

    #1. Reading config.json values
    root_folder = Path(__file__).parent
    config_path: str = f"{root_folder}/config/config.json"
    config_content = None
    with open(f"{config_path}", "r") as jsonfile:
            config_content = json.load(jsonfile)        
    
    url = config_content["api_url"]
    username = config_content["user_name"]
    pw = config_content["password"]

    #2. Authorize and AI_ManServiceClient initiation
    token_credential:TokenCredential = TokenCredential(api_host_url=url, user_name=username, password=pw)

    #3 Instanciate the client
    client = AI_ManServiceClient(credential=token_credential)
    
    #4 Fetch available list of models
    models:List[AI_Model] = client.get_models()
    for model in models:
        print(f"[default tag:{model.defaultModelTagId:4}] {model.name.upper():25} - {model.shortDescription}")
    
    
    
    #5 Simple Prompt examples
    #5.1 prompt a question
    
    #using the first model (mistral)
    model_to_query: AI_Model = models[0]
    response = client.prompt(
                model_tag=model_to_query.defaultModelTagId, 
                query="Who is the current president of the united states")
    print(f"result for 5.1: {response['ResponseText']}")
    
    #5.2 Query and append file content to query
    result = client.prompt(
         model_tag=model_to_query.defaultModelTagId,  
         query="From the given CSV file, how many rows are there?", 
         loader=Loader.CSV, 
         file_append_to_query=f"{root_folder}/data/example_customers.csv" )
    print(f"result for 5.2: {result['ResponseText']}")
    
    #5.3 Query and append file content to query, ragging files
    result = client.prompt(
         model_tag=model_to_query.defaultModelTagId,
         query="From the given excel sheet content, please give me the value of the column named 'first name' and 'last name' where the column 'id' has the value 8.",
         loader=Loader.EXCEL, 
         file_append_to_query=f"{root_folder}/data/example_customers.xlsx", 
         files_to_rag=[f"{root_folder}/data/example_customers.xlsx"] )
    print(f"result for 5.3: {result['ResponseText']}")
    
    #5.4 Query with ragging files only 
    result = client.prompt(
         model_tag=model_to_query.defaultModelTagId, 
         query="From the given excel sheet content, please give me the value of the column named 'first name' and 'last name' where the column 'id' has the value 10.", 
         loader=Loader.EXCEL, 
         files_to_rag=[f"{root_folder}/data/example_customers.xlsx"] )
    print(f"result for 5.4: {result['ResponseText']}")
    
    
    #6. Prompt options
    #You can pass prompt options as a optional parameter to your prompt
    #(otherwise default values are used)
    
    options = PromptOptions()
    options.keep_context = True,
    options.num_ctx = 8128
    options.raw = True
    options.temperature = 0.4
    options.mirostat = 0
    options.mirostat_eta = 0.1
    options.mirostat_tau = 5
    options.num_gqa = 8
    options.num_gpu = 0
    options.num_thread = 0
    options.repeat_last_n = 64
    options.repeat_penalty = 1.1
    options.seed = 0
    
    #7. Prompting with datasources
    
    #7.1 Fetch all datasources (associated to my account)
    datasources = client.fetch_all_datasources()
    for source in datasources:
        print(f"{source.id}")
        print(f"{source.name}")
        print(f"{source.status}") #2 --> rdy, 1 --> indexing, 0 --> pending
    
    #7.2 Init a new datasource (minimum requirements - name and summary)
    datasource_id = client.init_new_datasource(
        name="Test datasource", 
        summary="New datasource for uploading some documents")
    
    #7.3 Or init a new datasource with a list of tags and categories
    datasource_id = client.init_new_datasource(
        name="Test datasource", 
        summary="New datasource for uploading documents", 
        tags=["tagA","tagB", "etc"], 
        categories=["catA","catB","etc"])
    
    #7.4 Add the new datasource to your account
    client.add_documents(
        data_source_id=datasource_id, 
        sources=[f"{root_folder}/data/fleet_ops_template.xlsx"])
    
    #Add multiple documents to a datasource (can be url or file)
    client.add_documents(
        data_source_id=datasource_id, 
        sources=[f"path/to_my_data/test.pdf", "https://www.brandcompete.com"] )
    
    #7.5. Prompt in conjunction with a datasource id
    response = client.prompt_on_datasource(
        datasource_id=datasource_id,
        model_tag_id=model_to_query.defaultModelTagId,
        query="your ?",
        prompt_options = None)

if __name__ == "__main__":
    main()