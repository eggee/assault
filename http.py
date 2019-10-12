# Make the request and return the results
import asyncio
import time

def fetch(url):
    """ Make a request to a url/webpage and return the connections results (ie. 200-OK)"""
    pass

def worker(name, queue, results):
    """ # A function to take unmade requests from a queue, perform the work, and then add result to the queue """
    pass

async def distribute_work(url, requests, concurrency, results):
    """ Distribute Work will divide up work into batches and collect final results """

    # instantiate a 'queue' using asycnio queue Class to hold all the jobs you want to run
    # which are the 'requests per url'
    queue = asyncio.Queue()

    # Add items into the queue. One item each for the # of requests given from the CLi input
    # Best thought of as a to-do list that the workers will pull from
    for _ in range(requests):   # the '_' is used when you don't really care, or use, the value.
        queue.put_nowait(url)

    # Create the 'task list' for however many concurrent jobs given
    tasks = []
    for i in range(concurrency):
        task = asyncio.create_task(worker(f"worker-{i+1}", queue, results))
        tasks.append(task)

    # Run the queue
    # start a timer execute the queue and calculate how much time each worker took.
    started_at = time.monotonic() # monotonic - think of it like a stop-watch, independant of AM/PM or timezones
    await queue.join()    # execute everything inside the queue.
    total_time = time.monotonic() - started_at # calculate time after finishing everything in the queue

    # now that the queue is finish, cancel each task from the tasks list
    for task in tasks:
        task.cancel()

    # output human readable information
    print("---")
    print(
        f"{concurrency} workers took {total_time:.2f} seconds to complete {len(results)} requests"
    )

# Entrypoint to making requests
def assault(url, requests, concurrency):
    results = []
    asyncio.run(distribute_work(url, requests, concurrency, results))
    print(results)