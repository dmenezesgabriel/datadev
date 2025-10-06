# ---
# jupyter:
#   language_info:
#     name: python # <- for syntax highlighting purposes
# ---

# %% [markdown]
# # Streamlit

# %% [markdown]
# Dependencies

# %%
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "streamlit",
# ]
# ///

# %% [markdown]
# Application

# %%
import streamlit as st

st.write("Hello, World!")

st.session_state["a"] = "a"

if st.button("rerun"):
    st.write(st.session_state["a"])

# %% [markdown]
# Trick to run with PEP 723 and astral/uv

# %%

if __name__ == "__main__":
    flag_options = {
        "browser.serverAddress": "localhost",
        "server.address": "0.0.0.0",
        "server.headless": True,
        "server.runOnSave": True,
        "server.fileWatcherType": "auto",
    }

    if "__streamlitmagic__" not in locals():
        from streamlit.web import bootstrap

        bootstrap.load_config_options(flag_options=flag_options)
        bootstrap.run(__file__, False, [], flag_options)
