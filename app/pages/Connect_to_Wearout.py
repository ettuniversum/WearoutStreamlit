import altair as alt
from pandas import DataFrame, concat
from backend.BLEInterface import BLEInterface
import platform
import streamlit as st


ADDRESS = (
    "F4:12:FA:5A:81:D1"
    if platform.system() != "Darwin"
    # Service ID
    else "0000180d-180d-1000-8000-00805f9b34fb"
)
IO_CONFIG_CHAR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

st.title("Connect to Wearout")

tab_one, tab_two = st.tabs(['Connect to BLE', 'Dashboard'])

with tab_one:

    if 'click_connect' not in st.session_state:
        st.session_state.click_connect = False
    if 'click_disconnect' not in st.session_state:
        st.session_state.click_disconnect = False

    def click_connect_button():
        st.session_state.click_connect = True

    def click_disconnect_button():
        ble_interface.close_connection()
        st.session_state.click_disconnect = False

    ble_interface = BLEInterface(ADDRESS)

    if st.button('Connect', key=1, on_click=click_connect_button):
        with st.status("Retrieving Device List...", expanded=True) as status:
            # Connect to BLE
            bool_found = ble_interface.found_device()
            if bool_found:
                st.write("Found device...")
            else:
                st.write("Did not find device. Reset device.")
            bool_connect = ble_interface.setup_connection()
            if bool_connect:
                st.write("Connection established")
                st.session_state.click_connect = True

            else:
                st.write("Connection to device failed")

    if st.button('Disconnect', key=2, on_click=click_disconnect_button):
        st.session_state.click_disconnect = True




chart_row = st.empty()

while st.session_state.click_connect:
    # Init sample
    df_sample = DataFrame([])
    # Retrieve 1000 samples
    for i in range(20):
        df = ble_interface.read_gatt()
        df_sample = concat([df_sample, df])
    df_sample = df_sample.reset_index(drop=True)
    c = alt.Chart(df_sample).mark_circle().encode(
        x='Time_sec', y='Signal', color='Signal')

    chart_row.altair_chart(c, use_container_width=True)

