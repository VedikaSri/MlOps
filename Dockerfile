# start with a light weight python image
# this gives over container a python runtime
FROM python:3.14-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the dependency list before coping application code
COPY requirements.txt .

# avoid retaining pip's download cache in the image
RUN pip install --no-cache-dir -r requirements.txt

# copy the application code and save model into /app
COPY . .
# first . -> source
# second . -> destination

# document the port used by FastAPI application
EXPOSE 8000

# Start the API server when container launches
# 0.0.0.0 allows connections through the containers's network interfaces
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]