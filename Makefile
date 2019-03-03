all:
	docker build . --network host
	heroku container:login
	heroku container:push -a debian-preseed-generator web --context-path .
	heroku container:release web -a debian-preseed-generator
