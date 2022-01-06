
import pandas as pd
import requests
import streamlit as st
import plotly.express as px



st.write("""
# Samad's TDI Milestone Project
### An interactive chart of stock closing prices using Streamlit and Plotly.""")

st.sidebar.header('Select Plot Parameters:')
symbol_inp = st.sidebar.text_input('Ticker (e.g. AAPL):','', placeholder='Enter a Ticker')

url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + symbol_inp +  "&outputsize=full&apikey=78W16YV9T26UZZGO"
if symbol_inp =='' :
  st.markdown(" #### **Error**: *Please enter a ticker*")
data = requests.get(url).json()
df = pd.DataFrame.from_dict(data)
df = df.drop(df.index[range(5)])
i = []
for x, y in df['Time Series (Daily)'].items():
  i.append([x, y['4. close']])
df = pd.DataFrame(i, columns = ['date', 'closing_price'])

df["date"] = pd.to_datetime(df["date"]).dt.normalize()
df['year'] = df["date"].dt.year
df['month'] = df["date"].dt.month
df['day'] = df["date"].dt.day



selected_year = st.sidebar.selectbox('Year', list(reversed(range(2010,2023))))
test = {"January":1, "February":2, "March":3, "April":4, "May":5, "June":6, "July":7, "August":8, "September":9, "October":10,
"November":11, "December":12}
selected_month = st.sidebar.selectbox('Months:', test.keys())

subdf = df.loc[(df['year']==selected_year) & (df['month']==test[selected_month])]
subdf.sort_values(["date"], ascending=False, inplace=True)
subdf.closing_price = subdf.closing_price.astype(float)


st.write(subdf)

"""### PLOTTING THE DATA"""
fig = px.line(subdf, x="date", y="closing_price")
st.write(fig)
