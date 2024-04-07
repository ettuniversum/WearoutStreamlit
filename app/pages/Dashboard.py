import heartpy as hp
import matplotlib.pyplot as plt
import streamlit as st
st.set_option('deprecation.showPyplotGlobalUse', False)

class Dashboard:

    def __init__(self, st):
        self.streamlit_obj = st

    def load_example_data(self):
        # Example data
        # first let's load the clean PPG signal
        data, timer = hp.load_exampledata(0)
        # run the example analysis
        wd, metrics = hp.process(data, sample_rate=100.0)


    def create_dash(self):
        # creating a single-element container.
        placeholder = st.empty()

        with placeholder.container():
            # create three columns
            kpi1, kpi2, kpi3 = st.columns(3)

            # fill in those three columns with respective metrics or KPIs
            kpi1.metric(label="BPM :heart:", value=round(metrics['bpm']), delta=round(metrics['bpm']))
            kpi2.metric(label="IBI :disney:", value=int(metrics['ibi']))
            kpi3.metric(label="Breathing Rate :smiley:", value=round(metrics['breathingrate']))

            column_one, column_two = st.columns(2)

            with column_one:
                #and visualise
                fig, ax = plt.subplots()
                ax.plot(data)
                st.pyplot(fig=fig)

            with column_two:
                #call plotter
                fig = hp.plotter(wd, metrics)
                st.pyplot(fig=fig)

#while ble_connected: # how to access this all the time?
#   pull streaming data # stream from read_gatt
#   create_dashboard # render the data that is stremed