FROM mcr.microsoft.com/playwright/python:v1.49.1-noble


# Set the working directory to /app
WORKDIR /app
# Copy requirements.txt to the working directory
COPY requirements.txt ./

# Install dependencies

# Copy the rest of the application code to the working directory
COPY . .
#upgrade pip
RUN pip install --upgrade pip
#RUN apt-get update && apt-get install -y default-libmysqlclient-dev gcc
#installing the dependencies
RUN pip install --no-cache-dir -r requirements.txt
#CMD instruction should be used to run the software
#contained by your image, along with any arguments.

#CMD ["python3", "-m", "server", "--host=0.0.0.0", "--port=443"]
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "4", "app:app"]