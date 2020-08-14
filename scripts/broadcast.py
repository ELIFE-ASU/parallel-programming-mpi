from mpi4py import MPI

comm = MPI.COMM_WORLD

rank = comm.Get_rank()

if rank == 0:
    data = list(range(10))
else:
    data = None

recv_data = comm.bcast(data)
print(rank, recv_data)
