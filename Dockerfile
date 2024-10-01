# Dockerfile for AGEAN_Cyber multipurpose agent

# Use official Python image from Docker Hub
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    LANGCHAIN_TRACING_V2=true \
    LANGCHAIN_API_KEY=$LANGCHAIN_API_KEY \
    HUMANLOOP_API_KEY=$HUMANLOOP_API_KEY

# Create a working directory
WORKDIR /app

# Copy the application code into the container
COPY . /app

# Install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Expose port (optional, depending on if your agent has a web interface/API)
EXPOSE 8000

# Set the default command to run the agent
CMD ["python", "-m", "MultipurposeAgent"]
