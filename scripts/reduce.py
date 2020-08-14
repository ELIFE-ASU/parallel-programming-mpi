from mpi4py import MPI

comm = MPI.COMM_WORLD

rank = comm.Get_rank()

if rank == 0:
    data = rank
    recv_data = comm.reduce(data, op=MPI.SUM)
else:
    data = rank
    recv_data = comm.reduce(data)

print(rank, recv_data)
