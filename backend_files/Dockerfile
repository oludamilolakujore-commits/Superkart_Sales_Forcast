# Use a minimal base image with Python 3.9 installed
FROM python:3.9-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy all files from the current directory on the host to the container's /app directory
COPY . .

# Install Python dependencies listed in requirements.txt
RUN pip3 install -r requirements.txt

# Hugging Face Docker Spaces route external traffic to port 7860
EXPOSE 7860

# Define the command to run the Flask API on port 7860 and make it accessible externally
CMD ["python3", "app.py"]
