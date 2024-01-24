# Backend Interview README

> Written by Shen Yifan

### **Part 1: Fork and Set Up the Repository**

Done.

### **Part 2: Setup dev environment and understand basic flow**

Done.

### Part 3: **Implement a ExpandReduceFlow and corresponding**ExpandOp and ReduceOp

**expand_op.py:**

~~~python
class ExpandOp(Op):
    def __init__(self, root_node, split_func=None):
        super().__init__(root_node.value_dict)
        self.split_func = split_func if split_func else self.default_split
        self.expand_1, self.expand_2 = self.split_func()

    def default_split(self):
        n = len(self.value_dict)
        half = n // 2
        return {k: self.value_dict[k] for k in list(self.value_dict.keys())[:half]}, \
               {k: self.value_dict[k] for k in list(self.value_dict.keys())[half:]}

    def split_func(self):
        # Custom split logic can be implemented here
        return self.default_split()

~~~

**reduce_op.py:**

~~~python
class ReduceOp(Op):
    def __init__(self, expand_1, expand_2, merge_func=None):
        super().__init__({})
        self.merge_func = merge_func if merge_func else self.default_merge
        self.merge_func(expand_1, expand_2)

    def default_merge(self, expand_1, expand_2):
        for k1, v1 in expand_1.value_dict.items():
            for k2, v2 in expand_2.value_dict.items():
                self.value_dict[f"{k1} {k2}"] = f"{v1} {v2}"

    def merge_func(self, expand_1, expand_2):
        # Custom merge logic can be implemented here
        self.default_merge(expand_1, expand_2)

~~~

**expand_reduce_flow.py:**

~~~python
class ExpandReduceFlow:
    def __init__(self, root_node):
        self.expand_op = ExpandOp(root_node)
        self.reduce_op = ReduceOp(self.expand_op.expand_1, self.expand_op.expand_2)

~~~

**constants.py:**

~~~python
ExpandReduceFlow = "expand_reduce_flow"
~~~



### Part 4: Dockerize the Application

1. Create a Dockerfile to containerize your new Uniflow application with latest change.Ensure that all the necessary dependencies are installed. 

   ~~~dockerfile
   # Use an official Python runtime as a parent image
   FROM python:3.7-slim
   
   # Set the working directory in the container to /app
   WORKDIR /app
   
   # Add the current directory contents into the container at /app
   ADD . /app
   
   # Install any needed packages specified in requirements.txt
   RUN pip install --trusted-host pypi.python.org -r requirements.txt
   
   # Make port 80 available to the world outside this container
   EXPOSE 80
   
   # Run app.py when the container launches
   CMD ["python", "app.py"]
   
   ~~~

   This Dockerfile starts with a Python 3.7 image from the official Python Docker image. It sets the working directory to /app, adds the current directory (i.e., the one containing the Dockerfile) into the container, and installs all the Python dependencies listed in requirements.txt. The EXPOSE instruction tells Docker to make the port 80 available to the outside world. Finally, CMD specifies what command to run when the container is started. In this case, it runs the Python script named app.py.

2. Write instructions on how to build and run the Docker container.

   To build the Docker image, navigate to the directory containing the Dockerfile and run the following command:

   ~~~bash
   docker build -t my-uniflow-app .
   ~~~

   This command builds an image tagged as "my-uniflow-app" based on the Dockerfile in the current directory.

   To run the Docker container, use the following command:

   ~~~bash
   docker run -p 4000:80 my-uniflow-app
   ~~~

   This command runs a new container from the image we just built, maps port 4000 inside the container to port 80 on your host machine, and names the container "my-uniflow-app". Now, you should be able to access your Uniflow application at http://localhost:4000.

### Part 5 :**Deploy on Kubernetes**

1.Create a Kubernetes Deployment YAML file to deploy the latest Uniflow application.

2.Include necessary Kubernetes resources like Service, ConfigMap, or Secret if needed.

Create a **configmap.yaml**:

~~~yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: uniflow-config
data:
  DATABASE_URL: <your-database-url>
~~~

And then create a **deployment.yaml** :

~~~yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: uniflow-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: uniflow
  template:
    metadata:
      labels:
        app: uniflow
    spec:
      containers:
      - name: uniflow
        image: <your-uniflow-image>
        ports:
        - containerPort: 8080
        envFrom:
        - configMapRef:
            name: uniflow-config

~~~

**Write instructions on how to deploy the application on a Kubernetes cluster.**

1. First, you need to have a Kubernetes cluster set up and logged into. You can do this using the `kubectl` command line tool. Then, you can apply the YAML files to create the resources:

~~~bash
kubectl apply -f deployment.yaml
kubectl apply -f configmap.yaml  
~~~

2. After that, you can check the status of the deployment with:

~~~bash
kubectl get deployments
~~~

3. If everything is fine, you can scale the deployment to run more instances:

~~~bash
kubectl scale deployment uniflow-deployment --replicas=5
~~~

### Part 6:  **Integrate Local Database**

This code connects to a SQLite database file named `uniflow.db`, creates a table named `output` if it doesn't exist, runs the `ExpandReduceFlow` (assuming it's a class or function that returns a dictionary), and then inserts each key-value pair from the output into the `output` table.

