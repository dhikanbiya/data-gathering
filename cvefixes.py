import os
import re
import json
import argparse
from cpgqls_client import CPGQLSClient, import_code_query

client = CPGQLSClient("localhost:8088")

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



def main(): 


    parser = argparse.ArgumentParser(description="Run Joern client on Java files within a base folder.")
    parser.add_argument(
        "--base_folder",
        type=str,
        required=True,
        help="Base directory containing subfolders with Java files (e.g., downloads/extracted_vulnerable)"
    )
    
    args = parser.parse_args()

    # base_folder = "/Users/danbiya/Documents/datasets/SARD/downloads/nv"
    base_folder = args.base_folder

    # Only include files ending with ".java" (case-insensitive)
    java_files = [f for f in os.listdir(base_folder) if f.lower().endswith(".java")]

    # Directories for output AST and CPG
    ast_dir = os.path.join(base_folder, "ast")
    cpg_dir = os.path.join(base_folder, "cpg")
    os.makedirs(ast_dir, exist_ok=True)
    os.makedirs(cpg_dir, exist_ok=True)

    for f in java_files:
        # Get the full path to the Java file
        java_file_full = os.path.join(base_folder, f)
        # Get the base filename without the extension
        base_filename = os.path.splitext(f)[0]
        

        # Generate output filenames with _cpg and _ast suffixes
        cpg_filename = os.path.join(cpg_dir, base_filename + "_cpg.json")
        ast_filename = os.path.join(ast_dir, base_filename + "_ast.json")

         # Check if both files already exist and are non-empty, then skip this file.
        if (os.path.exists(ast_filename) and os.path.getsize(ast_filename) > 0) and \
           (os.path.exists(cpg_filename) and os.path.getsize(cpg_filename) > 0):
            print(f"Skipping {java_file_full}: AST and CPG files already exist.")
            continue


        # Import the code into Joern for the given project (using the base filename as project name)
        query = import_code_query(java_file_full, base_filename)
        result_import = client.execute(query)
        
        # Execute the CPG query for methods
        cpg_query = "cpg.method.toJsonPretty"
        result_cpg = client.execute(cpg_query)
        cleaned_cpg = clean_output(result_cpg['stdout'])
        
        # Execute the AST query for methods
        ast_query = "cpg.method.ast.toJsonPretty"
        result_ast = client.execute(ast_query)
        cleaned_ast = clean_output(result_ast['stdout'])
        
        
        
        # Save the cleaned outputs to the respective files
        with open(cpg_filename, "w") as f_out:
            f_out.write(cleaned_cpg)
        
        with open(ast_filename, "w") as f_out:
            f_out.write(cleaned_ast)
        
        print(f"Processed {java_file_full}. \n Saved CPG to {cpg_filename} \n Saved AST to {ast_filename}.")
    print("\n\n=====Processing complete.======")

if __name__ == "__main__":
    main()