from functools import wraps

def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "No such name in contacts."
        except ValueError as e:
            return f"{e}"
        except IndexError:
            return "Enter user name."
        except Exception as e:
            return f"{e}"
    return inner
