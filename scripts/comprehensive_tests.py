import splunklib.client as client
import splunklib.results as results
import time
import json
import os
import sys

def connect_to_splunk():
    return client.connect(
        host=os.environ['SPLUNK_HOST'],
        port=os.environ['SPLUNK_PORT'],
        username=os.environ['SPLUNK_USERNAME'],
        password=os.environ['SPLUNK_PASSWORD']
    )

def performance_test(service, query, time_limit=60):
    start_time = time.time()
    job = service.jobs.create(query)
    while not job.is_done():
        if time.time() - start_time > time_limit:
            job.cancel()
            return False, f"Query exceeded time limit of {time_limit} seconds"
    execution_time = time.time() - start_time
    return True, f"Query executed in {execution_time:.2f} seconds"

def false_positive_test(service, query, test_data):
    # Assuming test_data is a list of events that should or should not trigger the alert
    job = service.jobs.create(query, earliest_time=test_data['start_time'], latest_time=test_data['end_time'])
    reader = results.ResultsReader(job.results())
    results = [result for result in reader if isinstance(result, dict)]
    
    if test_data['should_trigger'] and not results:
        return False, "Alert failed to trigger on test data"
    elif not test_data['should_trigger'] and results:
        return False, "Alert incorrectly triggered on test data"
    return True, "Alert behaved correctly on test data"

def main(files_to_check):
    service = connect_to_splunk()
       
    for file_path in files_to_check:
        print(f"Testing query: {file_path}")
        
        perf_result, perf_message = performance_test(service, query)
        print(f"Performance test: {'Passed' if perf_result else 'Failed'} - {perf_message}")
        
        fp_result, fp_message = false_positive_test(service, query, {
            'start_time': '-1h',
            'end_time': 'now',
            'should_trigger': True
        })
        print(f"False positive test: {'Passed' if fp_result else 'Failed'} - {fp_message}")
        
        print("\n")

if __name__ == "__main__":
    files_to_check = sys.argv[1:]
    if not files_to_check:
        print("No files to check")
        exit(0)
    main(files_to_check)