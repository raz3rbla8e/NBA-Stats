FROM python:3.9-slim

WORKDIR /app


#Copies the Local Files(such as the .py file over)
COPY . .

RUN pip install --no-cache-dir -r requirements.txt


#Run the command to start the program
CMD ["python", "nba_stat_fetcher.py"]


#Builds the image titled nba-stat-fetcher from the Dockerfile
#docker build -t shrimahesh04/nba-stat-fetcher .

#Pushes the image to my docker account
#docker push shrimahesh04/nba-stat-fetcher


#runs the container from the image thats loaded on my account
#docker run --rm -it shrimahesh04/nba-stat-fetcher




