import altair as alt
from BLEInterface import BLEInterface
import heartpy as hp
import matplotlib.pyplot as plt
import pandas as pd
import platform
from streamz import Stream
from streamz.dataframe import DataFrame, PeriodicDataFrame

# TODO: config file
ADDRESS = (
    "F4:12:FA:5A:81:D1"
    if platform.system() != "Darwin"
    # Service ID
    else "0000180d-180d-1000-8000-00805f9b34fb"
)
IO_CONFIG_CHAR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

ble_interface = BLEInterface(ADDRESS)

class stream_data():
    """
    Description: Stream data class holds the streamlit state system, BLE interface, and the streaming dataframe
    """

    def __init__(self):
        self.ble_interface = ble_interface













stream = Stream()
df_signal = pd.DataFrame({'Time_sec': [], 'Signal': []})
df_stream = DataFrame(stream, example=df_signal)

# Example data
# first let's load the clean PPG signal
data, timer = hp.load_exampledata(2)

# run the example analysis
sample_rate = hp.get_samplerate_datetime(timer, timeformat='%Y-%m-%d %H:%M:%S.%f')
wd, metrics = hp.process(data, sample_rate=sample_rate, report_time=True)

df_signal = pd.DataFrame({'Time_sec': timer, 'Signal': data})
df_signal["Time_sec"] = pd.to_datetime(df_signal["Time_sec"], format='%Y-%m-%d %H:%M:%S.%f', errors='coerce')
df_stream = DataFrame(stream, example=df_signal)

def get_df_signal(**kwargs):
    if st.session_state.click_connect:
        df_signal = ble_interface.read_gatt()
        return df_signal
    else:
        df_signal = pd.DataFrame([])

df = PeriodicDataFrame(get_df_signal, interval='300ms')