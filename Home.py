import streamlit as st


st.markdown(
    """
    <h1 style='text-align: center; color: white; font-family: Arial, sans-serif; font-size: 48px;'>
        Climate Change Data Visualization
    </h1>
    """,
    unsafe_allow_html=True
)

image_url = "https://count.getloli.com/@rain?name=rain&theme=booru-lewd&padding=7&offset=0&align=center&scale=2&pixelated=1&darkmode=0"
st.image(image_url, caption="", use_container_width=True)