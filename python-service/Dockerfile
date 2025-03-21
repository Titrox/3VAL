FROM python:3.10

WORKDIR /app

# Copy relevant files to container
COPY requirements.txt requirements.txt
COPY validation.py validation.py

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "validation.py"]
