# AWS 3-Tier Task Manager

A simple 3-tier task management application deployed on AWS using CloudFront, Amazon S3, Elastic Beanstalk, and MongoDB Atlas.

## Project Overview

This project is a simple Task Manager application built to demonstrate a 3-tier cloud architecture on AWS.

Users can add tasks, view tasks, and delete tasks through a web interface.

The frontend is hosted using Amazon S3 and delivered through Amazon CloudFront. The backend is deployed on AWS Elastic Beanstalk and runs Flask behind an Application Load Balancer. Task data is stored in MongoDB Atlas.

## Architecture

```text
User
 |
 v
CloudFront HTTPS
 |
 +--------------------+
 |                    |
 v                    v
S3 Frontend       /api/* request
HTML/CSS/JS            |
                       v
              Elastic Beanstalk
                       |
                       v
              Application Load
                  Balancer
                       |
                       v
              Private EC2 instances
                       |
                       v
                 MongoDB Atlas
AWS 3-Tier Design
Frontend Layer
Amazon S3
Amazon CloudFront
HTML
CSS
JavaScript

The frontend files are stored in an S3 bucket and served through CloudFront using HTTPS.

CloudFront also forwards /api/* requests to the Elastic Beanstalk backend.

Backend Layer
Python
Flask
Gunicorn
AWS Elastic Beanstalk
Application Load Balancer

The Flask application provides REST APIs for task management.

Database Layer
MongoDB Atlas
Database: taskdb
Collection: tasks

MongoDB Atlas is used as the database layer. Database access is restricted using network/IP access controls.

Application Features
View tasks
Add a task
Delete a task
Backend health check
Database health check
API Endpoints
Health Check
GET /health

Returns the application health status.

Example:

{
  "status": "ok"
}
Database Health Check
GET /health/db

Checks connectivity between the Flask application and MongoDB.

Get Tasks
GET /api/tasks

Returns all tasks.

Add Task
POST /api/tasks

Example request:

{
  "title": "Learn AWS"
}
Delete Task
DELETE /api/tasks/<task_id>

Deletes a task using its MongoDB ID.

AWS Services Used
Service	Purpose
Amazon VPC	Network isolation
Public Subnets	ALB and NAT Gateway
Private Subnets	Backend instances
Internet Gateway	Internet connectivity
NAT Gateway	Outbound internet access from private subnets
Security Groups	Network access control
Elastic Beanstalk	Backend deployment
Application Load Balancer	Backend traffic distribution
Amazon S3	Frontend hosting
Amazon CloudFront	HTTPS delivery and API routing
MongoDB Atlas	Database
VPC Configuration

VPC CIDR:

10.0.0.0/16
Public Subnets
ap-south-1a
10.0.0.0/20

ap-south-1b
10.0.16.0/20
Private Subnets
ap-south-1a
10.0.128.0/20

ap-south-1b
10.0.144.0/20

The Application Load Balancer is placed in the public subnets.

Elastic Beanstalk application instances run in the private subnets.

Security

The application uses separate security controls for the load balancer and backend.

The public-facing load balancer accepts HTTP traffic.

Backend instances are not assigned public IP addresses.

Backend traffic is controlled using security groups.

The private subnets use a NAT Gateway for required outbound internet access.

MongoDB Atlas access is restricted using IP/network access rules instead of making the database publicly open to all traffic.

Sensitive environment variables such as the MongoDB connection string are stored in the Elastic Beanstalk environment and are not committed to GitHub.

Environment Variables

The backend uses the following environment variable:

MONGODB_URI

The MongoDB connection string is not stored in the GitHub repository.

Elastic Beanstalk

Application:

aws-3tier-task-manager

Environment:

Aws-3tier-task-manager-env

Platform:

Python
Amazon Linux 2023

The Elastic Beanstalk environment uses a load-balanced web server environment.

The backend application runs using Gunicorn.

Gunicorn Configuration

The project uses the following Procfile:

web: gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 30 app:app
CloudFront Configuration

CloudFront provides the public HTTPS endpoint for the application.

Frontend requests are served from the S3 origin.

API requests matching:

/api/*

are forwarded to the Elastic Beanstalk origin.

The API behavior uses caching disabled so that task operations are sent directly to the backend.

Deployment Process
1. Create the application

The backend was created using Flask and the frontend using HTML, CSS and JavaScript.

2. Configure MongoDB

MongoDB Atlas was configured as the application database.

3. Create AWS networking

A custom VPC was created with:

2 public subnets
2 private subnets
Internet Gateway
NAT Gateway
Route tables
Security groups
4. Deploy the backend

The Flask backend was deployed to Elastic Beanstalk.

5. Configure private backend instances

Elastic Beanstalk instances were configured without public IP addresses and placed in private subnets.

6. Configure the frontend

The frontend files were uploaded to Amazon S3.

7. Configure CloudFront

CloudFront was configured with:

S3 frontend origin
Elastic Beanstalk API origin
/api/* behavior
HTTPS viewer access
8. Test the application

The application was tested by:

Opening the CloudFront URL
Loading existing tasks
Adding tasks
Deleting tasks
Checking backend health
Live Application

CloudFront URL:

https://dzu6tjt516jtx.cloudfront.net

GitHub Repository

https://github.com/Kaif2001/3-tier-aws-task-manager

Project Structure
3-tier-aws-app/
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── Procfile
│   └── .env
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
└── .gitignore

The .env file is excluded from Git using .gitignore.

Testing

The deployed application was tested through the CloudFront URL.

Example task operations:

AWS Elastic Beanstalk
CloudFront Test

The task data was successfully stored and retrieved through the backend API.

Conclusion

This project demonstrates a simple 3-tier application architecture using AWS networking, Elastic Beanstalk, S3, CloudFront and MongoDB Atlas.

The main goal was to keep the application simple while demonstrating deployment, networking, security, API communication and database connectivity on AWS.