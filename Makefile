run-dev-server: 
	fastapi dev app/main.py

build-image: 
	docker build -t splitaroo-api .

run-image: 
	docker run splitaroo-api

lint: 
	black . --check

fix-lint: 
	black . 

build-image: 
	docker build

run-image: 
	docker run -p 8080:8080 splitaroo