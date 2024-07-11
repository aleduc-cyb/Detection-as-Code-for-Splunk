import yaml
import sys

def validate_query(file_path):
    with open(file_path, 'r') as file:
        query = yaml.safe_load(file)
    
    required_fields = ['name', 'description', 'search', 'schedule']
    for field in required_fields:
        if field not in query:
            return False, f"Missing required field: {field}"
    
    # Add more validation as needed
    
    return True, "Query is valid"

def main(files_to_check):
    for file_path in files_to_check:
        if file_path.endswith('.yml') and file_path.startswith('queries/'):
            is_valid, message = validate_query(file_path)
            if not is_valid:
                print(f"Error in {file_path}: {message}")
                exit(1)
            else:
                print(f"Validated: {file_path}")
    
    print("All specified queries are valid")

if __name__ == "__main__":
    files_to_check = sys.argv[1:]
    if not files_to_check:
        print("No files to check")
        exit(0)
    main(files_to_check)