import inspect


def strict(func):
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)

        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        for param in sig.parameters.values():
            if param.annotation != type(bound_args.arguments[param.name]):
                raise TypeError(f'{bound_args.arguments[param.name]} not {param.annotation}')

        return func(*args, **kwargs)

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


@strict
def my_func(a: bool, b: int, c: float, d: str):
    return a, b, c, d


@strict
def another_func(a: int, b: str):
    return a + len(b)


try:
    print(sum_two(1, 2))  # >>> 3
    print(sum_two(1, 2.4))  # >>> TypeError
    print(my_func(True, 10, 3.14, "hello"))  # >>> True, 10, 3.14, "hello"
    print(my_func(True, "10", 3.14, "hello"))  # >>> TypeError
    print(my_func(1, 10, 3.14, "hello"))  # >>> TypeError
    print(another_func(10, "test"))  # >>> 10, "test"
    print(another_func("10", "test"))  # >>> TypeError
except TypeError as e:
    print(f"Ошибка: {e}")
