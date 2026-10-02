import yaml, json

with open("service_catalog.yaml", "r") as f:
        data = yaml.safe_load(f)
       
healthy_services = []
status_counts = {"healthy": 0, "unhealthy": 0, "maintenance": 0}
for svc in data.get("services"):
    status = svc.get("status")
    if status in status_counts:
        status_counts[status] += 1        
    if status == "healthy":
        healthy_services.append(svc) 
healthy_names = sorted([s["name"] for s in healthy_services])
with open("healthy_services.json", "w") as f:
    json.dump({"services": healthy_services}, f, indent=4)    
print(f"Healthy: {status_counts['healthy']} | Unhealthy: {status_counts['unhealthy']} | Maintenance: {status_counts['maintenance']}")
print(f"Healthy services: {', '.join(healthy_names)}")