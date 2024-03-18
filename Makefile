
clean:
	docker-compose down

start:
	docker-compose up -d --build


restart:
	docker-compose down
	docker-compose up -d --build

debug:
	docker-compose up --build

