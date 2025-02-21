# uni-bi

## Usage:


### To run locally create .env file in project root with:

MYSQL_ROOT_PASSWORD=chooseWisely

MYSQL_DATABASE=bi

MYSQL_USER=bi_user

MYSQL_PASSWORD=chooseWisely



### Pull images:

podman image pull ghcr.io/isithin/bi-db:demo

podman image pull ghcr.io/isithin/bi-scraper:demo

podman image pull ghcr.io/isithin/bi-ui:demo



### Run Containers:

podman-compose up -d
