# Project : Data Lake

## Project Overview:

<ul>A music streaming platform <strong>Sparkify</strong> has grown their database and want to move their data warehouse to a data lake.The data resides in s3 in a directory of JSON logs.And as a data engineer we need to build an ETL pipeline that extracts data from s3 and process them using Spark and loads back into s3 as a set of dimensional tables.It will help their analytics team to find the insights in what songs their users are listening to.
</ul><br>

## Project Files:
The files in this repository are :
- data/
- etl.py
- dl.cfg
- README.md
<br>

**Project Datasets/** - We have two datasets that reside in S3. Here are the S3 links for each:

- Song data: s3://udacity-dend/song_data
- Log data: s3://udacity-dend/log_data
- Log data json path: s3://udacity-dend/log_json_path.json
.
- 1. 'log_data/' - It contains JSON files related to songplay log data.

ex:
    {"artist":null,
     "auth":"Logged In",  
     "firstName":"Walter",  
     "gender":"M",  
     "itemInSession":0,
     "lastName":"Frye",
     "length":null,
     "level":"free",  
     "location":"San Francisco-Oakland-Hayward, CA",  
     "method":"GET",  
     "page":"Home",
     "registration":1540919166796.0,  
     "sessionId":38,  
     "song":null,
     "status":200,  
     "ts":1541105830796,  <br>
     "userAgent":"\"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"",  <br>
     "userId":"39"
     }
- 2. 'song_data/' - It has JSON files that contains metadata about song and artist of that song.

ex:
    {"num_songs": 1,<br>
     "artist_id": "ARJIE2Y1187B994AB7",<br>
     "artist_latitude": null, <br>
     "artist_longitude": null,<br>
      "artist_location": "",<br>
      "artist_name": "Line Renaud",<br>
      "song_id": "SOUPIRU12A6D4FA1E1", <br>
      "title": "Der Kleine Dompfaff",<br>
      "duration": 152.92036, <br>
      "year": 0}

**dwh.cfg** -<ul> This files contains all the information about the the AWS credentials.</ul>

**etl.py** -<ul> In this script file, we will read data from s3 and processes that data using Spark and writes them back to s3.</ul>

**README.md** - <ul>It provides details information about the project.</ul>

<br>

## Sparkify DataSchema :
The DataSchema has 7 tables represented in a Star schema.

#### Fact Table -
- songplays - It has records in log data associated with song plays.  

#### Dimension Tables -
- users - It has data about the users in the app.
- songs - It has data about the songs in music database.
- artists - It has data about the artists in music database.
- time - It has data about the timestamps of records in songplays broken down into specific units.

## Project Steps :
#### Step1 :-
<ul>Provide the AWS credential details in the <em>'dwh.cfg'</em> file. </ul>

#### Step2 :-
<ul>Complete the 'etl.py'</em> to load the data from s3 and process that data using Spark and write back all the data to s3.</ul>

#### Step3 :-
<ul>Run the <em>'etl.py'</em> to load data from s3 to tables and processes them and write back them to s3.</ul>
- !python etl.py
