import streamlit as st
from PIL import Image
import cv2
import numpy as np
import json


# testing values for now
muscle_values = {'Below Average': 0.38, 'Average': 0.5, 'Fit': 0.62, 'Muscular': 0.74, "Bodybuilder": 0.86}
body_fat_values = {'5 - 10': 0.40, '10 - 15': 0.5, '15 - 20': 0.6, '20 - 25': 0.7, "25 - 30": 0.8, "30 - 35": 0.9,
                   "35 - 40": 1, "40 - 45": 1.1, ">45": 1.2}
male_multiplier = 1
female_multiplier = 0.825


def main():
    selected_box = st.sidebar.selectbox(
        'Choose one of the following',
        ('Weight Estimation', 'Contact Me')
    )

    if selected_box == 'Weight Estimation':
        weight_estimation()
    if selected_box == 'Contact Me':
        contact_me()


def get_user_height():
    # st.header("Step 1, provide your height in cm")
    height = st.text_input("Input your height", '170')
    if int(height) < 300:
        st.write('The height provided is', height)
    else:
        st.write('Is your name Goliath? Please input something sensible')
    return height


def get_gender():
    gender = st.selectbox('What is your gender?', ('Male', 'Female'))
    st.write('You selected:', gender)
    if gender == "Male":
        gender_multiplier = male_multiplier
    else:
        gender_multiplier = female_multiplier  # women have less bone mass and less muscle mass
    return gender_multiplier


def get_user_body_type():
    st.header("Pick the category that describes you the best:")
    st.markdown("**Below average**: Your muscle mass is low due to health conditions or old age")
    st.markdown("**Average**: You don't exercise or do very minimal exercise")
    st.markdown("**Fit**: You exercise but do not engage in any form of weightlifting")
    st.markdown("**Muscular**: You do weightlifting regularly")
    st.markdown("**Bodybuilder**: You do frequent weightlifting with the intention of building mass")
    body_type = st.selectbox('How would you describe your muscular build?',
                             ('Below Average', 'Average', 'Fit', 'Muscular', "Bodybuilder"))
    muscle_proportion = muscle_values[body_type]
    st.write('You selected:', body_type)
    return muscle_proportion


def get_user_fat_percentage():
    st.header("Pick the fat percentage category that describes you the best:")
    body_fat = st.selectbox('Click the fat percentage visualised button if you are unsure',
                            ('5 - 10', '10 - 15', '15 - 20', '20 - 25', "25 - 30", "30 - 35", "35 - 40", "40 - 45",
                             ">45"))
    st.write('You selected:', body_fat)
    fat_value = body_fat_values[body_fat]
    image = "C:/Users/ace-j/AppData/Roaming/JetBrains/PyCharmCE2021.1/scratches/body_fat_percentage1.jpg"
    if st.button('See fat percentage visualised'):
        original = Image.open(image)
        st.image(original, use_column_width=True)
        st.write("For more info: [link1](https://rippedbody.com/body-fat-guide/) \n"
                 "[link2](https://www.ruled.me/visually-estimate-body-fat-percentage/)")
    return fat_value


# TODO improve the mathematical formula
def bmi_calculator(body_fat, muscle, gender):
    bmi_base = 19
    bmi = bmi_base * (body_fat + muscle) * gender
    return bmi


def weight_estimation():
    st.title('Weight Predictor based on muscle build and body fat percentage')

    st.subheader("A simple app that predicts a person's weight based on given parameters")

    gender_multiplier = get_gender()
    height = get_user_height()
    body_type = get_user_body_type()
    body_fat = get_user_fat_percentage()

    bmi = bmi_calculator(body_fat, body_type, gender_multiplier)
    weight = bmi * (int(height) / 100) ** 2
    weight = round(weight, 1)
    st.header("Weight value")
    st.write("Your predicted weight in kg is: ", weight)
    # st.subheader("Was this accurate? Your feedback is appreciated")
    # actual_weight = st.text_input("What was your actual weight (in kg)?", 'nil')


# shows the weight values based on different heights
# do one version for males
def unit_test1(gender_multiplier, json_name):
    weight_values = {}
    for height in range(145, 200):
        if height not in weight_values:
            weight_values[height] = {}
        for fat in body_fat_values:
            if fat not in weight_values[height]:
                weight_values[height][fat] = {}
            for muscle in muscle_values:
                fat_proportion = body_fat_values[fat]
                muscle_proportion = muscle_values[muscle]
                bmi = bmi_calculator(fat_proportion, muscle_proportion, gender_multiplier)
                weight = bmi * (height / 100) ** 2
                weight = round(weight, 1)
                weight_values[height][fat][muscle] = weight
    with open(json_name, "w+") as write_file:
        json.dump(weight_values, write_file, indent=4)


def unit_test_main():
    unit_test1(male_multiplier, "./weight_male.json")
    unit_test1(female_multiplier, "./weight_female.json")


def contact_me():
    st.write("email: marcus_teo@imagemachine.org")
    st.write("business site: https://www.imagemachine.org")


main()
# unit_test_main()