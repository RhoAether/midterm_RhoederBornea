import argparse,requests
from registry_client import RegistryClient

def fetch_all(client, status=None):
    collected, offset, limit = [], 0, 10
    while True:
        page = client.get_services(limit=limit, offset=offset, status=status)
        collected.extend(page["results"])
        offset += limit
        if offset >= page["count"]:
            break
    return collected

def run_inventory():
    parser = argparse.ArgumentParser()
    parser.add_argument("--status", default=None)
    args = parser.parse_args()
    client = RegistryClient()   
    try:
        services = fetch_all(client, status=args.status)
        print(f"{'ID':<4} | {'NAME':<20} | {'VERSION':<8} | {'STATUS':<12} | {'ENVIRONMENT'}")
        print("-" * 70)
        for svc in services:
            print(f"{svc.get('id', 'N/A'):<4} | {svc.get('name', 'N/A'):<20} | {svc.get('version', 'N/A'):<8} | {svc.get('status', 'N/A'):<12} | {svc.get('environment', 'N/A')}")
    except requests.exceptions.RequestException:
        print("Error: Could not connect to the registry or invalid API key provided.")
        sys.exit(0)