import array
import asyncio
from BLEInterface import BLEInterface
import datetime
from pandas import DataFrame
import signal
import streamlit as st
import sys
import time
from bleak import BleakClient, BleakGATTCharacteristic
import platform

#st.title("Hello World")

ADDRESS = (
    "F4:12:FA:5A:81:D1"
    if platform.system() != "Darwin"
    # Service ID
    else "0000180d-180d-1000-8000-00805f9b34fb"
)
IO_CONFIG_CHAR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"



def create_dataframe(signal):
    now = datetime.datetime.now()
    data_now = {'Time_sec': now, 'Signal': signal}
    df_now = DataFrame([data_now], columns=data_now.keys())
    return df_now

def main():
    try:
        # Connect to BLE
        ble_interface = BLEInterface(ADDRESS)
        client = ble_interface.establish_connection(ADDRESS)
        df = ble_interface.return_dataframe()
        print(df)
    except KeyboardInterrupt:
        ble_interface.close_connection()



if __name__ == "__main__":
    main()