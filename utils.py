from datetime import datetime

def log_action(action: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open("database/log.txt", "a") as f:
                f.write(f"{datetime.now()}: {action} - {func.__name__}\n")
            return result
        return wrapper
    return decorator

def apply_discount(price: float, discount_rate: float) -> float:
    return price * (1 - discount_rate)