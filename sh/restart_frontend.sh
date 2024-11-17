docker compose -f docker-compose.frontend.yml down
docker compose -f docker-compose.frontend.yml up --build -d
docker compose -f docker-compose.frontend.yml logs -f