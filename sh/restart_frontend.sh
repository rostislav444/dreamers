docker compose -f docker-compose.frontend.yml down
docker compose -f docker-compose.frontend.yml build --no-cache
docker compose -f docker-compose.frontend.yml up -d
docker compose -f docker-compose.frontend.yml logs -f   # to see the logs