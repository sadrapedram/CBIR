from front_end import frontEnd
from engine import CBIREngine
from data_base import dataBase


# Call the main function of your Streamlit app

if __name__ == "__main__":
    cbir_class =CBIREngine()
    cbir_db = dataBase('test_db.hdf5')
    cbir_db.get_group_names('')
    for key, img in cbir_class.images_dict.items():
        print(img)
        gray_image = cbir_class.gray_images(img)
        cbir_class.gray_images_dict[key] = gray_image

    cbir_class.getLBPimage(cbir_class.gray_images_dict)
    mean = cbir_class.image_color_mean()
    for key, img in cbir_class.images_dict.items():
        cbir_db.add_image(image_name=key,
                          image=img,
                          gray_image=cbir_class.gray_images_dict[key],
                          lbp_image= cbir_class.LBP_imgs[key])
    # print(list(cbir_class.images_dict.values())[0])

    frontEnd.main(cbir_class.images_dict.values(),cbir_class.gray_images_dict.values(),cbir_class.LBP_imgs.values(),mean)