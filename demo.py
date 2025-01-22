import ray,requests;ray.init()  
@ray.remote  
def f():return requests.get(f'http://localhost:1020/?query=testing').status_code  
print(ray.get([f.remote()for _ in range(3)]))  
