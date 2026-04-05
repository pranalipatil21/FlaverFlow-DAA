# Greedy Job Scheduling
def job_scheduling_deadlines(jobs):
    # jobs: list of {'name', 'deadline', 'profit'}
    jobs = sorted(jobs, key=lambda x: x['profit'], reverse=True)
    max_d = max(j['deadline'] for j in jobs)
    result = [None] * max_d
    for job in jobs:
        for j in range(min(max_d, job['deadline']) - 1, -1, -1):
            if result[j] is None:
                result[j] = job['name']
                break
    return [r for r in result if r is not None]