# Week07 / onClass — Code-First and Design-First demos

## Run both with Docker

From this `onClass` directory:

python -m flask --app app run --debug --port 5000
python -m flask --app app run --debug --port 8080

```powershell
docker compose up --build -d
docker compose ps
```

- Code-First Swagger UI: http://localhost:5000/swagger-ui
- Code-First API: http://localhost:5000/products/
- Design-First OpenAPI UI (Connexion default): http://localhost:8080/ui/
- Design-First API: http://localhost:8080/products

Example PowerShell tests (both services):

```powershell
Invoke-RestMethod http://localhost:5000/products/
Invoke-RestMethod http://localhost:8080/products
Invoke-RestMethod -Method Post -Uri http://localhost:5000/products/ -ContentType 'application/json' -Body '{"name":"Keyboard","price":50}'
Invoke-RestMethod -Method Post -Uri http://localhost:8080/products -ContentType 'application/json' -Body '{"name":"Keyboard","price":50}'
```

Stop:

```powershell
docker compose down
```

These are in-memory demo APIs. Product changes reset when the corresponding process/container restarts. Code-First is Flask + flask-smorest; Design-First is Connexion + OpenAPI YAML. No database is used in either demo.

If a port is already occupied by Lab01 or another application, stop it before running these two services, or change only the host-side port binding (left side in compose) and use that new URL.

## Run without Docker

Create separate Python virtual environments for each subdirectory, install each `requirements.txt`, then run `python app.py` from that subdirectory. The two demos need separate working directories because both have an `api` package.
