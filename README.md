# bongzy-API

1. Create `lta.env` file with the sample config:
`AccountKey=xxxxxx`

2. To build:
`docker build -t bongzy-api .`

3. To run:
`docker run -p 4656:4656 --name bongzy_api -e TZ=Asia/Singapore -d bongzy-api`

4. If using docker-compose:
`docker-compose up --build -d`

5. Application will be exposed in port 4656