docker build . -t web-service-message-votes
docker run --rm -it -p 5000:5000 web-service-message-votes