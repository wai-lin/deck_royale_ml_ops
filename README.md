# Deck Royale

## How to run with `docker-compose`

1. clone `.env.example` file with new name `.env`.
2. Add `empty` environment variables only. (You don't have to modify the prefilled ones unless necessary. It's already configured to work inside docker).
3. Run `docker compose up -d --build`.

#### Checking

You can check whether the docker is running with one of the following options.

- Option 1:
    - Try visiting the (backend api docs)[http://localhost:8000/docs]. You should see swagger UI and also try to play around with some api to make sure the backend is working.
    - Try visiting the (mlflow dashboard)[http://localhost:5001]. You should see the MLFlow dashboard.
- Option 2:
    - Run the command `docker ps`. The status of services should be `Up`.

## Development

After running the project with `docker compose up -d` or `docker compose up -d --build`,
You can just develop the project locally the docker should reload itself whenever there's file changes.

> NOTE: You might have to run `docker compose up -d --build` again
> when you added new environment variable in `.env` file
> OR when you've updated the environment variable value.
