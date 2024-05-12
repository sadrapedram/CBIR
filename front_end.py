import streamlit as st
from data_base import dataBase
from engine import CBIREngine

class frontEnd:
    def main():
        cbir = CBIREngine()
        db = dataBase()
        
        if 'image' not in st.session_state:
            st.session_state['image'] = None
        if 'custom_image_selection' not in st.session_state:
            st.session_state['custom_image_selection'] = None
        if 'search_image' not in st.session_state:
            st.session_state['search_image'] = None
        col1, col2, col3,col4 = st.columns(4)

        tab = st.sidebar.radio(label='choose tab',options=['available images','all_images','search'])

        if tab == 'available images':
            
            with st.sidebar:
                st.session_state['custom_image_selection'] = st.radio(label='choose the image you want to see:',options=db.get_group_names())
                custum_images_list,vector = db.get_custom_image_group(st.session_state['custom_image_selection'])
            with col1:
                st.image(custum_images_list[0])
            with col2:
                st.image(custum_images_list[1])
            with col3:
                st.image(custum_images_list[2])
            with col4:
                st.table(vector)


        if tab == 'all_images':
            groups= db.get_group_names()
            images = {}
            gray_images = {}
            lbp_images = {}
            vector_dic = {}
            for group_key in groups:
                custum_images_list,vector = db.get_custom_image_group(group=group_key)
                gray_images[group_key] = custum_images_list[1]
                images[group_key] = custum_images_list[0]
                lbp_images[group_key] = custum_images_list[2]
                vector_dic[group_key] = vector
            st.session_state['search_image1'] = st.file_uploader(label='upload_search_image1')


            with col1:
                for image in images.values():
                    st.image(image)
            with col2:
                for image in gray_images.values():
                    st.image(image)
            with col3:
                for image in lbp_images.values():
                    st.image(image)
            with col4:
                for vector in vector_dic.values():
                    st.table(vector)

        if tab == 'search':
            st.session_state['search_image'] = st.sidebar.file_uploader(label='upload_search_image')
            # if st.button('search'):
                # cbir.