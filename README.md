*** Tutorial created with ChatGPT assistant***
https://chatgpt.com/share/68353898-7330-800f-9034-c93926ffa21d

Here's a step-by-step tutorial for an absolute beginner to use curl to build, run, and test a local API and its services using CLI tools. This will cover:

Setting up a local API (we’ll use Python’s Flask for simplicity).
Running it locally.
Using curl to interact with the API (GET, POST, PUT, DELETE).

🧰 Prerequisites
Make sure you have the following installed:
Python 3.x → python3 --version
pip → pip --version
curl → curl --version


🧱 Step 1: Create a Simple Local API Using Flask
Create a working folder:
mkdir my-local-api && cd my-local-api

Install Flask:
pip install flask

Include a file called app.py:
nano app.py

your app.py, designed for absolute beginners, using:
Flask with RESTful best practices
Upsert support
Automatic JSON file loading/saving
Full HTTP status codes + headers
Extensive inline comments for learning

🧱 Step 1: Create a Virtual Environment
In your project folder (/my-local-api):
python3 -m venv venv
This creates a folder called venv/ that will hold Python and pip just for your project.
▶️ Step 2: Activate the Virtual Environment
Run this command:
source venv/bin/activate
Your prompt should now change to something like:
(venv) drei@S340:/my-local-api$
❌ To Exit the Virtual Environment Later:
Just run:
deactivate
📦 Step 3: Install Flask Safely
Now, while the virtual environment is active:
pip install flask
🚀 Step 4: Run Your Flask App
You can now run:
python3 app.py
You will see output like:
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
This means your local API is now running at http://127.0.0.1:5000

TEST wit PYTEST
pip install flask pytest
pytest ./test_app.py


