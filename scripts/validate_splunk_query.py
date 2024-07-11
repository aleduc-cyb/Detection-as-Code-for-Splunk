import yaml
import sys
import splunklib.client as client
import os

def test_query_syntax(file_path, service):
    with open(file_path, 'r') as file:
        query = yaml.safe_load(file)
    
    try:
        # Use the oneshot method to test the search syntax
        search_results = service.jobs.oneshot(query['search'])
        print(f"Syntax valid for query in {file_path}")
        return True
    except Exception as e:
        print(f"Syntax error in query {file_path}: {str(e)}")
        return False

def main(files_to_check):
    # Connect to Splunk
    service = client.connect(
        host=os.environ['SPLUNK_HOST'],
        port=os.environ['SPLUNK_PORT'],
        username=os.environ['SPLUNK_USERNAME'],
        password=os.environ['SPLUNK_PASSWORD']
    )

    all_valid = True
    for file_path in files_to_check:
        if file_path.endswith('.yml') and file_path.startswith('queries/'):
            if not test_query_syntax(file_path, service):
                all_valid = False
    
    if not all_valid:
        exit(1)

if __name__ == "__main__":
    files_to_check = sys.argv[1:]
    if not files_to_check:
        print("No files to check")
        exit(0)
    main(files_to_check)