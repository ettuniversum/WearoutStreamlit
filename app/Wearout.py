import datetime
import streamlit as st
from pandas import DataFrame


column_one, column_two = st.columns(2)
with column_one:
    st.title("Wearout")
    st.markdown("""#### Wearout was born from the MakerSpace Community. Leveraging Adafruit's Qt Py, our favorite 'lil chip, paired with the Pulse Sensor's open source hardware a over-the-ear heart rate sensor came to life.""")

with column_two:
    st.markdown("[![Click me](./app/static/CG_Heart.gif)](https://streamlit.io)")

def create_dataframe(signal):
    now = datetime.datetime.now()
    data_now = {'Time_sec': now, 'Signal': signal}
    df_now = DataFrame([data_now], columns=data_now.keys())
    return df_now





if __name__ == "__main__":
    pass