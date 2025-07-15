# Dockerfile

# Use the official Python image with the desired version
FROM python:3.13.3-slim


# Set app/ as working directory and Copy files in it 

WORKDIR /app

COPY requirements.txt /app
COPY app/drug_app.py /app
COPY models/. /app/models/


# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Gradio will run on (default is 7860)
EXPOSE 7860

ENV GRADIO_SERVER_NAME="0.0.0.0"

# Command to run your application
CMD ["python", "drug_app.py"]

