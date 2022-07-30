import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import openpyxl

# Config
st.set_page_config(
    page_title="GetAround Dashboard",
    page_icon=" 🕚 🚗 🕦",
    layout="wide"
)



# Set title and markdown 
st.title("GetAround Dashboard")
st.markdown('''DELAYS IMPACT ANALYSIS ON GETAROUND USERS''')

# Use `st.cache` to put data in cache
# The dataset will not be reloaded each time the app is refreshed
@st.cache(allow_output_mutation=True)
def load_data(nrows=''):
    data = pd.DataFrame()
    if(nrows == ''):
        data = pd.read_excel("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx")
    else:
        data = pd.read_excel("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx",nrows=nrows)

    return data



# Load the data
data_loading_status = st.text('Loading data...')
data = load_data()
data_loading_status.text('data_loaded ✔️')

# Data exploration with some informations about the dataset
st.subheader("DATA EXPLORATION")

# Run the below code if the check is checked ✅
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data) 

# Present the dataset
columns=" "
for column in data.columns:
    columns=columns+" "+str(column)+"/ "
st.markdown(f"""
    The dataset represent {len(data)} rental records.\n
    The informations contained are: {columns}""")


# Late checkouts proportions
# We can consider that negatif delays as in time 
st.subheader('LATE CHECKOUT PROPORTION')
data['checkout_status']=["Late" if x>0 else "in_time" for x in data.delay_at_checkout_in_minutes]
fig = px.pie(data, names='checkout_status', title='LATE CHECKOUT PROPORTION')
st.plotly_chart(fig)


# Delay at checkout repartition visualization
st.subheader('DELAY REPARTITION VISUALIZATION')
st.markdown("""Let's have a closer look to the delays repartition""")
choice = st.selectbox("select values to be displayed", ["all_values","values_without_outliers"])
data_with_delay=data[data.delay_at_checkout_in_minutes>0]
if choice=="all_values":
    # Graph showing the time passed in minutes before a late checkout
    fig = px.histogram(
        data_with_delay["delay_at_checkout_in_minutes"],
        x="delay_at_checkout_in_minutes")
    fig.update_layout()
    st.plotly_chart(fig, use_container_width=True)
    
    
else:
    # Graph showing the time passed in minutes before a late checkout
    fig = px.histogram(
        data_with_delay[
            (data_with_delay["delay_at_checkout_in_minutes"] <(2*data_with_delay['delay_at_checkout_in_minutes'].std()))
        ]["delay_at_checkout_in_minutes"],
        x="delay_at_checkout_in_minutes")
    fig.update_layout()
    st.plotly_chart(fig, use_container_width=True)



# Consecutive rentals
st.subheader("CONSECUTIVE RENTALS")


# Get one dataset with 
consecutive_rental_data = pd.merge(data, data, how='inner', left_on = 'previous_ended_rental_id', right_on = 'rental_id')

consecutive_rental_data.drop(
    [
        "delay_at_checkout_in_minutes_x",
        "rental_id_y", 
        "car_id_y", 
        "state_y",
        "time_delta_with_previous_rental_in_minutes_y",
        "previous_ended_rental_id_y",
        "checkout_status_x"
    ], 
    axis=1,
    inplace=True
)

consecutive_rental_data.columns = [
    'rental_id',
    'car_id',
    'checkin_type',
    'state',
    'previous_ended_rental_id',
    'time_delta_with_previous_rental_in_minutes',
    'previous_checkin_type',
    'previous_delay_at_checkout_in_minutes',
    "previous_checkout_status"
]

# Remove rows with missing previous rental delay values
consecutive_rental_data = consecutive_rental_data[~consecutive_rental_data["previous_delay_at_checkout_in_minutes"].isnull()]
consecutive_rental_data.reset_index(drop=True, inplace=True)

# Run the below code if the check is checked ✅
if st.checkbox('Show consecutive rental dataset'):
    st.write(consecutive_rental_data) 

