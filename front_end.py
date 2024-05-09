import streamlit as st



class frontEnd:
    def main(images,gray_images,lbp_images,table):
        if 'image' not in st.session_state:
            st.session_state['image'] = None
    
        with st.sidebar:
            st.session_state['image'] =  st.file_uploader(label="upload image",type=['png','jpg','jpeg'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            for image in images:
                st.image(image)
        with col2:
            st.image(gray_images)
        with col3:
            st.image(lbp_images)




