""" 
- max_threads
- (task_id, fn, deps, timeout)

    queue = asyncio.Queue()
    tasks = []
    for i in range(3):
        task = asyncio.create_task(worker(f'worker-{i}', queue))
        tasks.append(task)
    await queue.join()
    for task in tasks:
        task.cancel()
"""
import asyncio
from collections import defaultdict


class Task:
    def __init__(self, tid: int, timeout: int, deps: list[int]):
        self.tid = tid
        self.timeout = timeout
        self.deps = deps
        async def fn():
            print(f"task {self.tid} (dep {self.deps}) done")
        self.fn = fn

tasks = [
    Task(0, .5, []),
    Task(1, 1, [0]),
    Task(2, .1, [0]),
]
queue = asyncio.Queue()  # task_id
tid_task: dict[int, Task] = {}
tid_map = defaultdict(list)
tid_deps = {}
for t in tasks:
    tid_task[t.tid] = t
    tid_deps[t.tid] = len(t.deps)
    for dep in t.deps:
        tid_map[dep].append(t.tid)
    if len(t.deps) == 0:
        print(f"queue: adding task {t.tid}")
        queue.put_nowait(t.tid)
async def worker(wid: int):
    while tasks:
        print(f"worker {wid} getting task...")
        tid = await queue.get()
        print(f"worker {wid} got task {tid}")
        task = tid_task[tid]
        try:
            await asyncio.wait_for(task.fn(), task.timeout)
            # handle the deps
            for dep_tid in tid_map[tid]:
                tid_deps[dep_tid] -= 1
                if tid_deps[dep_tid] == 0:
                    queue.put_nowait(dep_tid)
                    print(f"queue: adding task {dep_tid}")
        except Exception as e:
            print(f"task {tid} failed: {e}. canelling {tid_map[tid]}")
            # failed, cancel all the dep tasks
            for t in tid_map:
                tid_task.pop(t)
    
                

async def main():
    max_threads = 2
    await asyncio.gather(*[worker(i) for i in range(max_threads)])

asyncio.run(main())