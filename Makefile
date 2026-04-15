run-dev-server: 
	fastapi dev app/main.py

build-image: 
	docker build -t splitaroo-api .

run-image: 
	docker run splitaroo-api
