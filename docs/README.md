# N03 Open MPI PingPong on Linux Cluster - Beginner's Guide

## What is this project?

This project extends **N02** by adding **Open MPI** (Message Passing Interface) capabilities to the Linux cluster. It creates a **distributed computing environment** where 9 Docker containers work together using MPI to run a PingPong program. Instead of using real physical computers, we use **Docker containers** (like lightweight virtual machines) that communicate using SSH and MPI.

## 🏗️ What does the script do?

The `N03.txt` script automatically sets up 9 Linux environments with Open MPI installed in Python virtual environments and runs a PingPong program. Here's what happens when you run it:

### Steps 1-7: Cluster Setup (from N02) 🔧

These steps are identical to N02 and create the SSH cluster infrastructure:

1. **Generate SSH Keys** 🔑 - Creates passwordless authentication keys
2. **Create Dockerfile** 🏭 - Builds Ubuntu image with OpenSSH, Open MPI, and Python
3. **Build Docker Image** 🛠️ - Creates the container template
4. **Create Private Network** 🌐 - Sets up Docker bridge network
5. **Launch 9 Containers** 🚀 - Creates containers for MPI ranks 0-8
6. **Setup SSH Keys** 🔐 - Configures passwordless SSH in all containers
7. **Scan SSH Host Keys** 🤝 - Sets up host key verification

### Step 8: Python Virtual Environments 🐍

- Creates a Python virtual environment in each container (`/root/mpi_env`)
- Installs `mpi4py` package in each virtual environment
- This allows Python programs to use Open MPI for distributed computing

### Step 9: Copy PingPong Program 📋

- Copies the `pingpong.py` program to all containers
- This program implements the MPI PingPong logic

### Step 10: Create MPI Hostfile 📝

- Creates a hostfile listing all 9 container IP addresses
- Tells Open MPI which hosts are available and how many processes can run on each

### Step 11: Configure SSH for MPI 🔌

- Configures SSH to allow passwordless MPI communication between containers
- Open MPI uses SSH to launch processes on remote containers

### Step 12: Run PingPong Program 🎾

- Executes the PingPong program using `mpirun` with 9 processes:
  - **Rank 0 (Master)**: Sends random floats (0.00-180.00) to clients
  - **Ranks 1-8 (Clients)**: Receive numbers and echo them back to master
  - Master accumulates sum modulo 360
  - Continues until sum is between **270.505 and 270.515**
  - Prints the number of ping-pong message pairs to terminal and `RESULT.TXT`

### Step 13: Summary 📊

- Displays container information, MPI rank assignments, and execution statistics

## 🎾 What is the PingPong Program?

The PingPong program demonstrates **distributed computing** using MPI:

1. **Master (Rank 0)** generates 8 random floating-point numbers (0.00 to 180.00)
2. **Master sends** one number to each client (ranks 1-8)
3. **Clients receive** their number and **echo it back** to master
4. **Master receives** all 8 numbers and adds them to a running sum
5. The sum is kept **modulo 360** (like degrees on a circle)
6. Process repeats until the sum is between **270.505 and 270.515**
7. Final result: Number of ping-pong iterations required to reach the target range

**Example output:**
```
Master (rank 0) starting PingPong with 8 clients...
Number of ping-pong message pairs: 8915
```

## 🚀 How to Run It

### Prerequisites

- Docker must be installed and running
- Basic command line knowledge
- Python 3 (for understanding the program)

### Basic Usage

```bash
# Run the script (creates 9 containers automatically)
./N03.txt
```

**Note:** Unlike N02, N03 always creates exactly 9 containers (1 master + 8 clients for MPI ranks 0-8).

### What You'll See

The script will show progress through 13 steps, including:
- Docker image building with Open MPI
- Virtual environment creation
- MPI installation
- PingPong program execution
- Final results printed to terminal and saved to `RESULT.TXT`

```
Master (rank 0) starting PingPong with 8 clients...
Number of ping-pong message pairs: 8915

Results saved to RESULT.TXT:
Number of ping-pong message pairs: 8915
Final sum (modulo 360): 270.506406
```

## 🔧 Key Concepts Explained

### Open MPI 🚀

- **Message Passing Interface (MPI)**: Standard for parallel and distributed computing
- **Open MPI**: Open-source implementation of MPI
- Allows programs to run across multiple computers/containers
- Processes communicate by sending and receiving messages

### Virtual Environments 🐍

- **Python Virtual Environment**: Isolated Python environment for each container
- Prevents conflicts between different projects
- Contains its own Python packages (like `mpi4py`)
- Located at `/root/mpi_env` in each container

### MPI Ranks 🏷️

- Each MPI process gets a unique **rank** (number starting from 0)
- **Rank 0**: Usually the "master" or "coordinator" process
- **Ranks 1-8**: Worker or "client" processes
- Ranks communicate using `MPI.COMM_WORLD` (the global communicator)

