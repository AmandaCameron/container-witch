Container Witch is a simple tool to take a running docker container list and generate config files for it.

Right now, this is limited to just nginx configs, but I plan to extend this as the needs increase.

It is a pre-packaged container available on the [Docker Hub](http://hub.docker.com) and is designed to be run inside a container with
access to the host's docker.sock.

It works by polling the /containers endpoint every 15 seconds and checking the running containers. If it spies a container running an image that it wants, it makes a file for the nginx config. If the container goes away, it removes the file. It was designed to ease the pain of setting up a nginx reverse proxy into containers we have started setting up at DarkDNA.

It uses a config file that looks something like this:

    blag:
      image: wordpress:latest
      http:
        host: blag.example.com
        port: 80