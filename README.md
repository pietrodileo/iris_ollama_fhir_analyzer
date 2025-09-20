# Running InterSystems IRIS with Docker: A Step-by-Step Guide - Part 1: From the Basics to Custom Dockerfile

This repository contains the source code and examples from **Article 1: From the Basics to Custom Code**, where we explore how to run [InterSystems IRIS](https://www.intersystems.com/products/intersystems-iris/) in Docker.

---

## What you’ll find here

- **Dockerfile** → builds a custom IRIS image with sample custom code.
- **docker-compose.yml** → runs IRIS with durable %SYS (persistent data on your host), custom password and exposed ports.
- **src/** → contains a simple class `DockerStepByStep.cheers`.
- **iris.script** → loads source classes at container startup.
- **logs/** → stores build logs redirected during image build.

## Requirements

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

## Quick start

1. Clone the repository:

   ```
   git clone https://github.com/pietrodileo/InterSystems-IRIS-with-Docker-A-Step-by-Step-Guide---Part-1.git
   ```
2. Pull the InterSystems IRIS Image from Docker Hub:

   ```
   docker pull intersystems/iris-community:latest-cd
   ```
3. Build and run the container

   ```
   docker compose up --build -d
   ```
4. Checks build logs:

   ```
   docker exec -it my-iris cat /opt/irisapp/logs/build.log
   ```
5. Access IRIS at the following URL:

   ```
   http://localhost:9092/csp/sys/UtilHome.csp
   ```

### Test the demo class

After the container is running, exec into IRIS and run the sayHi() method:

```
docker exec -it my-iris iris session IRIS
```

Inside the IRIS terminal:

```
ZN "USER"
Do ##class(DockerStepByStep.cheers).sayHi()
```

Expected output:

```
Hi mom!
```
