ISL21 REQ117214 Written Assignment by Dylan Boyling
============

## Setting up the Developer Environment

### Git
Download the latest version of 64-bit Git for Windows [here](https://git-scm.com/downloads/win). Run the file once it's downloaded and follow the recommended installation options. 

After installation, set your Git username and email using the following commands:

    git config --global user.name "YOUR_NAME"
    git config --global user.email "YOUR_EMAIL"

Verify Git is installed correctly by running:

    git --version

### Python 
Download Python 3.1.0 [here](https://www.python.org/downloads/). Run the file once it's downloaded, check the box to add python to your PATH, and follow the recommended installation options.

Verify Python is installed correctly by running:

    python --version

### VSCode
Download the latest version of VSCode for your operating system [here](https://code.visualstudio.com/download). Run the file once it's downloaded and follow the recommended installation options. 

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
    .\venv\Scripts\activate

Install required dependencies:

    python install -r requirements.txt

## Project Structure
* `client.py`: Wraps MQTT client to encapsulating connection logic, streamline publishing messages, and graceful error handling to prevent crashes.
* `config.py`: Contains configuration variables for connecting to the MQTT broker and topics.
* `constants.py`: Stores business logic constants to use in the rules engine.
* `main.py`: Entry point for the application where the MQTT clients is launched and subscribes to a topic.
* `message_handler.py`: Contains function(s) which handle a request by calling the necessary functions to validate input data, call the appropriate rules engine function, and format the output data before it is published in the client wrapper. 
* `rules_engine.py`: Contains business logic for determining winter supplement eligibility and calculating supplement amounts.
* `validation.py`: Validates incoming input data for the rules engine, this ensures that the rules engine can focus on business logic.
* `tests/`: Contains unit tests for all major components of the project.


## Starting the Rules Engine
Before starting the rules engine, we need to ensure the MQTT topic ID in the config is using the correct one from our web app instance. 

Open your browser and navigate to the [Winter Supplement Calculator](https://winter-supplement-app-d690e5-tools.apps.silver.devops.gov.bc.ca/)

Copy the MQTT topic ID, open config.py, and update the TOPIC_ID constant with your unique topic ID.

Start the rules engine by running:

    python main.py

Now that the rules engine is running, try filling out the form on the Winter Supplement Calculator and then clicking 'Submit'. Once the rules engine has processed your request, you should see the web app update with the results of your request. 

## Running Unit Tests
Run the tests with:

    python -m unittest discover -s tests -p "test_*.py"

Optionally, you can use the coverage dependency to generate a coverage report:

    coverage run --source=. -m unittest discover -s tests -p "test_*.py"
    coverage report

## Approaches, Assumptions, and Design Decisions
### Validation and Logging Strategy
The validation.py file handles any request specific validation (proper data type, proper request format, etc) before passing it to rules_engine.py. rules_engine.py only handles business logic validation in order to ensure a clear separation of concerns.

### Error Handling
Errors encountered during processing are logged, and the application gracefully handles them by returning error messages. For example, if "numberOfChildren" is missing from the request, the program logs the error and then publishes a response in the "error" field without crashing the application. This ensures that the rules engine does not crash due to one malformed request, as stabiltiy is an important component of government software.

### Constants and Encapsulation of Business Logic
Constants, such as base amounts and per-child amounts, are defined in a constants.py. This encapsulates any business logic for easy modification by storing any constants in one location. The rules_engine.py functions were designed to be generic in order to allow the possibility of supporting other supplement programs. Much of the project was designed with this goal in mind. I would initially focus on funtionality at first, and then went back to refactor my code with the intention of decoupling the idea of 'Winter Supplement' from as much of my code as possible. 

Though some functions, like calculate_base_amount and calculate_children_amount, are simple one-liners, they encapsulate business logic. This makes them more maintainable and allows for flexibility if additional qualifiers or conditions are introduced in the future.

### MQTT Loop Behavior
The client wrapper uses loop_forever instead of loop_start under the assumption that the application will run as a single process in a container. This approach would allow for horizontal scaling by running multiple instances.

### Absence of Docstrings
The project's code was written with the aim of not needing comments by opting to use descriptive function and variable naming conventions in order to effectively convey the meaning of the code. Docstring comments were planned to be included to ensure grading went as smooth as possible but due to time constraints they could not be included.

### Dependencies
The minimal amount of dependencies were used to meet the criteria while minimizing any potential vulnerabilities or bloat. paho-mqtt and coverage were the only extensions used to connect to the MQTT broker and determine all necessary code was covered.

### Additional Resources
* [paho-mqtt documentation](https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html)