# brandcompete AI-Manager-Usage-Example
This is a small test project to test the AI Manager Python SDK. 
At the same time, the use of the SDK is shown as it can take place in another project.

The AI Manager Python SDK can found [here](https://github.com/brandcompete/AI-Manager-Python-SDK.git)

## Preconditions

Python version: >=3.8.1,<3.12

## Get Started

### Download or clone this example project

```
cd /path/to/projects
git clone https://github.com/brandcompete/AI-Manager-Usage-Example.git
```

### Create your python environment
It is recommended to create a new Phython environment within the project. The .venv folder is ignored in git.

```
python -m venv .venv
```
### Install requirements
You can install the SDK via pip
```
pip install -e git+https://github.com/brandcompete/AI-Manager-Python-SDK.git#egg=AI-Manager-Python-SDK
```

or install dependencies with the requirements.txt file
```
pip install -r requirements.txt
```

### Local config / Credentials
1) Open the config folder ```cd config```
1) Copy config.template.json to config.json ```cp -p config.template.json config.json```
2) Fill out 'api_url', 'user_name' and 'password' in config.json

### Run main.py

