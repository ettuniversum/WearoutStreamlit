from BLEInterface import BLEInterface
import platform
import streamlit as st
import time

ADDRESS = (
    "F4:12:FA:5A:81:D1"
    if platform.system() != "Darwin"
    # Service ID
    else "0000180d-180d-1000-8000-00805f9b34fb"
)
IO_CONFIG_CHAR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

st.title("Wearout: Connect to BLE")

if 'click_connect' not in st.session_state:
    st.session_state.click_connect = False
if 'click_disconnect' not in st.session_state:
    st.session_state.click_disconnect = False

def click_connect_button():
    st.session_state.click_connect = True

def click_disconnect_button():
    st.session_state.click_disconnect = True

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



if st.button('Disconnect', key=2, on_click=click_disconnect_button) and st.session_state.click_disconnect:
    ble_interface.close_connection()
    st.session_state.click_disconnect = False
