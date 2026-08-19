# 1. Use official lightweight Python image
FROM python:3.12-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy our Python project files into the container
COPY . /app

# 4. Install required libraries (Added redis module)
RUN pip install --no-cache-dir streamlit redis pandas scikit-learn openpyxl

# 5. Open up port 8585 for web browsers
EXPOSE 8585

# 6. Default command (Overridden by docker-compose for workers)
CMD ["streamlit", "run", "app.py", "--server.port=8585", "--server.address=0.0.0.0"]
