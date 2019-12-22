from typing import Union


def edit(message: Union[str, None], time: Union[str, None],
         mins: Union[str, None], colored: bool) -> None:
    print(f'message={repr(message)}')
    print(f'time={repr(time)}')
    print(f'mins={repr(mins)}')
    print(f'colored={repr(colored)}')
