import streamlit as st



class frontEnd:
    def main(images,gray_images,lbp_images,table):
        if 'image' not in st.session_state:
            st.session_state['image'] = None
    
        with st.sidebar:
            st.session_state['image'] =  st.file_uploader(label="upload image",type=['png','jpg','jpeg'])
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            for image in images:
                st.image(image)
        with col2:
            for image in gray_images:
                st.image(image)
        with col3:
            for image in lbp_images:
                st.image(image)
        with col4:
            st.table(table)



