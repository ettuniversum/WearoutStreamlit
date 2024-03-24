import pandas as pd
from datetime import datetime
import asyncio

async def print_time():
    while True:
        print(datetime.now().time())
        await asyncio.sleep(1)

async def print_int():
# I would like this to return the full 10x2 dataframe
    col_1 = []
    col_2 = []
    for i in range(10):
        col_1.append(i)
        col_2.append(2*i)
        print(i)
        await asyncio.sleep(1)
    return col_1

async def main():
    # how can I catch and process the 10x2 dataframe returned by print_int()?
    # this will get the other co-routine running in the background:
    asyncio.create_task(print_time())
    result = await print_int()
    pass

if __name__ == "__main__":
    asyncio.run(main())