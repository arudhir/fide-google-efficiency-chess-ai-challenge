# Use a lightweight base image
FROM python:3.11-slim

# Install uv
RUN pip install uv

# Set environment variable to disable output buffering
ENV PYTHONUNBUFFERED=1

# Set up working directory
WORKDIR /app

# Copy your chess agent code
COPY . /app

# Sync dependencies using uv
RUN uv sync

# Set entrypoint to a script that enforces ulimit constraints
ENTRYPOINT ["bash", "/app/entrypoint.sh"]
