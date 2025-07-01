#base image 
FROM python:latest

#working directory
WORKDIR /app

#copy 
COPY . /app/

#run
RUN pip install --no-cache-dir -r requirements.txt

#expose port
EXPOSE 5000

#command to run the app
CMD ["python", "app.py"]