### PingPong Pattern 🎾

- Classic MPI pattern: Master sends data → Workers process → Workers send back
- Demonstrates **bidirectional communication**
- Used in distributed algorithms and parallel computing

## 📁 Project Structure

```
/home/jokac/Desktop/Personal/FERI/Cloud Computing/N03-MPI Ping Pong/
├── N03.txt              # Main script (extends N02)
├── pingpong.py          # MPI PingPong Python program
├── Dockerfile           # Docker blueprint (created by script)
├── RESULT.TXT           # Output file (created after execution)
├── docs/                # Documentation
│   ├── README.md        # This file
│   ├── index.md         # Documentation index
│   └── ...              # Other documentation files
├── keydir/              # SSH keys
│   ├── my_key           # Private key
│   └── my_key.pub       # Public key
└── known_hosts          # SSH host fingerprints
```

## 🌐 MPI Communication Flow

```
┌─────────────────┐
│  Rank 0 (Master)│
│  172.20.0.2     │
└────────┬────────┘
         │
         ├─────────────┬─────────────┬─────────────┐
         │             │             │             │
    ┌────▼────┐  ┌────▼────┐  ┌────▼────┐  ┌────▼────┐
    │Rank 1   │  │Rank 2   │  │Rank 3   │  │Rank 4   │
    │172.20.0.3│  │172.20.0.4│  │172.20.0.5│  │172.20.0.6│
    └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘
         │             │             │             │
         └─────────────┴─────────────┴─────────────┘
                (and ranks 5, 6, 7, 8)

1. Master sends random numbers → Clients
2. Clients echo numbers back → Master
3. Master accumulates sum (modulo 360)
4. Repeat until sum ∈ [270.505, 270.515]
```

## 🧹 Cleanup

After you're done, clean up with these commands:

```bash
# Stop all containers
docker stop $(docker ps -q --filter 'name=ssh-container-')

# Remove all containers
docker rm $(docker ps -aq --filter 'name=ssh-container-')

# Remove network
docker network rm ssh-cluster-net-alt

# Remove Docker image
docker image rm linux-ssh-mpi-cluster
```

## 🔍 Understanding the Output

### PingPong Execution

```
Master (rank 0) starting PingPong with 8 clients...
Number of ping-pong message pairs: 8915
```

- **Master starting**: Rank 0 process begins coordination
- **8 clients**: Ranks 1-8 are ready to receive messages
- **8915 pairs**: Number of iterations needed to reach target sum range
- Each "pair" = Master sends to all 8 + receives from all 8

### RESULT.TXT

```
Number of ping-pong message pairs: 8915
Final sum (modulo 360): 270.506406
```

- First line: Number of ping-pong iterations
- Second line: Final accumulated sum (after modulo 360)
- The sum is guaranteed to be between 270.505 and 270.515

## 🎯 What You Learn

This project teaches:

- **Distributed Computing**: Running programs across multiple machines
- **MPI Programming**: Message passing between processes
- **Virtual Environments**: Python environment isolation
- **Network Configuration**: Docker networking for MPI
- **Parallel Algorithms**: Coordinating work across processes
- **Docker Containerization**: Multi-container orchestration
- **SSH Automation**: Passwordless remote execution

## ❓ Troubleshooting

### "Permission denied" errors

- Make sure you're in the correct directory
- Ensure the script is executable: `chmod +x N03.txt`

### Docker not running

```bash
# Check Docker status
sudo systemctl status docker

# Start Docker if needed
sudo systemctl start docker
```

### MPI execution fails

- Check that all 9 containers are running: `docker ps`
- Verify SSH keys are set up: `docker exec ssh-container-1 ls -la /root/.ssh/`
- Check virtual environment exists: `docker exec ssh-container-1 ls /root/mpi_env/`

### Virtual environment issues

```bash
# Verify mpi4py is installed
docker exec ssh-container-1 /root/mpi_env/bin/pip list | grep mpi4py
```

### MPI process launch errors

- Ensure SSH is working between containers
- Check known_hosts file is present: `docker exec ssh-container-1 cat /root/.ssh/known_hosts`

## 📚 Further Reading

- [Open MPI Documentation](https://www.open-mpi.org/doc/)
- [MPI4py Documentation](https://mpi4py.readthedocs.io/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [Docker Networking](https://docs.docker.com/network/)
- [MPI Tutorial](https://computing.llnl.gov/tutorials/mpi/)

## 🔗 Related Projects

- **N02**: Base SSH cluster setup (prerequisite)
- This project extends N02 with MPI capabilities

---

**Congratulations!** You've just set up a distributed computing cluster using Open MPI. This demonstrates real parallel computing concepts used in high-performance computing (HPC), scientific simulations, and cloud computing platforms. 🚀

---

*Documentation created for Cloud Computing course - FERI*  
*Last updated: N03 Open MPI PingPong version*
