import asyncio
from i2c_comm_constants import *


# from smbus2 import SMBus


async def write_data_to_arduino():
    print("write_data_to_arduino_start")
    await asyncio.sleep(1)
    print("write_data_to_arduino_end")


async def read_data_from_arduino():
    print("read_data_from_arduino_start")
    await asyncio.sleep(1)
    print("read_data_from_arduino_end")
