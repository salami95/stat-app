import os
import uuid
import requests
import boto3
from flask import Flask, render_template, request, redirect, session
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "stat_secret_key")

# AWS S3 configuration - these environment variables must be set in Railway.
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME", "your-default-bucket-name")

# Initialize the S3 client
s3 = boto3.client("s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

# URL for the backend job service (your worker service)
BACKEND_JOB_URL = os.getenv("BACKEND_JOB_URL", "http://jobqueue-production.up.railway.app/start-job")

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('audio')
    if not file:
        return "No file uploaded", 400

    # Secure the filename and make it unique
    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4().hex}_{filename}"

    # Upload file to S3
    try:
        s3.upload_fileobj(file, AWS_S3_BUCKET_NAME, unique_filename)
    except Exception as e:
        session['log_output'] = f"Failed to upload file to S3: {str(e)}\n"
        return redirect('/processing')

    # Generate a presigned URL (valid for 1 hour)
    try:
        file_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': AWS_S3_BUCKET_NAME, 'Key': unique_filename},
            ExpiresIn=3600
        )
    except Exception as e:
        session['log_output'] = f"Failed to generate presigned URL: {str(e)}\n"
        return redirect('/processing')

    session['log_output'] = "Upload received and file stored on S3. Starting processing...\n"
    session.modified = True

    try:
        # Trigger backend processing by sending the S3 URL
        response = requests.post(BACKEND_JOB_URL, json={"filepath": file_url})
        response.raise_for_status()
        session['log_output'] += "✓ Processing job submitted successfully.\n"
    except Exception as e:
        session['log_output'] += f"✗ Failed to start processing: {str(e)}\n"
        return redirect('/processing')

    try:
        data = response.json()
        session['topics'] = data.get('topics')
        session['summary'] = data.get('summary')
        session['scripts'] = data.get('scripts')
        return redirect('/results')
    except Exception as e:
        session['log_output'] += f"✗ Error parsing worker response: {str(e)}\n"
        return redirect('/processing')

@app.route('/processing')
def processing():
    return render_template("processing.html", log_output=session.get("log_output", ""))

@app.route('/results')
def results():
    return render_template("results.html", session=session)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
