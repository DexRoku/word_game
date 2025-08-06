FROM python:3.9-slim
WORKDIR /app

# Copy the app folder (with app.py inside) into the container
COPY app ./app

# Install dependencies
RUN pip install streamlit

EXPOSE 8501

# Run the app with correct path
CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