# Count the number of consecutive rentals cases
st.markdown(f"""
    Let's have a look to the consecutive rentals to understand the impact of delays on next users.
 
    The total number of usable cases is: **{len(consecutive_rental_data)}**
""")



# Impacted users with previous delay
consecutive_rental_data['delayed_checkin_in_minutes']=[
    consecutive_rental_data.previous_delay_at_checkout_in_minutes[i]-consecutive_rental_data.time_delta_with_previous_rental_in_minutes[i] for i in range(len(consecutive_rental_data))
    ]

cancellation_df=consecutive_rental_data[
    (consecutive_rental_data["delayed_checkin_in_minutes"]>0) & (consecutive_rental_data["state"]=="canceled")
    ]

impacted_df= consecutive_rental_data[consecutive_rental_data.delayed_checkin_in_minutes>0]
st.markdown(f"""
    The number of checkins impacted by previous delays is:  **{len(impacted_df)}**

    The number of potential cancellations due to delays is:  **{len(cancellation_df)}**\n
    
    ---------------------------------------------------------------------------------\n

""")

#### Create two columns
col1, col2 = st.columns(2)

with col1:
    # Run the below code if the check is checked ✅
    if st.checkbox(' Histogram without outliers'):
        fig = px.histogram(
            impacted_df[impacted_df.delayed_checkin_in_minutes<2*impacted_df.delayed_checkin_in_minutes.std()],
            x="delayed_checkin_in_minutes", color="state",title='DELAYED CHECKIN'
            )
        st.plotly_chart(fig)        
    else:
        fig = px.histogram(impacted_df,x="delayed_checkin_in_minutes", color="state",title='DELAYED CHECKIN')
        st.plotly_chart(fig)

with col2:
    fig = px.pie(consecutive_rental_data, names='state', title='DELAYED CHECKIN STATUS')
    st.plotly_chart(fig)


# Threshold: minimum time between two rentals
st.subheader("Threshold testing")


# Threshold form
with st.form("Threshhold"):
    threshold = st.number_input("Threshold in minutes", min_value = 0, step = 1)
    checkin_type = st.selectbox("Checkin types", ["Connect only", "Mobile only","All"])
    submit = st.form_submit_button("submit")

    if submit:
        consecutive_rental_data_selected = impacted_df
        cancellation_df_selected= cancellation_df
        #select checkin type "connect"
        if checkin_type == "Connect only":
            consecutive_rental_data_selected = consecutive_rental_data_selected[consecutive_rental_data_selected["checkin_type"] == "connect"]
            cancellation_df_selected= cancellation_df[cancellation_df["checkin_type"] == "connect"]
        elif checkin_type == "Mobile only":
            consecutive_rental_data_selected = consecutive_rental_data_selected[consecutive_rental_data_selected["checkin_type"] == "mobile"]
            cancellation_df_selected= cancellation_df[cancellation_df["checkin_type"] == "mobile"]
        


        avoided_checkin_delays = len(consecutive_rental_data_selected[consecutive_rental_data_selected["delayed_checkin_in_minutes"] < threshold])
            
        avoided_cancellation = len(cancellation_df_selected[cancellation_df_selected["delayed_checkin_in_minutes"] < threshold])


        percentage_avoided_checkin_delays=round((avoided_checkin_delays/len(consecutive_rental_data_selected))*100, 1)
        precentage_avoided_cancellations=round((avoided_cancellation/len(cancellation_df_selected))*100, 1)
        st.markdown(f"""
            With a threshold of **{threshold}**minutes on **{checkin_type}** there is:
            - **{avoided_checkin_delays}** avoided checkin delays cases ({percentage_avoided_checkin_delays}% solved)
            - **{avoided_cancellation}** avoided cancellations (due to delays) cases ({precentage_avoided_cancellations}% solved)
        """)

