import sys, argparse, requests
from registry_client import RegistryClient

def main():
    parser = argparse.ArgumentParser(description="Update and deregister a service")
    parser.add_argument("id", type=int, help="The service ID to deregister")
    args = parser.parse_args()
    client = RegistryClient()

    try:
        svc_before = client.get_service(args.id)
        before_status = svc_before.get("status", "unknown")
        client.patch_service(args.id, {"status": "maintenance"})
        svc_after = client.get_service(args.id)
        after_status = svc_after.get("status", "unknown")
        print(f"Status before: {before_status}")
        print(f"Status after: {after_status}")
        client.delete_service(args.id)
        print(f"Deregistered {svc_after.get('name')} (id {args.id})")
    except requests.exceptions.HTTPError as exc:
        if exc.response is not None and exc.response.status_code == 404:
            print(f"Service id {args.id} not found, nothing to do.")
            sys.exit(0)
        else:
            print(f"HTTP Error: {exc}")
            sys.exit(0)
    except requests.exceptions.RequestException:
        print("Error: Could not connect to the registry server.")
        sys.exit(0)
if __name__ == "__main__":
    main()