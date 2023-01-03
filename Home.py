import streamlit as st 
import plotly.express as px
import pandas as pd
from datetime import datetime as dt
import time
from plotly.subplots import make_subplots
from urllib.request import urlopen 
import plotly.graph_objects as go
from PIL import  Image
import json
import requests
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
st.set_page_config(
 page_title="Osmosis Analysis",
 layout="wide",
 initial_sidebar_state="expanded"
)
new_users=pd.read_json("https://node-api.flipsidecrypto.com/api/v2/queries/786af7d7-2485-48b7-9db6-57c30f6ccc6a/data/latest")
action_type=pd.read_json("https://node-api.flipsidecrypto.com/api/v2/queries/ddf37478-2972-452e-baa7-946ba855ea72/data/latest")
swap_by_project=pd.read_json("https://node-api.flipsidecrypto.com/api/v2/queries/db6f1ac4-d4ee-4dfd-bbc6-d06275a8d204/data/latest")
transfers_by_pool=pd.read_json("https://node-api.flipsidecrypto.com/api/v2/queries/33ee1bd9-30d4-4659-a306-4b2ec1a8e4a4/data/latest")
transfers_by_chain=pd.read_json("https://node-api.flipsidecrypto.com/api/v2/queries/5975fc1a-02ad-4760-9741-d7373fb98f6d/data/latest")
volume_transfers_by_chain = pd.read_json("https://node-api.flipsidecrypto.com/api/v2/queries/7bf635c0-1e91-4844-b183-82e5d587d7d3/data/latest")
trace1 = go.Bar(x=new_users['MIN_DAY'], 
 y=new_users['NEW_USERS'],
 name='Number of new Users')
trace2 = go.Scatter(x=new_users['MIN_DAY'], 
y=new_users['CUME_USERS'],
mode='lines',
line=dict(color='red'),
name='Number of cumulative new users')
new_users_fig = go.Figure()
new_users_fig = make_subplots(specs=[[{"secondary_y": True}]])
new_users_fig.add_trace(trace1,secondary_y=False)
new_users_fig.add_trace(trace2,secondary_y=True)
new_users_fig.update_layout(title="Osmosis New Users",
  xaxis_title="DATE",
  yaxis_title="NEW USERS",
  yaxis2_title="CUMULATIVE USERS")
chain_transfers_fig = px.area(transfers_by_chain, 
 x='DAY', 
 y='TRANSFERS', 
 color='CHAIN_TYPE')
chain_transfers_fig.update_layout(title="Number of transfers to OSMOSIS by chain",
  xaxis_title="DAY",
  yaxis_title="TRANSFERS")
chain_normalized_transfers_fig = px.area(transfers_by_chain, 
 x='DAY', 
 y='TRANSFERS', 
 color='CHAIN_TYPE', 
 groupnorm='percent')
chain_normalized_transfers_fig.update_layout(title="Normalized Number of transfers to OSMOSIS by chain",
  xaxis_title="DAY",
  yaxis_title="TRANSFERS(%)")
chain_transfers_pie_fig = px.pie(transfers_by_chain,
names='CHAIN_TYPE',
values='TRANSFERS'
)
chain_transfers_pie_fig.update_layout(title="Number of transfers to Osmosis by chain",
  xaxis_title="Chain",
  yaxis_title="Number of transfers")
chain_transfers_pie_fig.update_traces(textposition='inside', textinfo='value+percent+label')
chain_volume_transfers_fig = px.area(volume_transfers_by_chain, 
 x='DAY', 
 y='VOLUME', 
 color='CHAIN_TYPE')
chain_volume_transfers_fig.update_layout(title="Volume of transfers to OSMOSIS by chain",
  xaxis_title="DAY",
  yaxis_title="VOLUME")
chain_volume_normalized_transfers_fig = px.area(volume_transfers_by_chain, 
 x='DAY', 
 y='VOLUME', 
 color='CHAIN_TYPE', 
 groupnorm='percent')
chain_volume_normalized_transfers_fig.update_layout(title="Normalized volume of transfers to OSMOSIS by chain",
  xaxis_title="DAY",
  yaxis_title="VOLUME(%)")
chain_volume_transfers_pie_fig = px.pie(volume_transfers_by_chain,
names='CHAIN_TYPE',
values='VOLUME'
)
chain_volume_transfers_pie_fig.update_layout(title="Volume of transfers to Osmosis by chain",
  xaxis_title="Chain",
  yaxis_title="Volume of transfers")
