# Project Setup
```bash
# Create a project directory:
mkdir chocolate_supply_chain_aws
cd chocolate_supply_chain_aws

# Create a virtual environment:
python3 -m venv venv
source venv/bin/activate  # On Linux/macOS

#Install Flask and psycopg2:
pip install Flask psycopg2
```


# Database Setup (AWS RDS for PostgreSQL)

Create an RDS instance:

Log in to the AWS Management Console.

Go to the RDS service.

Create a new PostgreSQL database instance.

Configure the instance settings:

DB instance identifier: Choose a name (e.g., chocolate-db).

Engine version: Select a PostgreSQL version (e.g., 14.9).

Template: Choose "Free tier" (if eligible) or "Production" for a more robust setup.

Settings:

DB instance class: Choose an instance type (e.g., db.t3.micro for free tier, or a larger one for production).

Storage: Allocate storage (e.g., 20 GiB for free tier, adjust as needed).

Master username: your_user

Master password: your_password  (store securely)

Connectivity:

Virtual Private Cloud (VPC): Use the default VPC or create a new one.

Subnet group: Use the default subnet group or create a new one.

Publicly accessible: Set to "Yes" if you want to connect from your local machine (for initial setup).  Important: For production, it's recommended to keep it "No" and access it from within your VPC (e.g., from an EC2 instance).

VPC security group: Create a new security group that allows inbound connections on port 5432 (PostgreSQL) from your IP address (for development) or from your EC2 instance's security group (for production).

Database options:

Database name: chocolate_db

Review and create the database.

Note down the endpoint (host), database name, username, and password. You'll need these to connect to the database.



# Flask Application Setup

Create app.py:

Explanation of app.py:

The code is similar to the previous version, but with a crucial change:  It now retrieves database connection details from environment variables (os.environ).  This is essential for security and for deploying to AWS.

Important: You will need to set these environment variables in your deployment environment (e.g., on your EC2 instance, in your ECS task definition, or in AWS Lambda).

Set up EC2 Instance (Optional, for running Flask):

Launch an EC2 instance:

Go to the EC2 service in the AWS Management Console.

Launch a new instance.

Choose an Amazon Machine Image (AMI) (e.g., Amazon Linux 2).

Choose an instance type (e.g., t3.micro for free tier, or a larger one as needed).

Configure instance details (VPC, subnet).  Make sure the instance is in the same VPC as your RDS instance (if they need to communicate).

Security Group: Create a new security group that allows:

Inbound traffic on port 22 (SSH) from your IP address (for access).

Inbound traffic on port 5000 (or your Flask app's port) from 0.0.0.0/0 (for public access) or from the security group of your load balancer (if you're using one).

Configure storage.

Add tags (e.g., Name: chocolate-app-server).

Review and launch the instance.

Create a new key pair and download the .pem file.  Important: Store this file securely.

Connect to the EC2 instance:

Use an SSH client (e.g., ssh on Linux/macOS, PuTTY on Windows) to connect to the instance using the downloaded .pem file.

Install Python and dependencies:

Once connected, update the package manager and install Python and pip:

sudo yum update -y  # For Amazon Linux
sudo yum install -y python3 python3-pip

Create a virtual environment:

python3 -m venv venv
source venv/bin/activate

Install Flask and psycopg2:

pip install Flask psycopg2

Copy your Flask application code (app.py) to the EC2 instance using scp.

Set environment variables:

Set the database connection details as environment variables on the EC2 instance:

export DB_HOST=chocolate-scm-db.cczmwsygmnv6.us-east-1.rds.amazonaws.com  # From RDS setup
export DB_NAME=postgres
export DB_USER=postgres      # From RDS setup
export DB_PASSWORD=chocolate-scm-master      # From RDS setup

(You might want to add these to your ~/.bashrc or ~/.bash_profile file so they persist across sessions.)

Run the Flask application: 
```bash
python app.py
```

Create Database Tables:

You can create the tables using a PostgreSQL client from your local machine or from the EC2 instance.

From your local machine:

Use a PostgreSQL client (e.g., psql, pgAdmin) and connect to your RDS instance using the endpoint, username, password, and database name.

Execute the CREATE TABLE statements provided in the previous guide.

From the EC2 instance:

Install psql if it's not already installed:

sudo yum install -y postgresql

Connect to the RDS instance:

psql -h your_rds_endpoint -d chocolate_db -U your_user -p 5432

Enter the password when prompted.

Execute the CREATE TABLE statements.

5. Test the API
From your local machine (if RDS is publicly accessible):

Use curl or Postman, as shown in the previous guide, but use the public IP address or DNS name of your EC2 instance (if running Flask on EC2) or if you have set up a Load Balancer, use that DNS name.

From the EC2 instance:

You can test the API endpoints using curl directly on the EC2 instance:

```bash
curl http://localhost:5000/api/health
curl http://localhost:5000/api/products
curl -X POST -H "Content-Type: application/json" \
-d '{"name": "Dark Chocolate", "description": "Premium dark chocolate", "manufacturer_id": 1, "batch_number": "BATCH001"}' \
http://localhost:5000/api/products
```


```sql
# Connect to PostgreSQL
   psql -h chocolate-scm-db.xxxxxxxxxx.us-east-1.rds.amazonaws.com -d chocolate_db -U postgres -p 5432
   
   # Enter password when prompted
   
   # You should now see the psql prompt:
   # chocolate_db=>
   
   # Execute the INSERT statement:
   INSERT INTO manufacturers (manufacturer_id, name, location) VALUES (1, 'Sample Manufacturer', 'Sample Location');
   
   # You should see output like:
   # INSERT 0 1
   
   # View the contents of the manufacturers table:
   SELECT * FROM manufacturers;
   
   # Exit psql:
   \q
```
