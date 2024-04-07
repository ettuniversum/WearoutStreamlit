import datetime
import streamlit as st
from pandas import DataFrame


column_one, column_two = st.columns(2)
with column_one:
    st.write("[![Click me](./app/static/CG_Heart_2.gif)]()", width=400)

with column_two:
    st.title("Wearout")
    st.markdown(
        """#### Wearout was born from the MakerSpace Community. A over-the-ear heart rate sensor came to life, leveraging Adafruit's Qt Py chip paired with the Pulse Sensor's open source hardware""")

if __name__ == "__main__":
    pass