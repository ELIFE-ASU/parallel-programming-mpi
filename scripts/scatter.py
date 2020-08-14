from mpi4py import MPI

comm = MPI.COMM_WORLD

rank = comm.Get_rank()

if rank == 0:
    data = list(range(10))
    recv_data = comm.scatter(data)
else:
    recv_data = comm.scatter(None)

print(rank, recv_data)
