FROM ubuntu:22.04

# Prevent interactive prompts during apt installs
ENV DEBIAN_FRONTEND=noninteractive

# Install OpenSSH server, sudo, parallel-ssh, Open MPI, Python3, pip, and venv
RUN apt-get update && \
    apt-get install -y openssh-server sudo pssh \
                       libopenmpi-dev openmpi-bin openmpi-common \
                       python3 python3-pip python3-venv && \
    mkdir -p /var/run/sshd && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user with home directory and SSH folder
RUN useradd -m -s /bin/bash student && \
    mkdir -p /home/student/.ssh && \
    chown -R student:student /home/student

# Setup SSH directories (relying on Ubuntu 22.04 default SSH configuration)
RUN mkdir -p /root/.ssh

# Create Python virtual environment and install mpi4py
RUN python3 -m venv /root/mpi_env && \
    /root/mpi_env/bin/pip install --upgrade pip && \
    /root/mpi_env/bin/pip install mpi4py

# Generate SSH host keys
RUN ssh-keygen -A

# Expose port 22 for SSH
EXPOSE 22

# Start the SSH daemon in foreground when container runs
CMD ["/usr/sbin/sshd", "-D"]