To prevent race conditions, you would need to use locks or other synchronization mechanisms. This is a complex topic and the best approach depends on your specific requirements. In Python, you could use the `threading` module's `Lock` class for this purpose.

~~~python
import sqlite3
from uniflow import ExpandReduceFlow

# Connect to the SQLite database
conn = sqlite3.connect('uniflow.db')
c = conn.cursor()

# Create a table to store the output key-value pairs
c.execute('''
    CREATE TABLE IF NOT EXISTS output (
        key TEXT,
        value TEXT
    )
''')

# Run the ExpandReduceFlow
flow = ExpandReduceFlow()
output = flow.run()

# Store the output key-value pairs in the database
for key, value in output.items():
    c.execute('''
        INSERT INTO output (key, value)
        VALUES (?, ?)
    ''', (key, value))

# Commit the changes and close the connection
conn.commit()
conn.close()

~~~

### Part 7:  **Develop Client-Facing APIs**

#### **7.1 Asynchronous RESTful Invocation of** **ExpandReduceFlow**

Below is an example using Python's Flask framework to create an API endpoint for error handling during the ExpandReduceFlow process. This example assumes that you have a function `get_error_details` that fetches error details from a database or some other data source based on the job ID and filters.

~~~python
from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock function to get error details based on job ID and filters
def get_error_details(job_id, error_type=None, time_filter=None):
    # Fetch error details from database or other data source
    # For demonstration, returning mock data
    errors = [
        {'job_id': 'job1', 'error_type': 'TypeError', 'time_occurred': '2023-09-01T12:00:00', 'stack_trace': '...'},
        {'job_id': 'job2', 'error_type': 'ValueError', 'time_occurred': '2023-09-02T12:00:00', 'stack_trace': '...'},
        # ... more errors
    ]
    
    filtered_errors = errors
    
    if error_type:
        filtered_errors = [e for e in filtered_errors if e['error_type'] == error_type]
    
    if time_filter:
        filtered_errors = [e for e in filtered_errors if e['time_occurred'] == time_filter]
    
    return filtered_errors

@app.route('/api/error_handling', methods=['GET'])
def error_handling():
    job_id = request.args.get('job_id')
    error_type = request.args.get('error_type')
    time_filter = request.args.get('time_filter')
    
    if not job_id:
        return jsonify({"error": "Job ID is required"}), 400
    
    try:
        error_details = get_error_details(job_id, error_type, time_filter)
        return jsonify(error_details), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

~~~



To use this API, you can send a GET request to `http://localhost:5000/api/error_handling` with query parameters like so:

- `job_id`: The ID of the job for which you want to fetch error details.
- `error_type`: Optional. Filters the errors by type.
- `time_filter`: Optional. Filters the errors by time of occurrence.

For example, to get all TypeErrors that occurred on '2023-09-01T12:00:00', you would send a GET request to `http://localhost:5000/api/error_handling?job_id=job1&error_type=TypeError&time_filter=2023-09-01T12:00:00`.

#### **7.2 Synchronous RESTful Endpoint to Verify Async Call Status**

To create a synchronous RESTful endpoint to verify the status of an asynchronous call, you can use various programming languages and frameworks. Below is an example using Python with Flask:

~~~python
from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulated database of job statuses
job_statuses = {
    "job1": "pending",
    "job2": "completed",
    "job3": "running"
}

@app.route('/api/verify_status', methods=['GET'])
def verify_status():
    job_id = request.args.get('job_id')
    
    if job_id not in job_statuses:
        return jsonify({'error': 'Job ID not found'}), 404
    
    status = job_statuses[job_id]
    return jsonify({'job_id': job_id, 'status': status})

if __name__ == '__main__':
    app.run()

~~~

In this example, we have a simulated database (`job_statuses`) that stores the status of each job. The `verify_status` function retrieves the job ID from the query parameters and checks its status from the database. If the job ID is not found, it returns an error message. Otherwise, it returns the current status of the job.

You can test this endpoint by running the script and making a GET request to `http://localhost:5000/api/verify_status?job_id=job1`. It should return a JSON response like:

~~~json
{
  "job_id": "job1",
  "status": "pending"
}
~~~

#### **7.3 Synchronous RESTful Endpoint to Retrieve All key-value Pairs**

Here is a basic example of how you could implement this in Python using Flask and SQLAlchemy for database interaction. This example assumes that you have a `KeyValue` model with `key` and `value` fields.

~~~python
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'  # Use your own database URI
db = SQLAlchemy(app)

class KeyValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(80), unique=True, nullable=False)
    value = db.Column(db.String(120), nullable=False)

@app.route('/api/keyvalues', methods=['GET'])
def get_keyvalues():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 50)
    data = KeyValue.query.paginate(page, per_page, error_out=False)
    return {
        'items': [item.to_dict() for item in data.items],
        'total': data.total,
        'pages': data.pages,
        'current_page': data.page
    }

~~~

In this example, the `get_keyvalues` function retrieves all key-value pairs from the database and returns them as a JSON object. The `paginate` function from SQLAlchemy is used to manage pagination. The `page` and `per_page` parameters can be passed as query parameters to the API endpoint. If they are not provided, the default values are 1 and 10, respectively. The maximum number of items per page is limited to 50 to prevent overloading the server.

