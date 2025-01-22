import ray,requests;ray.init()  
@ray.remote  
def f():return requests.get('http://localhost:1020').status_code  
print(ray.get([f.remote()for _ in range(1000)]))  
