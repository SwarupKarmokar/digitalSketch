import streamlit as st
import cv2
import numpy as np 
import base64
import time
from io import BytesIO
from PIL import Image



def get_image_download_link(img):
	buffered = BytesIO()
	img.save(buffered, format="JPEG")
	img_str = base64.b64encode(buffered.getvalue()).decode()
	href = f'<a href="data:file/jpg;base64,{img_str}">Download digital sketch</a>'
	return href




st.set_option('deprecation.showfileUploaderEncoding',False)
st.title("Digital Photo Sketch")
st.text("upload image")

uploaded_img = st.file_uploader("choose image", type=["jpg", "png", "jpeg"])

if uploaded_img is not None:
    img = Image.open(uploaded_img)
    st.image(img, width=200, caption="uploaded image")

    if st.button("convert"):
        st.write("Result")
        img = np.array(img)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_inv = cv2.bitwise_not(gray_img)
        img_blurr = cv2.GaussianBlur(img_inv, (21,21), sigmaX=0, sigmaY=0)
        inv_blurr = cv2.bitwise_not(img_blurr)
        sketch = cv2.divide(gray_img, inv_blurr, scale=256.0)
        st.write("Your digital Sketch")
        st.image(sketch, width=200)


        result = Image.fromarray(sketch)
        st.markdown(get_image_download_link(result), unsafe_allow_html=True)