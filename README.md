# swe599-troll-detector
Troll Detection Interface

-The application can only detect the inputs entered in the English language. 
-This app is mostly a tool developed to analyze the statements of suspicious social media trolls and decide whether 
the statements are troll or not.
-In the project, integration with the open source project named “transformers_state_trolls_cch” developed by GitHub 
user chuachinhon and integration with Google Perspective API is created.
-SWE599-Troll-Detector is analyzing a new expression entered as input and inferences about whether it is a troll 
expression or not.

•	Copy source folders of Chuachinhon’s transformers_state_trolls_cch project ( https://www.dropbox.com/sh/lk9blbafnvlzo28/AAA0RoAurXg_QPCxT5SG-slFa?dl=0 )
These files should be under project directory (under swe599-troll-detector folder)
•	Create a virtual environment in the project root directory: 
python3 -m venv venv
•	Activate  virtual environment: 
source venv/bin/activate
•	Install requirments of the project: 
pip3 install -r requirements.txt
•	Run flask application in the app folder: 
cd app & python3 -m flask run

![main_page](https://github.com/ilterisdkc/swe599-troll-detector/blob/main/main-page.png)

![results](https://github.com/ilterisdkc/swe599-troll-detector/blob/main/Results for Obama Tweet.png)
