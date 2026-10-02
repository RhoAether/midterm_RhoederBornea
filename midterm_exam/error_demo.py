import sys, requests
from registry_client import RegistryClient

def main():
    print("--- 1. Triggering HTTP 401 Unauthorized ---")
    try:
        bad_client = RegistryClient(api_key="wrong-key")
        bad_client.get_services()
    except requests.exceptions.HTTPError as exc:
        if exc.response is not None and exc.response.status_code == 401:
            print("What happened: Request failed with HTTP 401 Unauthorized.")
            print("Probable cause: Invalid API key ('wrong-key') passed to RegistryClient.")
        else:
            print(f"HTTP Error: {exc}")
    except requests.exceptions.RequestException as err:
        print(f"Connection failed: {err}")
    print("\n--- 2. Triggering HTTP 404 Not Found ---")
    try:
        good_client = RegistryClient()
        good_client.get_service(9999)
    except requests.exceptions.HTTPError as exc:
        # Pattern P5: Inspect response status code
        if exc.response is not None and exc.response.status_code == 404:
            print("What happened: Request failed with HTTP 404 Not Found.")
            print("Probable cause: Service ID 9999 does not exist in the registry catalog.")
        else:
            print(f"HTTP Error: {exc}")
    except requests.exceptions.RequestException as err:
        print(f"Connection failed: {err}")
    sys.exit(0)
if __name__ == "__main__":
    main()