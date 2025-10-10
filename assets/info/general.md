# DOCS: notify-cyber

## Brief History

- In December 2019, Mehmet became really paranoid about cyber security after discovering how the hardware/software that people use everyday is being explioted everyday by criminals what want to hurt others.
- In 2021, Mehmet started looking into ways to automate getting infomration about the latest cyber security news. He thought, by keeping yourself up to date about the latest cyber security news, is the best way most people can protect themselfs from hackers/criminals.
- In around February 11, 2022, Mehmet and Dylan started a project called thn-discord-bot (TDB) which can be viewed here: https://github.com/MehmetMHY/thn-discord-bot
  - This was basically an earlier verison of notify-cyber. It was a Discord bot that would get the latest cyber security news from "The Hacker News" and post them on a Discord server. There was a channel for all the news then 4 "filter" channels. These filter channels were for "Google", "Microsoft", "Apple", and "Linux". They would contain news related to their names.
  - Well this project was running, there were around 10 to 20 people in the Discord server. But most people had the server muted and most of these people were classmate and/or friends.
  - In May 2022, the service was shut down and the Discord server was deleted. The code was then maked open source on GitHub.
  - The main things learned with this project were the following:
    - Discord sucks at measuring engagement.
    - A good amount of people did not use Discord as their main notification platform.
    - A lot of people muted the channel and most people did not think the filter channels were that useful.
    - People wanted to make their own filters, not just be limited to 4 options.
- On April 21, 2022, this repo was made: https://github.com/MehmetMHY/thn-api
  - This repo contained the "The Hacker News" web scrapper that was developed for the Discord bot. It was made in the hopes that it would help some people out (if needed).
- On (around) February 2023, notify-cyber (NC) was created. It was initially developed for a Hackathon hosted by Courier on the Devpost platform. As the Hackathon went on, Mehmet and Dylan dropped the Hackathon because they confirmed that Courier's API is NOT ideal/designed-for what notify-cyber is trying to do. They then decided to make this into a product rather than just a project for a Hackathon.

## \*How to setup repo before building the docker image

```
# go to this dir:
cd collector/scraping

# clone cvelist
git clone https://github.com/CVEProject/cvelist.git
```

- NOTE: You HAVE to do this before building the Docker image

## SQL queries:

```
# count the total number of entries in the db
SELECT COUNT(*) FROM cybernews;

# count the total number of unique URL(s) in the db
SELECT COUNT(DISTINCT url) AS unique_url_count FROM cybernews;

# count the number of unique sources in the db
SELECT source, COUNT(*) AS count FROM cybernews GROUP BY source;
```

## Build Image V2:

```
# go to repo's directory:
cd notify-cyber/

# build project's image:
docker build -t notify_cyber .

# run container:
docker run --name c_news -e POSTGRES_PASSWORD=password -d -p 5432:5432 -p 8000:8000 notify_cyber

# exec into container:
docker exec -it $(docker ps | awk '{print $1}' | tail -n 1) bash

# stop container:
docker stop $(docker ps | awk '{print $1}' | tail -n 1)

# start container:
docker start $(docker ps -a | grep "notify_cyber" | awk '{print $1}')
```

## Setting up a local Python environment:

1. Install and setup python3, pip3, and virtualenv on your machine
2. Setup python environment:
   ```
   python3 -m venv env
   ```
3. Active environment:
   ```
   source env/bin/activate
   ```
4. Install required python packages for this project by running this command:
   ```
   pip3 install -r requirements.txt
   ```
5. From here you can install and/or update any packages you want by using pip.
6. (optional) Update requirements.txt when ever you update or install a new pip package:
   ```
   pip3 freeze > requirements.txt
   ```
7. Deactivate environment:
   ```
   deactivate
   ```

## AI Notes:

- Why is AI used in Notify Cyber?
  - AI is used to summarize aritcles into a couple sentences for anyone in the emil "newsletter"
  - This will make it easier for users to get an overview of the article as well as better avoid "click bait" titles.
