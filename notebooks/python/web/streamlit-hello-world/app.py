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
import streamlit as st

# %% [markdown]
# Home Page


# %%
def home():
    st.write("Home")


# %% [markdown]
# Dashboard Page


# %%
def dashboard():
    st.write("Dashboard")


# %% [markdown]
# Contact Page


# %%
def contact():
    container = st.container(
        border=False,
        height=500,
        horizontal=True,
        horizontal_alignment="center",
        vertical_alignment="center",
    )
    form = container.form(
        key="contact_form",
        width=400,
        border=False,
    )

    header = form.container()
    header.header("contact")

    body = form.container()
    body.text_input(label="E-mail")
    body.text_area(label="Message")

    footer = form.container(
        horizontal=True,
        horizontal_alignment="right",
    )
    footer.form_submit_button("Submit")


# %% [markdown]
# About Page


# %%
def about():
    st.write("About")


# %% [markdown]
# Pages configuration


# %%
pg = st.navigation(
    [
        st.Page(home, title="Home", icon=":material/house:"),
        st.Page(dashboard, title="Dashboard", icon=":material/bar_chart:"),
        st.Page(contact, title="Contact", icon=":material/phone:"),
        st.Page(about, title="About", icon=":material/person:"),
    ]
)

pg.run()

# %% [markdown]
# Run application
# ```sh
#  uvx --with plotly streamlit run app.py --server.runOnSave=True
# ```
