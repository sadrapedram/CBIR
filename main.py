from front_end import frontEnd
from engine import CBIREngine



# Call the main function of your Streamlit app

if __name__ == "__main__":
    cbir_class =CBIREngine()
    for img in cbir_class.images:
        print(img)
        gray_image = cbir_class.gray_images(img)
        cbir_class.gray_images_list.append(gray_image)
    lbp_images = cbir_class.getLBPimage(cbir_class.gray_images_list)
    frontEnd.main(cbir_class.images,cbir_class.gray_images_list,lbp_images)