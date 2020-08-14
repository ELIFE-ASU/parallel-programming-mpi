---
title: Parallel Processing with OpenMPI
author: Douglas G. Moore
patat:
    wrap: true
    theme:
        imageTarget: [onDullWhite, vividRed]
...

# Parallel Processing with OpenMPI

MPI is the best option when you need to scale your computation beyond
one computer.

# Concurrency vs Parallelism

In computation, there's a difference between doing things "concurrently"
and doing things "in parallel".

# Concurrency

Concurrency is about structuring your program in terms of "components"
that can be executed in any order, allowing the runtime to decide when to
"context switch" between them.

These independent components are sometimes called "coroutines" or "tasks".

```javascript
async function create_remote(url) {
    <create an empty remote on GitHub>
}

async function create_repo(template_dir) {
    <create local repository>
}

(function() {
    let github = create_remote(...);
    let local = create_repo(...);
    Promise.all([github, local]).then(() => publish_repo(...)).except((err) => console.log(err));
}());
```

The `create_remote` and `create_repo` function will run "concurrently",
meaning that the runtime environment is free to execute them in any order,
and even interupt one to work on the other, e.g. while create_remote
waits for Github to respond.

# Parallelism

Parallelism is related in that a concurrent program can almost always
be run in parallel, with appropriate synchronization points.

```julia
using Distributed
add_procs(2)

function create_remote(url)
    <create an empty remote on Github>
end

function create_repo(templatedir)
    <create local repository>
end

function main()
    github = @spawn create_remote(...)
    localrep = @spawn create_repo(...)

    foreach(wait, [github, localrep])
    publish_repo(...)
end
```

The `create_remote` and `create_repo` methods are run on different
processes, meaning they can be executed at the same time without blocking
one another (provided you have enough free CPU cores).

# Models of Parallelism

There are three classes of parallel computing: threaded, distributed and GPU
computing.

Under the threading model:

- A "root" or "parent" process spawns some number of "worker" subprocesses
- The root and workers share a memory space
- Pros:
    - shared memory is fast and fairly easy (if processes only **read**)
- Cons:
    - shared memory is a nightmare (if processes have to **write**)
    - limited to one machine (physical or virtual)

Under the distributed model:

- A number of independent processes are spawn
- Data is shared and computation is coordinated via messages sent
  between processes
- Pros:
   - Easier to avoid race conditions
   - Processes can (in principle) run on any machine anywhere
- Cons:
   - Message passing has a greater runtime cost than shared memory

Under the GPU model:

- Graphics processing units are used in place of the CPU
- GPUs have a huge number of relatively dump control units
- Pros:
   - Very fast if what you're parallelizing is "simple", e.g. matrix
     multiplication
- Cons:
   - Very slow if the units of computation have complex logic, e.g. lots of if
     statements
   - Confined to a single machine unless combined with distributed computing

# Message Passing Mechanisms

1. Interprocess Communication

    - Generally provided by the operating system
    - Some APIs allow remote procedure calls (similar to `@spawn`)

2. Message Passing Interface (MPI)

    - An API specification
    - Two big implementations: OpenMPI and MPICH
    - Standard on compute clusters

# MPI Techniques

1. Point-to-Point Communications

    - One process specifically sends a message to another process
    - Can be blocking (synchronous) or non-blocking (asynchronous)

2. Collective Communication

    - One process sends data to all processes in a group
    - One process receives data from all processes in a group

# What we'll do today

MPI is a fairly large specification and API. There's no way we could
cover everything in a single session. Some of what we'll cover include

1. Sending and Recieving point-to-point communication
2. Broadcasing, Scattering, Gathering, and Reducing (collective communication)

Unfortunately, we probably won't discuss

- Barriers (used for synchronization)
- Communication Groups (think of these as teams of processes that like
  to work together)
- MPI-facilitated Input/Output
- Dynamic Process Management

All code will be written in Python using the
[mpi4py](https://mpi4py.readthedocs.io/en/stable/index.html) package.

Documentation of the full OpenMPI API can be found
[here](https://www.open-mpi.org/doc/current/)