chain_volume_transfers_pie_fig.update_traces(textposition='inside', textinfo='value+percent+label')
action_type_fig = px.bar(action_type, 
x='WEEK', 
y = 'COUNT(*)', 
color='ACTION_TYPE'
)
action_type_fig.update_layout(title="First actions by new Osmosis Users",
  xaxis_title="Week",
  yaxis_title="Number of Actions")
action_type_normalized_fig = px.area(action_type, 
 x='WEEK', 
 y='COUNT(*)', 
 color='ACTION_TYPE', 
 groupnorm='percent')
action_type_normalized_fig.update_layout(title="Normalized first actions by new Osmosis Users",
  xaxis_title="Week",
  yaxis_title="Number of Actions")
action_type_first_fig = px.histogram(action_type, 
x='ACTION_TYPE', 
y = 'COUNT(*)', 
color = 'ACTION_TYPE', 
title="Number of users by first action", 
log_y = False)
action_type_first_fig_pie = px.pie(action_type,
names='ACTION_TYPE',
values='COUNT(*)'
)
action_type_first_fig_pie.update_layout(title="Distribution of users by first action",
  xaxis_title="Action",
  yaxis_title="Number of users")
action_type_first_fig_pie.update_traces(textposition='inside', textinfo='percent+label')
first_asset_swapped_to_fig = px.bar(swap_by_project, 
x='WEEK', 
y = 'COUNT(*)', 
color='PROJECT_NAME',
)
first_asset_swapped_to_fig.update_layout(title="Asset that users first swapped to",
  xaxis_title="WEEK",
  yaxis_title="Number of swappers")
normalized_first_asset_swapped_to_fig = px.histogram(swap_by_project.dropna(subset=['PROJECT_NAME']), 
 x='WEEK', 
 y='COUNT(*)', 
 barnorm='percent', 
 color='PROJECT_NAME')
normalized_first_asset_swapped_to_fig.update_layout(title="Normalized First Asset Swapped To",
  xaxis_title="WEEK",
  yaxis_title="Number of swappers",
  bargap=0.1)
first_asset_swapped_to_fig_pie = px.pie(swap_by_project,
names='PROJECT_NAME',
values='COUNT(*)'
)
first_asset_swapped_to_fig_pie.update_layout(title="Number of Osmosis users by first asset swapped to",
  xaxis_title="Asset",
  yaxis_title="Swappers")
first_asset_swapped_to_fig_pie.update_traces(textposition='inside', textinfo='percent+value+label')
first_asset_swapped_to_fig_multi = px.histogram(swap_by_project, 
x='PROJECT_NAME', 
y = 'COUNT(*)', 
color = 'PROJECT_NAME',
log_y = False)
first_asset_swapped_to_fig_multi.update_layout(title="Number of swappers by first asset swapped to",
  xaxis_title="Asset",
  yaxis_title="Swappers")
first_pool_deposited_to_fig = px.bar(transfers_by_pool.astype({'POOL': 'string'}), 
x='WEEK', 
y = 'COUNT(*)', 
color='POOL'
)
first_pool_deposited_to_fig.update_layout(title="New Osmosis LPs by First Pool Deposited",
  xaxis_title="WEEK",
  yaxis_title="Number of Deposits")
normalized_first_pool_deposited_to_fig = px.histogram(transfers_by_pool.dropna(subset=['POOL']), 
 x='WEEK', 
 y='COUNT(*)', 
 barnorm='percent', 
 color='POOL')
normalized_first_pool_deposited_to_fig.update_layout(title="Normalized New Osmosis LPs by First Pool Deposited",
  xaxis_title="WEEK",
  yaxis_title="Number of deposits",
  bargap=0.1,
  bargroupgap=0.0)
first_pool_deposited_to_fig_pie = px.pie(transfers_by_pool,
names='POOL',
values='COUNT(*)'
)
first_pool_deposited_to_fig_pie.update_layout(title="Distribtuon of first deposits to pool by users",
  xaxis_title="Pool",
  yaxis_title="Number of deposits")
first_pool_deposited_to_fig_pie.update_traces(textposition='inside', textinfo='value+percent+label')
first_pool_deposited_to_fig_multi = px.histogram(transfers_by_pool, 
x='POOL', 
y = 'COUNT(*)', 
color = 'POOL',
barmode='group',
log_y = False)
first_pool_deposited_to_fig_multi.update_layout(title="Number of first deposits to pool by users",
  xaxis_title="Pool",
  yaxis_title="Number of deposits")
