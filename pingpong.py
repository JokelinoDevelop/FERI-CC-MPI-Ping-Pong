#!/usr/bin/env python3
"""
Open MPI PingPong Program
Master (rank 0) sends random floating point numbers to clients (ranks 1-8).
Clients send numbers back to master, which accumulates sum modulo 360.
Continues until sum is between 270.505 and 270.515.
"""

from mpi4py import MPI
import random

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    # Ensure we have exactly 9 processes (1 master + 8 clients)
    if size != 9:
        if rank == 0:
            print(f"Error: This program requires exactly 9 processes, but {size} were started.")
        return
    
    ping_pong_count = 0
    total_sum = 0.0
    
    if rank == 0:
        # Master process
        print(f"Master (rank 0) starting PingPong with {size - 1} clients...")
        
        while True:
            ping_pong_count += 1
            
            # Send random float (0.00 to 180.00) to each client
            numbers_sent = []
            for client_rank in range(1, 9):
                random_number = random.uniform(0.00, 180.00)
                numbers_sent.append(random_number)
                comm.send(random_number, dest=client_rank, tag=1)
            
            # Receive numbers back from all clients
            numbers_received = []
            for client_rank in range(1, 9):
                received_number = comm.recv(source=client_rank, tag=2)
                numbers_received.append(received_number)
            
            # Add received numbers to sum by modulo 360
            for num in numbers_received:
                total_sum = (total_sum + num) % 360.0
            
            # Check if sum is in target range
            if 270.505 <= total_sum <= 270.515:
                # Send termination signal to all clients
                for client_rank in range(1, 9):
                    comm.send(-1.0, dest=client_rank, tag=1)
                break
        
        # Print results
        result_message = f"Number of ping-pong message pairs: {ping_pong_count}"
        print(result_message)
        
        # Write to RESULT.TXT
        with open("RESULT.TXT", "w") as f:
            f.write(result_message + "\n")
            f.write(f"Final sum (modulo 360): {total_sum:.6f}\n")
    
    else:
        # Client processes (ranks 1-8)
        while True:
            # Receive number from master (with termination check)
            # Master sends -1.0 as termination signal
            received_number = comm.recv(source=0, tag=1)
            
            # Check for termination signal
            if received_number < 0:
                break
            
            # Send number back to master
            comm.send(received_number, dest=0, tag=2)

if __name__ == "__main__":
    main()
