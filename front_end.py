import streamlit as st



class frontEnd:
    def main(images):
        if 'image' not in st.session_state:
            st.session_state['image'] = None
    
        with st.sidebar:
            st.session_state['image'] =  st.file_uploader(label="upload image",type=['png','jpg','jpeg'])
        
        col1, col2 = st.columns(2)
        with col1:
            for image in images:
                st.image(image)
        with col2:
            st.image(images[0])






