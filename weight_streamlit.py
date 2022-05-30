import streamlit as st
from PIL import Image
import json


# testing values for now
muscle_values = {'Below Average': 0.38, 'Average': 0.5, 'Fit': 0.57, 'Muscular': 0.74, "Bodybuilder": 0.86}
body_fat_values = {'5 - 10': 0.40, '10 - 15': 0.5, '15 - 20': 0.62, '20 - 25': 0.74, "25 - 30": 0.90, "30 - 35": 1.18,
                   "35 - 40": 1.38, "40 - 45": 1.60, ">45": 1.84}
gender_value = {"male": 1, "female": 0.8}


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
        gender_multiplier = gender_value["male"]
    else:
        gender_multiplier = gender_value["female"] # women have less bone mass and less muscle mass
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
    image = "body_fat_percentage1.jpg"
    if st.button('See fat percentage visualised'):
        original = Image.open(image)
        st.image(original, use_column_width=True)
        st.write("For more info: [link1](https://rippedbody.com/body-fat-guide/) \n"
                 "[link2](https://www.ruled.me/visually-estimate-body-fat-percentage/)")
    return fat_value


# TODO improve the mathematical formula
def bmi_calculator(body_fat, muscle, gender):
    bmi_base = 19
    additional_muscle_factor = 0
    # account for the fact that fatter people are naturally more muscular
    # if body_fat >= 0.5:
    #     additional_muscle_factor = (body_fat - 0.5) * 0.65
    # else:
    #     additional_muscle_factor = 0

    bmi = bmi_base * ((body_fat + muscle) * gender + additional_muscle_factor)
    return bmi


def weight_calculation(body_fat, body_type, gender_multiplier, height):
    # 0.025 to describe the full fat percentage range
    bmi_lower_bound = bmi_calculator(body_fat - 0.025, body_type, gender_multiplier)
    bmi_upper_bound = bmi_calculator(body_fat + 0.025, body_type, gender_multiplier)
    # 5% margin of error
    weight_lower_bound = round(bmi_lower_bound * (int(height) / 100) ** 2 * 0.97, 1)
    weight_upper_bound = round(bmi_upper_bound * (int(height) / 100) ** 2 * 1.03, 1)
    # cap the range at +/- 5kg
    middle_bmi = bmi_calculator(body_fat, body_type, gender_multiplier)
    middle_value = round(middle_bmi * (int(height) / 100) ** 2, 1)
    threshold = 5.5
    if middle_value - bmi_lower_bound > threshold:
        weight_lower_bound = middle_value - threshold
    if weight_upper_bound - middle_value > threshold:
        weight_upper_bound = middle_value + threshold
    return weight_lower_bound, weight_upper_bound


def weight_estimation():
    st.title('Weight Predictor based on muscle build and body fat percentage')

    st.subheader("A simple app that predicts a person's weight based on given parameters")

    gender_multiplier = get_gender()
    height = get_user_height()
    body_type = get_user_body_type()
    body_fat = get_user_fat_percentage()

    weight_lower_bound, weight_upper_bound = weight_calculation(body_fat, body_type, gender_multiplier, height)
    st.header("Weight value")
    final_str = "Your predicted weight in kg is between: " + str(weight_lower_bound) + " to " + str(weight_upper_bound)
    st.write(final_str)
    # st.subheader("Was this accurate? Your feedback is appreciated")
    # actual_weight = st.text_input("What was your actual weight (in kg)?", 'nil')
    st.text("Version1.2")


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
    # unit_test1(male_multiplier, "./weight_male.json")
    # unit_test1(female_multiplier, "./weight_female.json")
    people_profile_location = "./people_profiles.json"
    profiles = json.load(open(people_profile_location))
    tests_passed = True
    for people in profiles:
        body_fat = body_fat_values[profiles[people]["body_fat"]]
        body_type = muscle_values[profiles[people]["muscle_type"]]
        height = profiles[people]["height"]
        gender_multiplier = gender_value[profiles[people]["gender"]]
        weight_lower, weight_upper = weight_calculation(body_fat, body_type, gender_multiplier, height)
        if weight_lower <= profiles[people]["actual"] <= weight_upper:
            message = people + " is WITHIN range."
        else:
            message = people + " is OUT of range."
            tests_passed = False
        range_str = " Actual: " + str(profiles[people]["actual"]) + ", range: " + str(weight_lower) + " - " \
                    + str(weight_upper)
        print(message + range_str)
    if tests_passed:
        print("Good job all test cases passed")


def contact_me():
    st.write("email: marcus_teo@imagemachine.org")
    st.write("business site: https://www.imagemachine.org")


main()
# unit_test_main()
