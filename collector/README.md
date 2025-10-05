# Notify Cyber - Collector Deployment

## About

This is a Notify Cyber deployment that scrapes the internet for cybersecurity news. It then cleans up and processes the data it has scraped so that it can be structured and added to the project's database. The collector builds the database and keeps it updated.

## Links

- [Docker](https://www.docker.com/)
- [OpenAI](https://platform.openai.com/settings/organization/usage/legacy)
- [Supabase](https://supabase.com/dashboard/projects)
- [Linode](https://www.linode.com/pricing/)
- [Vercel](https://vercel.com/)
- [WebcrawlingAPI](https://dash.webcrawlerapi.com/stats)

## How To Run

**Quick Start**: Run `./start.sh` to automatically build and run the Docker container.

**Manual Setup**:

1. Make sure to be in the root directory of this project, use the **cd** command.

2. Add your **.env**, refer to **.env_template** to figure out what keys you need.

3. Install and setup [Docker](https://www.docker.com/)

   **Note**: For host setup on Linode or Raspberry Pi, see the `./host/` directory for automated setup scripts and configuration.

4. Build the docker image for this project:

```bash
docker build -t nc-collector .
```

5. Run the docker image as a container:

```bash
docker run -d nc-collector
```

6. Run this command to get a list of all running containers:

```bash
docker ps
```

7. You can also exec into the container if you want with this command:

```bash
docker exec -it nc-collector bash
```

8. If you want to get the logs of a container, run these commands:

```bash
# get the id for the container
docker ps

# print logs
docker logs <container_name_or_id>
```

9. If you want to kill the container, run these commands:

```bash
# get the id for the container
docker ps

# kill the container
docker kill <container_name_or_id>
```
