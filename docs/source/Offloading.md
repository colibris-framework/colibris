# Offloading

Running time-consuming, blocking tasks can be done by using the `taskqueue` functionality in separate workers. The
`TASK_QUEUE` variable in `${PACKAGE}/settings.py` configures the background running task mechanism. Background tasks
are disabled by default.

## Usage

To run a background task, import the `taskqueue` wherever you need it:

    from colibris import taskqueue
    
Then run your time consuming task:

    def time_consuming_task(arg1, arg2):
        time.sleep(10)
    
    ...
    
    try:
        result = await taskqueue.execute(time_consuming_task, 'value1', arg2='value2', timeout=20)
    
    except Exception as e:
        handle_exception(e)

## RQ Backend

Make sure to have the `rq` and `redis` python packages installed.

In `${PACKAGE}/settings.py`, set:

    TASK_QUEUE = {
        'backend': 'colibris.taskqueue.rq.RQBackend',
        'host': '127.0.0.1',
        'port': 6379,
        'db': 0,
        'password': 'yourpassword',
        'poll_results_interval': 1
    }

## Background Worker

To actually execute the queued background tasks, you'll need to spawn at least one worker:

    ./${PACKAGE}/manage.py runworker
