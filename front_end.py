import streamlit as st
from data_base import dataBase


class frontEnd:
    def main(images,gray_images,lbp_images,table):
        db = dataBase()

        if 'image' not in st.session_state:
            st.session_state['image'] = None
        if 'custom_image_selection' not in st.session_state:
            st.session_state['custom_image_selection'] = None
        if 'search_image' not in st.session_state:
            st.session_state['search_image'] = None
        with st.sidebar:
            st.session_state['search_image'] = st.file_uploader(label='upload_search_image')
            st.session_state['custom_image_selection'] = st.radio(label='choose the image you want to see:',options=db.get_group_names())
            custum_images_list,vector = db.get_custom_image_group(st.session_state['custom_image_selection'])
        col1, col2, col3,col4 = st.columns(4)

        with col1:
            st.image(custum_images_list[0])
        with col2:
            st.image(custum_images_list[1])
        with col3:
            st.image(custum_images_list[2])
        with col4:
            st.table(vector)




        # with col1:

        #     for image in images:
        #         st.image(image)
        # with col2:
        #     for image in gray_images:
        #         st.image(image)
        # with col3:
        #     for image in lbp_images:
        #         st.image(image)
        # with col4:
        #     st.table(table)



