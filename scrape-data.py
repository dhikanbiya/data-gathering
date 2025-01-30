import json

# Function to load JSON data from a file
def load_json_from_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data



# Example usage
file_path = 'sample.json'
json_data = load_json_from_file(file_path)

for i in range(len(json_data['testCases'])):

    download = json_data['testCases'][i]['download']
    # taxa = json_data['testCases'][i]['sarif']['runs']['taxonomies']['taxa'][0]
    taxa = json_data['testCases'][i]['sarif']['runs'][0]['taxonomies'][0]['taxa'][0]
    print(f"{download} {taxa}") 

    # print(json_data['testCases'][i]['download']json_data['testCases'][i]['sarif']['runs']['taxonomies']['taxa'][0])



# print(len(json_data['testCases']))
    