- How to setup the AI for this project:
  1. WARNING: The AI setup for this project assumes you are using Ubuntu 20 and your computer has a modern Nvidia GPU. If not, this AI feature will not work on your system. If you do not have the prefered setup, DO NOT continue with these steps. If you want though, you can mess with the code and try to make it work on your setup.
  2. Make sure you are using a Unix based operating system (ideally Ubuntu or MacOS)
  3. Make sure you set up everything else for this project.
  4. Install Python3, Pip3, and all the python package requirments by using the requirements.txt file located at the root of this repo.
  5. Install HuggingFace's transformers library:
     ```
     pip3 install transformers
     ```
  6. Update your system:
     ```
     sudo apt update
     sudo apt upgrade
     ```
  7. Make sure you have the nvidia driver installed by running the following command:
     ```
     nvidia-smi
     ```
  8. Skip this step if the command above outted currectly. Go to and follow the steps layouted on these websites:
     - NOTE: make sure to install the nvidia drivers from nvidia directly!
     - https://www.cyberciti.biz/faq/ubuntu-linux-install-nvidia-driver-latest-proprietary-driver/
     - https://linuxconfig.org/how-to-install-the-nvidia-drivers-on-ubuntu-20-04-focal-fossa-linux
  9. Install and test Cuda:

     ```
     # Source: https://linuxconfig.org/how-to-install-cuda-on-ubuntu-20-04-focal-fossa-linux

     # install Cuda:
     sudo apt install nvidia-cuda-toolkit

     # test Cuda (output driver information):
     nvcc --version
     ```

  10. Install PyTorch:
      ```
      # check this source out for more details: https://pytorch.org/
      pip3 install torch torchvision torchaudio
      ```

- Things I learned about AI:
  - The philschmid/bart-large-cnn-samsum model's token indices max sequence length us 1024
- Sources used to build the AI part of this project:
  - https://huggingface.co/philschmid/bart-large-cnn-samsum
  - https://huggingface.co/docs/transformers/main_classes/pipelines
  - https://huggingface.co/docs/transformers/main_classes/pipelines
  - https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them
  - https://pytorch.org/get-started/locally/
  - https://linuxconfig.org/how-to-install-cuda-on-ubuntu-20-04-focal-fossa-linux
  - https://stackoverflow.com/questions/48152674/how-do-i-check-if-pytorch-is-using-the-gpu
  - https://phoenixnap.com/kb/how-to-install-python-3-ubuntu
  - https://huggingface.co/philschmid/bart-large-cnn-samsum
  - https://huggingface.co/philschmid/flan-t5-base-samsum
  - https://gist.github.com/ksopyla/bf74e8ce2683460d8de6e0dc389fc7f5

## General Notes:

- Information about the logo:
  - The logo is stored in assets/
  - The logo was generated using OpenAI's DALL-E 2 on 3-10-2023
  - The promot for DALL-E was: “A picture of a bird carrying a news paper”
  - The logo was lightly editied, cleaned up, by Mehmet on MacOS using Preview, Google Drawing, and Screenshot.

## (temporary) Way Of Running The App:

1. Make sure you have Docker installed; ideally in a Unix based OS
2. Make sure to be in the project's root dir
3. Build and create the App's docker container:

   ```
   # build docker image:
   docker build -t notify_cyber .

   # run docker container from built image:
   docker run --name c_news -e POSTGRES_PASSWORD=password -d -p 5432:5432 -p 8000:8000 notify_cyber
   ```

4. Manually execute App's importat processes in the container:

   ```
   # go into the container:
   docker exec -it $(docker ps -a | grep "notify_cyber" | awk '{print $1}' | tail -n 1) bash

   # run process setup script:
   #   - NOTE: Might have to hit ENTER after running the script
   bash run.sh

   # exist container:
   exist
   ```

5. Go to the following url to use the app:
   - http://localhost:8000/
6. When needed, this is how you stop and start the container you created:

   ```
   # stop container:
   docker stop $(docker ps | awk '{docker ps -a | grep "notify_cyber" | awk '{print $1}' | tail -n 1)

   # start container:
   #   - NOTE: Go though step 4 after starting the container again
   docker start $(docker ps -a | grep "notify_cyber" | awk '{print $1}' | tail -n 1)
   ```

## Cron Jobs:

