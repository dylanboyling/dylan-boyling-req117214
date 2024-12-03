ISL21 REQ117214 Written Assignment by Dylan Boyling
============

## Setting up the Developer Environment

### Git
Download the latest version of 64-bit Git for Windows [here](https://git-scm.com/downloads/win). Run the file once its downloaded and follow the recommended installation options. 

After installation, set your Git username and email using the following commands:

    git config --global user.name "YOUR_NAME"
    git config --global user.email "YOUR_EMAIL"

Verify Git installed correctly by running:

    git --version

### Python 
Download Python 3.1.0 [here](https://www.python.org/downloads/). Run the file once its downloaded, check the box to add python to your PATH, and follow the recommended installation options.

Verify Python installed correctly by running:

    python --version

### VSCode
Download the latest version of VSCode for your operating system [here](https://code.visualstudio.com/download). Run the file once its downloaded and follow the recommended installation options. 

After installation, open VSCode and press Ctrl+Shift+X to open the extensions tab and install the following extensions:

* Python
* Pylance
* Python Debugger
* isort
* Git Graph
* GitLens

### Cloning the Repository
Open your terminal, ensure you are in your projects folder, and clone the repository from GitHub:

    git clone https://github.com/dylanboyling/dylan-boyling-req117214.git
    cd dylan-boyling-req117214

### Setting up a Virtual Environment
Activate your python virtual environment:

    python -m venv venv
    venv\Scripts\activate

Install required dependencies:

    python install -r requirements.txt

## Starting the Rules Engine
Before starting the rules engine, we need to ensure the MQTT topic ID in the config is using the correct one from our web app instance. 

Open your browser and navigate to the [Winter Supplement Calculator](https://winter-supplement-app-d690e5-tools.apps.silver.devops.gov.bc.ca/)

Copy the MQTT topic ID, open config.py, and update the TOPIC_ID constant with your unique topic ID.

Start the rules engine by running:

    python main.py

Now that the rules engine is running, try filling out the form on the Winter Supplement Calculator and then clicking 'Submit'. Once the rules engine has processed your request, you should see the web app update with the results of your request. 

## Running Unit Tests

