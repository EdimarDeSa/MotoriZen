from datetime import datetime
from functools import wraps


def print_progress(*args) -> None:
    formatted_args = [str(arg).center(25) for arg in args]

    print(
        "Progress:".ljust(12),
        *formatted_args,
        sep=" │ ",
        end="\r",
    )


def with_progress(description: str = ""):
    def decorator(test_func):
        @wraps(test_func)
        def wrapper(*args, **kwargs):
            initial_time = datetime.now()
            # Imprime uma linha vazia antes do teste
            print()

            # Se houver descrição, imprime
            if description:
                print(f"🚀 {description}")

            try:
                result = test_func(*args, **kwargs)
            finally:
                final_time = datetime.now()
                total_time = (final_time - initial_time).total_seconds()
                print()
                print(f"Time: {total_time:.2f}s")

            return result

        return wrapper

    return decorator