introduction = """
The dashboard's purpose is to examine a typical Osmosis user's actions.
- We'll take a look at the most popular entry points into Osmosis. As part of this process, we will examine how many people access Osmosis over the Axelar satellite network vs how many people get it through other means.
- The next step is to look at the most often traded item that gets moved into Osmosis. This will help us get a feel for the asset composition of the Osmosis platform as a whole, as well as see which assets are the most popular among users.
- Once a user has landed on Osmosis, they can take one of several different routes. Some users may decide to sell or trade their original asset for something else before taking their funds elsewhere. The OSMO token is the native currency of the Osmosis ecosystem and may be staked by users. Others may decide to make a trade in their initial asset and then offer liquidity to one of the Osmosis pools. The percentage of users who perform these actions is being analyzed in this dashboard.
- Last but not least, we'll examine the most popular assets for liquidity provision, asset swaps, and asset transfers. This will allow us to grasp the most popular trading pairs and liquidity hubs on the Osmosis platform and gauge the liquidity dynamics of the market.
- This dashboard will provide you a high-level view of the activity and behavior on Osmosis by analyzing the usual user's path through the system.
  """
st.header("New Osmosis Users Analysis")
st.caption("A simple analysis about how users come to Osmosis, what is their first actions")
st.header("Introduction")
with st.expander("Expand to see"):
 st.write(introduction)
st.header("Methods")
with st.expander("Expand to see"):
 st.write("""
 In this dashboard, we will use Flipside database with the following tables
 - osmosis.core.fact_transactions
 - osmosis.core.fact_swaps
 - osmosis.core.fact_liquidity_provider_actions
Links to query:
- https://app.flipsidecrypto.com/velocity/queries/7bf635c0-1e91-4844-b183-82e5d587d7d3
- https://app.flipsidecrypto.com/velocity/queries/5975fc1a-02ad-4760-9741-d7373fb98f6d
- https://app.flipsidecrypto.com/velocity/queries/786af7d7-2485-48b7-9db6-57c30f6ccc6a
- https://app.flipsidecrypto.com/velocity/queries/ddf37478-2972-452e-baa7-946ba855ea72
- https://app.flipsidecrypto.com/velocity/queries/db6f1ac4-d4ee-4dfd-bbc6-d06275a8d204
- https://app.flipsidecrypto.com/velocity/queries/33ee1bd9-30d4-4659-a306-4b2ec1a8e4a4
  """)
st.header("New Osmosis Users")
st.write("Let take a look at the number of new Osmosis users over time")
col1, col2 = st.columns([4, 1])
col1.plotly_chart(new_users_fig, theme="streamlit", use_container_width=True)
col2.write("""
  According to the chart, we can see that
  - Since last year, the number of new Osmosis users increased sharply from just less than 1500 to over 600K, a 400X growth
  - Between Jan 2022 and Mar 2022 were the best months for Osmosis when a lot of users came to the chain during these months.
  - From May 2022, the number of new users came to Osmosis decreased over time and but still remain high with several thousands new users per day
  """)
st.header("The most common ways of entering Osmosis")
col3, col4 = st.columns([4, 1])
col3.plotly_chart(chain_transfers_fig, theme="streamlit", use_container_width=True)
col4.write("""
  According to the chart, we can see that
- Starting from Jan 2022, the number of transfers from other chains to OSMOSIS via IBC channel witness a high growth
- Cosmos and EVMOS were two most popular source chain that contributed the the growth of the number of transfers to Osmosis
- Chihuahua also accounted for a great share of transfers to Osmosis
 """)
col5, col6 = st.columns([4, 2])
col5.plotly_chart(chain_normalized_transfers_fig, theme="streamlit", use_container_width=True)
col6.plotly_chart(chain_transfers_pie_fig, theme="streamlit", use_container_width=True)
st.write("""
In detail, we can see that top 3 of transfers to OSMOSIS are: 
- Cosmos with 1242427 transfers, accounted for 22.1% of all transfers to OSMOSIS
- EVMOS with 804150 transfers, accounted for 14.3% of all transfers to OSMOSIS
- JUNO with 641884 transfers, accounted for 11.4% of all transfers to OSMOSIS
 """)
col7, col8 = st.columns([4, 1])
col7.plotly_chart(chain_volume_transfers_fig, theme="streamlit", use_container_width=True)
col8.write("""
  To exclude volume of unnecssary tokens, I only included transfers of token with the volume less than 1 billion.
  According to the chart, we can see that
- Starting from Jan 2022, the volume of transfers from other chains to OSMOSIS via IBC channel witness a high growth
- Chihuahua and Injective were two most popular source chain that contributed the the growth of the volume of transfers to Osmosis
- Cerberus also accounted for a great share in term volume of transfers to Osmosis
 """)
