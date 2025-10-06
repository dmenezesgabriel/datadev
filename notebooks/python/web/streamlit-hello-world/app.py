# ---
# jupyter:
#   language_info:
#     name: python # <- for syntax highlighting purposes
# ---

# %% [markdown]
# # Streamlit


# %% [markdown]
# Application

# %%
import altair as alt
import pandas as pd
import streamlit as st
from numpy.random import default_rng as rng

df = pd.DataFrame(rng(0).standard_normal((60, 3)), columns=["a", "b", "c"])

chart = (
    alt.Chart(df)
    .mark_circle()
    .encode(x="a", y="b", size="c", color="c", tooltip=["a", "b", "c"])
)

st.altair_chart(chart)

# %% [markdown]
# Run application
# ```sh
#  uvx --with plotly streamlit run app.py
# ```
