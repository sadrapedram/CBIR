from front_end import frontEnd
from engine import CBIREngine



# Call the main function of your Streamlit app

if __name__ == "__main__":
    cbir_class =CBIREngine()
    cbir_class.images
    frontEnd.main(cbir_class.images)