col9, col10 = st.columns([4, 2])
col9.plotly_chart(chain_volume_normalized_transfers_fig, theme="streamlit", use_container_width=True)
col10.plotly_chart(chain_volume_transfers_pie_fig, theme="streamlit", use_container_width=True)
st.write("""
In detail, we can see that top 3 of transfers to OSMOSIS are: 
- Chihuahua accounted for 36.8% of all volume transferred to OSMOSIS
- Injective accounted for 30.3% of all volume transferred to OSMOSIS
- Cerberus accounted for 17.5% of all volume transferred to OSMOSIS
 """)
st.header("First action by first time users on Osmosis")
col11, col12 = st.columns([2, 2])
col11.plotly_chart(action_type_first_fig, theme="streamlit", use_container_width=True)
col12.plotly_chart(action_type_first_fig_pie, theme="streamlit", use_container_width=True)
st.write("""
  According to the chart, we can see that
  - Swap is the most popular actions among first time OSMOSIS users
  - There have been around 345K users that conducted swapping after they went to OSMOSIS, this action accounted for 64.6% of all actions
  - Staking is the second most popular actions among first time OSMOSIS users
  - There have been around 88K users that conducted staking after they went to OSMOSIS, this action accounted for 16.6% of all actions
  - Transfer is the third most popular actions among first time OSMOSIS users
  - There have been around 63K users that conducted transferring after they went to OSMOSIS, this action accounted for 11.9% of all actions
""")
col13, col14 = st.columns([4, 1])
col13.plotly_chart(action_type_fig, theme="streamlit", use_container_width=True)
col14.write("""
According to the chart, we can see that
- March 2022 was the month with the highest number of actions by first time Osmosis users.
- Mar 7, 2022 was the week with the highest number of actions with over 35K actions
- After Mar 7, 2022 The number of actions started to decline until now
""")
col15, col16 = st.columns([4, 1])
col15.plotly_chart(action_type_normalized_fig, theme="streamlit", use_container_width=True)
col16.write("""
According to the chart, we can see that
- The share of swap actions started to grow since July 2021 and reached its highest in Jan 2022
- However, since then, the share of swap actions dropped slightly and fluctuated over the next period
- On the other hand, the share of staking actions witnessed a high growth during Mar 2022 and accounted for 56% of all actions this month.
""")
st.header("The most common asset when transferred to Osmosis")
st.plotly_chart(normalized_first_asset_swapped_to_fig, theme="streamlit", use_container_width=True)
st.plotly_chart(first_asset_swapped_to_fig_pie, theme="streamlit", use_container_width=True)
st.write("""
According to the chart, we can see that
- OSMO accounted for a half of all asset swapped by first time OSMO users
- This is understandable since OSMOS is needed for transaction fee on OSMOSIS
- ATOM, NGM and JUNO each accounted for around 1/3 of all asset swapped  by first time OSMO users
""")
st.plotly_chart(first_asset_swapped_to_fig_multi, theme="streamlit", use_container_width=True)
st.header("The most common pool by first time users Osmosis")
col17, col18 = st.columns([4, 1])
col17.plotly_chart(first_pool_deposited_to_fig, theme="streamlit", use_container_width=True)
col18.plotly_chart(first_pool_deposited_to_fig_pie, theme="streamlit", use_container_width=True)
st.plotly_chart(normalized_first_pool_deposited_to_fig, theme="streamlit", use_container_width=True)
st.write("""
According to the chart, we can see that
- Pool 1 is the most loved pool with 74.2% of participation from new Osmosis users.
- Pool 497 is the second most loved pool with 4.69% of participation from new Osmosis users.
- It's quite clear that Pool 1 has the domination over all other pools
- March 2022 was the month with the most number of LP actions from new Osmosis users with nearly 12K of actions on Mar 14, 2022.
""")
st.header("""Conclusion""")
st.write("""
1. Most of users conducted swapping right after they moved to Osmosis from other chain. Swap actions accounted for 64.6% of all actions
2. After that, users tended to skate their tokens when this actions accounted for 16.6% of all actions
3. Most of users went to OSMOSIS from COSMOS and EVMOS
4. OSMO is the most common asset transferred into Osmosis for first transfer. This is understandable since this token is needed for transaction fee.
5. Pool 1 - OSMO/ATOM is the most popular pool among first time Osmosis users.
 """)
