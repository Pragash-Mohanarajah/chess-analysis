import streamlit as st

# PageConfig
st.set_page_config(page_title='Homepage',page_icon='🏠')
st.sidebar.success('Select a page above ⬆')

# ---- HEADER SECTION ----
with st.container():
    st.title('Chess.com Games Analysis')
    st.write('You want to see the code? ➡ Check out the [Github Repository](https://github.com/Pragash-Mohanarajah/chess-analysis) 💡')

# ---- MAIN SECTION ----

# ---- FOOTER SECTION ----
st.markdown("<br>",unsafe_allow_html=True)