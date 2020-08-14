from mpi4py import MPI

comm = MPI.COMM_WORLD

rank = comm.Get_rank()

if rank == 0:
    data = rank**2
    recv_data = comm.gather(data, root=1)
else:
    data = rank**2
    recv_data = comm.gather(data, root=1)

print(rank, recv_data)
