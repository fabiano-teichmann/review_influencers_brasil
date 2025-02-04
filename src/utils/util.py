import time

def timing_decorator(method):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = method(*args, **kwargs)
        end_time = time.time()
        print(f"Method `{method.__name__}` executed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper
