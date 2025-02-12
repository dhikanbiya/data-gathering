import os
import re
import json
import argparse
from cpgqls_client import CPGQLSClient, import_code_query

def clean_output(output):
    # Remove any ANSI escape sequences (e.g. color codes)
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    output = ansi_escape.sub('', output)
    
    # Find the first occurrence of '[' and the last occurrence of ']'
    start = output.find('[')
    end = output.rfind(']')
    if start == -1 or end == -1:
        return output  # fallback if not found
    return output[start:end+1]

def write_log(message, global_log):
    print(message)
    with open(global_log, "a") as f:
        f.write(message + "\n")

def main():
    parser = argparse.ArgumentParser(description="Run Joern client on Java files within a base folder.")
    parser.add_argument(
        "--base_folder",
        type=str,
        required=True,
        help="Base directory containing subfolders with Java files (e.g., downloads/extracted_vulnerable)"
    )
    parser.add_argument(
        "--server_endpoint",
        type=str,
        default="localhost:8088",
        help="Joern server endpoint (default: localhost:8088)"
    )
    args = parser.parse_args()

    base_folder = args.base_folder
    server_endpoint = args.server_endpoint
    client = CPGQLSClient(server_endpoint)
    
    # Define the global log file in the base folder.
    global_log = os.path.join(base_folder, "log.txt")
    
    # Clear previous log content if exists.
    open(global_log, "w").close()

    # Walk through the base folder (only one level deep subfolders are processed)
    for folder in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder)
        if not os.path.isdir(folder_path):
            continue

        # If both JSON files already exist in the folder, skip it.
        ast_json = os.path.join(folder_path, "exported-ast.json")
        cpg_json = os.path.join(folder_path, "exported-cpg.json")
        if os.path.exists(ast_json) and os.path.exists(cpg_json):
            write_log(f"Skipping {folder_path}: JSON files already exist.", global_log)
            continue

        # Look for .java files in the folder
        java_files = [f for f in os.listdir(folder_path) if f.endswith('.java')]
        if not java_files:
            write_log(f"Skipping {folder_path}: no Java file found.", global_log)
            continue

        # Choose the first java file
        java_file = os.path.abspath(os.path.join(folder_path, java_files[0]))
        # Use the folder name as the project name for import_code_query
        project_name = folder

        write_log(f"Processing {java_file} as project '{project_name}'", global_log)
        
        # Import the code; this returns a query that is executed against Joern
        query = import_code_query(java_file, project_name)
        result_import = client.execute(query)
        # Pretty print the import query response
        formatted_import = json.dumps(result_import, indent=4)
        # write_log("Import executed. Response:\n" + formatted_import, global_log)
        
        # Perform a CPG query to list all methods in the code
        cpg_query = "cpg.method.toJsonPretty"
        result_cpg = client.execute(cpg_query)
        # write_log("CPG query executed.", global_log)
        
        # Perform an AST query
        ast_query = "cpg.method.ast.toJsonPretty"
        result_ast = client.execute(ast_query)
        # write_log("AST query executed.", global_log)

        cleaned_ast = clean_output(result_ast['stdout'])
        cleaned_cpg = clean_output(result_cpg['stdout'])

        # Save the results in the folder containing the Java file
        with open(ast_json, "w") as f:
            f.write(cleaned_ast)
        with open(cpg_json, "w") as f:
            f.write(cleaned_cpg)

        write_log(f"{project_name} exported", global_log)
        # write_log(f"Saved AST to {ast_json}", global_log)
        # write_log(f"Saved CPG to {cpg_json}", global_log)

    write_log("All folders processed.", global_log)

if __name__ == "__main__":
    main()


