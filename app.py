import streamlit as st
import pandas as pd
import plotly.express as px
from core import analyze, demo

st.set_page_config(page_title='Flight Telemetry Analyzer', layout='wide')
st.title('Flight Telemetry Analyzer')
st.caption('Inspect flight logs and configurable engineering thresholds. Demo data is synthetic.')
file = st.sidebar.file_uploader('Upload CSV', type='csv')
alt = st.sidebar.number_input('Altitude threshold (m)', value=120.0)
bat = st.sidebar.slider('Battery threshold (%)', 0, 100, 20)
try:
    data = analyze(pd.read_csv(file) if file else demo(), alt, bat)
except (ValueError, TypeError, pd.errors.ParserError) as exc:
    st.error(str(exc))
    st.stop()
cols = st.columns(3)
cols[0].metric('Duration', f'{data.time_s.iloc[-1]-data.time_s.iloc[0]:.0f} s')
cols[1].metric('Peak altitude', f'{data.altitude_m.max():.1f} m')
cols[2].metric('Lowest battery', f'{data.battery_pct.min():.1f}%')
for field in ['altitude_m', 'airspeed_ms', 'battery_pct', 'vertical_speed_ms']:
    st.plotly_chart(px.line(data, x='time_s', y=field), width='stretch')
st.subheader('Samples exceeding thresholds')
st.dataframe(data[data.altitude_alert | data.battery_alert], width='stretch')
st.download_button('Download analyzed CSV', data.to_csv(index=False), 'analysis.csv', 'text/csv')
