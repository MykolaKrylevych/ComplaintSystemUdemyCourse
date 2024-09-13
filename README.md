# Complaint Management System

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![AWS](https://img.shields.io/badge/AWS_S3_and_SES-232F3E?style=for-the-badge&logo=amazon-aws)
![Wise](https://img.shields.io/badge/Wise_API-00B9FF?style=for-the-badge&logo=wise)


This project is a Complaint Management System built with FastAPI. It allows users to submit complaints, track their status, and receive email notifications regarding status updates.

## Features

- **Submit Complaints**: Users can create complaints, which are stored in a PostgreSQL database.
- **Email Notifications**: The system uses AWS SES (Simple Email Service) to send notifications to users when the status of a complaint changes.
- **File Uploads**: AWS S3 is used for storing files attached to complaints (e.g., photos, documents).
- **Wise Integration**: The system integrates with the Wise API for processing financial operations related to complaints.

## Technologies Used

- **FastAPI**: A modern, fast web framework for building APIs with Python 3.6+.
- **PostgreSQL**: A powerful, open-source object-relational database system.
- **AWS S3 & SES**: Amazon's cloud storage and email services.
- **Wise API**: Integration with Wise for financial transactions.

## Requirements

To run the project, you'll need the following:

- Python 3.9+
- PostgreSQL
- AWS credentials for S3 and SES
- Wise account for API access

## Installation

1. Clone the repository:
```bash
git clone https://github.com/MykolaKrylevych/ComplaintSystemUdemyCourse.git
```
2. Navigate to the project directory:

  ```bash
cd ComplaintSystemUdemyCourse
  ```
3. Install the required dependencies:

  ```bash
pip install -r requirements.txt
  ```
4. Set up the environment variables:

- DATABASE_URL: URL for connecting to PostgreSQL.
- AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY: Your AWS credentials for accessing S3 and SES.
- WISE_API_KEY: API key for Wise integration.

5. Apply database migrations:
  ```bash
  alembic upgrade head
  ```
6. Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```
## Usage
Once the server is up and running, you can access the Swagger documentation at `http://127.0.0.1:8000/docs` to interact with the API.
