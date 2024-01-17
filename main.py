from typing import List
from brandcompete.core.credentials import TokenCredential
from brandcompete.core.classes import Loader
from brandcompete.client import AI_ManServiceClient
from brandcompete.client._ai_man_client import AI_Model

#access_token = token_credential.get_token("host","username","pass" 

def main():
    url = "https://aiman-api-test.brandcompete.com"
    username = "thorsten.atzeni@brandcompete.com"
    pw = "thorsten.atzeni@brandcompete.com42"

    token_credential = TokenCredential(api_host_url=url, user_name=username, password=pw)
    client = AI_ManServiceClient(credential=token_credential)

    models:List[AI_Model] = client.get_models()
    for model in models:
        #print(f"- [ID:{model.id:2}] {model.name.upper():25} - {model.shortDescription}")
        pass

    query="Please describe the applicant and her skills"
    #result = client.prompt(model_id=models[1].id,query=query, loader=Loader.EXCEL, file_path='./data/fleet.xlsx' )
    result = client.prompt(model_id=models[0].id,query=query, loader=Loader.PDF, file_path='./data/test_01.pdf' )
    #result = client.prompt(model_id=models[1].id,query=query, loader=Loader.CSV, file_path='./data/test.csv' )
    #result = client.prompt(model_id=models[1].id,query=query, loader=Loader.DOCX, file_path='./data/test.docx.zip' )
    print(f"Query: {query}")
    print(f"Answere: {result}")

if __name__ == "__main__":
    main()