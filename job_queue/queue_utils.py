import os
import redis
from rq import Queue
from worker import conn  # Assuming the worker.py file contains your Redis connection

# Initialize the queue
queue = Queue(connection=conn)

def enqueue_job(job_function, *args, **kwargs):
    """
    Enqueue a job to be processed by the worker.
    
    :param job_function: The function to execute.
    :param args: Arguments for the job function.
    :param kwargs: Keyword arguments for the job function.
    :return: Job instance
    """
    job = queue.enqueue(job_function, *args, **kwargs)
    return job

def get_job_status(job_id):
    """
    Get the status of a job by its job ID.
    
    :param job_id: The ID of the job.
    :return: The status of the job (e.g., 'queued', 'in-progress', 'finished', etc.)
    """
    job = queue.fetch_job(job_id)
    if job:
        return job.get_status()
    return 'Job not found'

def job_result(job_id):
    """
    Retrieve the result of a completed job.
    
    :param job_id: The ID of the job.
    :return: The result of the job, if finished, otherwise None.
    """
    job = queue.fetch_job(job_id)
    if job and job.is_finished:
        return job.result
    return None
