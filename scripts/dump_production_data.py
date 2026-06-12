import urllib.request
import json
import urllib.parse
import os

workspace_dir = r"C:\Users\tiago\OneDrive\Documentos\Comparativo de legislações CBM"
output_json = os.path.join(workspace_dir, "database", "states_data.json")

# Ensure database directory exists
os.makedirs(os.path.dirname(output_json), exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def get_trpc(proc, inp):
    inp_str = json.dumps(inp)
    inp_encoded = urllib.parse.quote(inp_str)
    url = f"https://bombeiros-3mdsnvbm.manus.space/api/trpc/{proc}?batch=1&input={inp_encoded}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            res_str = response.read().decode('utf-8')
            res_json = json.loads(res_str)
            # tRPC returns an array in batch mode: [{"result": {"data": {"json": ...}}}]
            if isinstance(res_json, list) and len(res_json) > 0:
                return res_json[0].get("result", {}).get("data", {}).get("json")
            return res_json
    except Exception as e:
        print(f"Error fetching {proc} with input {inp}: {e}")
        return None

def main():
    print("Fetching states list from tRPC...")
    # states.list has empty input
    states_list = get_trpc("states.list", {})
    if not states_list:
        print("Failed to fetch states list.")
        return
        
    print(f"Found {len(states_list)} states in production database.")
    
    full_data = []
    
    for state in states_list:
        sigla = state.get("sigla")
        name = state.get("name")
        print(f"Fetching details for: {name} ({sigla})...")
        
        # input for states.details is {"0": {"json": {"sigla": sigla}}}
        details = get_trpc("states.details", {"0": {"json": {"sigla": sigla}}})
        if details:
            print(f"Successfully fetched details for {sigla}.")
            full_data.append(details)
        else:
            print(f"Failed to fetch details for {sigla}.")
            
    # Save the consolidated data to database/states_data.json
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(full_data, f, ensure_ascii=False, indent=2)
        
    print(f"\nConsolidated data successfully saved to: {output_json}")
    print(f"Total states consolidated: {len(full_data)}")

if __name__ == "__main__":
    main()
