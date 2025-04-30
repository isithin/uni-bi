# uni-bi

## Usage:

To run locally create .env file in project root and source it before running the containers with the following variables

### Environment Variables:

MYSQL_ROOT_PASSWORD=chooseWisely

MYSQL_DATABASE=bi

MYSQL_USER=bi_user

MYSQL_PASSWORD=chooseWisely

GF_DATABASE_USER=grafanaReader

GF_DATABASE_PASSWORD=chooseWisely


### Pull image:

podman image pull ghcr.io/isithin/bi-scraper:demo



### Run Containers:

podman-compose up -d

### Cautions:

- sometimes you need to take them down and up again because of the db initialisation
- the scraping process can take quite some time (depending on the amount of information available)
- if the python_container exits wit code 0 the scraping is completed
