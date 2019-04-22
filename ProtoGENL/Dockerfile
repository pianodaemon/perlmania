FROM ubuntu:bionic
MAINTAINER miriam.physics@gmail.com


# getting last software catalog, upgrade and install java
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y  software-properties-common && \
    apt-get update --fix-missing
RUN apt-get install -y openjdk-8-jre maven tomcat9

RUN mkdir -p /app

WORKDIR /app

COPY . /app

RUN mvn package

WORKDIR /app/target

EXPOSE 8080

CMD ["java", "-jar", "ProtoGENL-0.0.1-SNAPSHOT.jar", "-httpPort=8080"]
