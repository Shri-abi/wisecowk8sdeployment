FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Install correct netcat version and dependencies
RUN apt-get update && \
    apt-get install -y \
    bash \
    netcat-openbsd \
    fortune-mod \
    cowsay && \
    ln -s /usr/games/fortune /usr/local/bin/fortune && \
    ln -s /usr/games/cowsay /usr/local/bin/cowsay && \
    rm -rf /var/lib/apt/lists/*

# Force override of nc by symlinking nc.openbsd
RUN ln -sf /bin/nc.openbsd /usr/local/bin/nc

COPY wisecow.sh /wisecow.sh
RUN chmod +x /wisecow.sh

EXPOSE 4499

CMD ["/wisecow.sh"]

