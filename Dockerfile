# 1. Use the official lightweight Python image from Docker Hub
FROM python:3.12-slim

# 2. Set the working directory inside the virtual container container
WORKDIR /app

# 3. Copy our Python project files from your computer into the container
COPY app.py ingest_data.py ecommerce.db ./

# 4. Install the required external software libraries
RUN pip install --no-cache-dir streamlit pandas plotly scikit-learn openpyxl starlette uvicorn

# 5. Open up port 8501 so web browsers can connect to the container
EXPOSE 8501

# 6. Command to automatically run the platform when the container starts
CMD ["python", "-m", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
