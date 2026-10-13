import json
import pandas as pd
import plotly.express as px
import streamlit as st
from core import analyze, demo, summary, alert_intervals

st.set_page_config(page_title='Flight Telemetry Analyzer', page_icon='✈️', layout='wide')
st.title('Flight Telemetry Analyzer')
st.caption('Flight log inspection · SI units · synthetic demonstration flight')
file = st.sidebar.file_uploader('Upload flight CSV', type='csv')
st.sidebar.markdown('Required: `time_s`, `altitude_m`, `airspeed_ms`, `battery_pct`')
alt = st.sidebar.number_input('Altitude threshold (m)', value=120.0)
bat = st.sidebar.slider('Battery threshold (%)', 0, 100, 20)
st.sidebar.download_button('Download example CSV', demo().to_csv(index=False), 'example_flight.csv', 'text/csv')
try:
    if file and file.size > 20_000_000: raise ValueError('Please use a CSV smaller than 20 MB.')
    data = analyze(pd.read_csv(file) if file else demo(), alt, bat)
except (ValueError, TypeError, UnicodeError, pd.errors.ParserError) as exc:
    st.error(str(exc)); st.stop()
stats = summary(data)
columns = st.columns(4)
for col, label, value in zip(columns, ['Duration', 'Peak altitude', 'Air-relative distance', 'Battery used'],
                            [f'{stats["duration_s"]:.0f} s', f'{stats["peak_altitude_m"]:.1f} m', f'{stats["air_distance_m"]/1000:.2f} km', f'{stats["battery_used_pct"]:.1f} percentage points']):
    col.metric(label, value)
plots, alerts, raw, exports = st.tabs(['Flight plots', 'Alerts & quality', 'Data', 'Export'])
with plots:
    for field in ['altitude_m', 'airspeed_ms', 'battery_pct', 'vertical_speed_ms']:
        figure = px.line(data, x='time_s', y=field, template='plotly_dark')
        if field == 'altitude_m': figure.add_hline(y=alt, line_dash='dash')
        if field == 'battery_pct': figure.add_hline(y=bat, line_dash='dash')
        st.plotly_chart(figure, width='stretch')
with alerts:
    st.info('Intervals group consecutive flagged samples. Their bounds are observed timestamps; they do not establish the exact crossing time.')
    for field in ['altitude_alert', 'battery_alert', 'time_gap_alert']:
        st.subheader(field.replace('_', ' ').title())
        intervals = alert_intervals(data, field)
        if intervals: st.dataframe(pd.DataFrame(intervals), width='stretch')
        else: st.success('No flagged samples.')
    st.write('Sampling gap threshold: three times the median sample interval. Gradients across large gaps can be less reliable.')
with raw: st.dataframe(data, width='stretch')
with exports:
    st.download_button('Analyzed CSV', data.to_csv(index=False), 'analysis.csv', 'text/csv')
    st.download_button('Summary JSON', json.dumps(stats, indent=2), 'summary.json', 'application/json')
    st.json(stats)
