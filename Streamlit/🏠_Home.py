import streamlit as st
from streamlit_extras.badges import badge

# PageConfig
st.set_page_config(page_title='Homepage',page_icon='🏠')
st.sidebar.success('Select a page above ⬆')

# ---- HEADER SECTION ----
with st.container():
    st.title('Chess.com Games Analysis')
    st.write('You want to see the code? ➡ Check out the [Github Repository](https://github.com/Pragash-Mohanarajah/chess-analysis) 💡')

# ---- MAIN SECTION ----

with st.container():
    st.write('---')
    st.header('Target Goal')
    st.write('A web-app which offers a quick overview of my chess game analysis. The Analysis can be found under 📊:blue[Analysis] in the sidebar.')
    
# ---- Credits ----
with st.container():
    st.write('---')
    st.header('Contributers')
    
with st.container():
    st.write('---')
    st.header('Social Media')
    badge(type="github", name="Pragash-Mohanarajah")
    st.markdown("[LinkedIn](https://www.linkedin.com/in/pragash-mohanarajah/)")

# ---- FOOTER SECTION ----
st.markdown("<br>",unsafe_allow_html=True)