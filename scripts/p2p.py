from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    msg = {'a': 1, 'b': [1, 2, 3]}
    comm.send(msg, dest=1, tag=1)
else:
    msg = comm.recv(source=0, tag=1)
    print(rank, msg)
