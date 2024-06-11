# Use the official Python base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    API_ID=${API_ID} \
    API_HASH=${API_HASH} \
    BOT_TOKEN=${BOT_TOKEN} \
    PORT=8080

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the bot listens on
EXPOSE $PORT

# Run the bot
CMD ["python", "bot.py"]
