FROM python:3.9-slim

WORKDIR /app


#Copies the Local Files(such as the .py file over)
COPY . .

RUN pip install --no-cache-dir -r requirements.txt


#Run the command to start the program
CMD ["python", "nba_stat_fetcher.py"]




