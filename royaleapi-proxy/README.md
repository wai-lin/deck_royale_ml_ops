# RoyaleAPI Proxy Server

RoyaleAPI only accept requests from white-listed IP Addresses.
Therefore, the purpose of this service is to act as an white-listed server
which just proxy the request to RoyaleAPI.

## Development

```
npm install
npm run dev
```

```
open http://localhost:3001
```

## Build and Push Docker Registry

```sh
# use buildx to build the universal container image
# NOTE: you only need to run this one time
docker buildx create --use

# build and push the registry to digital ocean
docker buildx build --platform linux/amd64,linux/arm64 -t registry.digitalocean.com/do-registery/hono-royaleapi-proxy:latest --push .
```

## Use Docker Image on Cloud

There're 2 ways to run the docker image on cloud.

- Using docker-compose (Recommended)

**_OR_**

- Manually run the container

### Using docker-compose (Recommended)

Create the following `docker-compose.yml` file in your hosting server.

```yaml
services:
  royaleapi-proxy:
    image: registry.digitalocean.com/do-registery/hono-royaleapi-proxy:latest
    ports:
      - "80:3001"
    environment:
      - API_KEY=${API_KEY}
      - ALLOWED_ORIGINS=${ALLOWED_ORIGINS}
      - API_KEY_1=${API_KEY_1}
      - API_KEY_2=${API_KEY_2}
      - API_KEY_3=${API_KEY_3}
    restart: unless-stopped
```

Create `.env` file with `API_KEY`.

```
API_KEY="your secure api key here"
```

Then you can run the container as usual with `docker-compose`.

- `docker compose pull` Pulling/Updating the latest image.
- `docker compose up -d` Running the image.
- `docker compose down` Stopping the image.

### Manually run the container

```
docker pull registry.digitalocean.com/do-registery/hono-royaleapi-proxy:latest
docker stop <id>
docker rm <id>
docker run -d -p 80:3001 registry.digitalocean.com/do-registery/hono-royaleapi-proxy:latest
```

## Check Logs

```
docker logs <id>
```
