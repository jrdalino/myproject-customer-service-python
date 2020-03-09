# Set base image to python
FROM python:3.7
ENV PYTHONBUFFERED 1

# Copy source file and python req's
COPY . /app
WORKDIR /app

# Install requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set image's main command and run the command within the container
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["app.py"]