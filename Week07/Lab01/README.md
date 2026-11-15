docker compose up --build -d
docker compose logs -f api
docker compose down
http://localhost:5000/healthz
http://localhost:5000/ready
http://localhost:5000/swagger-ui