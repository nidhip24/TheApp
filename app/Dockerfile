FROM python:3.9-slim

# Set a non-root user
RUN addgroup --system appgroup && adduser --system --group appuser

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Set proper ownership
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Expose the port on which the application will run
EXPOSE 8080

RUN pwd

# Run the FastAPI application using uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

