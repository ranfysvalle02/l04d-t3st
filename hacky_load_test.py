"""  
    Sends a GET request to a server and returns the HTTP status code.  
    This function is intended for responsible load testing only.  
"""  
import ray,requests;ray.init()  
@ray.remote  
def f():return requests.get(f'http://localhost:1020/?query=testing').status_code  
print(ray.get([f.remote()for _ in range(3)]))  
"""
	INFO worker.py:1821 -- Started a local Ray instance.
[200, 200, 200]
"""
# Reminder: Always use this script in a controlled environment and with permission from the server owner.  
# Note: The requests made by this script will be logged by the server, making it easy to identify   
# the load testing activity. Use responsibly to avoid any unintended consequences.  