```
SOURCE:
https://www.airplane.dev/blog/docker-cron-jobs-how-to-run-cron-inside-containers

VALUES:
* * * * * command to be executed
| | | | |______ Day of the Week (0 - 6) (Sunday to Saturday)
| | | |________ Month of the Year (1 - 12)
| | |__________ Day of the Month (1 - 31)
| |____________ Hour (0 - 23)
|______________ Minute (0 - 59)
```

## Build Image:

```
# go to repo's directory:
cd notify-cyber/

# build project's image:
docker build -t notify_cyber .

# run container:
docker run --name c_news -e POSTGRES_PASSWORD=password -d -p 5432:5432 notify_cyber

# exec into container:
docker exec -it $(docker ps | awk '{print $1}' | tail -n 1) bash

# stop container:
docker stop $(docker ps | awk '{print $1}' | tail -n 1)

# start container:
docker start $(docker ps -a | grep "notify_cyber" | awk '{print $1}')
```

## Useful Commands:

- psql:

  ```
  # list all databases:
  psql -U postgres
  \list
  \q

  # go into a database:
  psql --username postgres --dbname postgres
  \dt
  SELECT * FROM cybernews;
  ```

- git:
  ```
  # create a new branch based on an existing branch:
  #   - source: https://www.git-tower.com/learn/git/faq/create-branch
  git branch <new-branch> <base-branch>
  ```

## Sources:

- project layout:
  - https://github.com/app-generator/tutorial-flask/blob/main/flask-project-structure.md
  - https://towardsdatascience.com/build-deploy-a-react-flask-app-47a89a5d17d9

## Other Technolgoy Notes

### sql queries:

```
# count the total number of entries in the db
SELECT COUNT(*) FROM cybernews;

# count the total number of unique URL(s) in the db
SELECT COUNT(DISTINCT url) AS unique_url_count FROM cybernews;

# count the number of unique sources in the db
SELECT source, COUNT(*) AS count FROM cybernews GROUP BY source;
```

### psql commands:

```
# list all databases:
psql -U postgres
\list
\q

# go into a database:
psql --username postgres --dbname postgres
\dt
SELECT * FROM cybernews;
```

### git notes

```
# https://www.git-tower.com/learn/git/faq/create-branch
# create a new branch based on an existing branch:
git branch <new-branch> <base-branch>
```

### local python environments

1. Install and setup python3, pip3, and virtualenv on your machine
2. Setup python environment:
   ```
   python3 -m venv env
   ```
3. Active environment:
   ```
   source env/bin/activate
   ```
4. Install required python packages for this project by running this command:
   ```
   pip3 install -r requirements.txt
   ```
5. From here you can install and/or update any packages you want by using pip.
6. (optional) Update requirements.txt when ever you update or install a new pip package:
   ```
   pip3 freeze > requirements.txt
   ```
7. Deactivate environment:
   ```
   deactivate
   ```

## Old NC Setup Documentations

### About:

This file contains documentation for setting up certain deployments for Notify-Cyber.

### Collector Setup:

- Date: 5-14-2023

1. Get the machine/deployment ready for the collector. You can use something like a AWS EC2 instance or AWS Lambda. As of 5-14-2023, a Raspberry Pi 3B+ running on a local network is used. The collector only needs one instance so only one machine is needed for the collector to run. There SHOULD NOT be more then ONE collector running at once.

2. Make sure all dependencies are installed and setup. Know what you are doing, look though the code, or contact the developers to figure out how to do this. Good places to reference are the following:
   - notify-cyber/collector/requirements.txt
   - notify-cyber/.archive/pitools.sh

3. Initialize environment variables:

   ```
   source .env
   ```

4. Go to the collector directory:

   ```
   cd collector/
   ```

5. Clone the cvelist Github repo:

   ```
   git clone https://github.com/CVEProject/cvelist.git
   ```

6. Change the permission of the log file's parent directory:

- NOTE: Be careful here! Only one this on a single instance/deployment that is JUST running the Collector. DO NOT run this on your personal machine or a deployment running other processes.

  ```
  sudo chmod a+w /opt/
  ```

7. Run the collectory (background):

   ```
   python3 collector.py &
   ```

8. (optional) Kill the collector process:

   ```
   # list all python processes:
   ps -fA | grep "python" | grep -v 'grep'

   # look at the second row of the ps output for the pid (process id) for the collector process

   # kill the collector process:
   kill -9 <collector_pid>
   ```
