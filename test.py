import os
a = "E:/path"
b = "path/a"
print(os.path.join(a,b))
from typing import Mapping
def print_two(i:int) -> Mapping[int, int]:
    i += 1
    return i, i-1