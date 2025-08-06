FROM python:3.9-slim
# Set the working directory
WORKDIR /app

# Install system dependencies
RUN pip install streamlit

# Expose the port for Streamlit
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]