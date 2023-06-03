import streamlit
import pandas as pd
import requests
import snowflake.connector

streamlit.title('My pararent new healthy dinner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 and blueberry Oatmeal')
streamlit.text('🥑 Kale, Spinach and Rocket Smoothie')
streamlit.text('🐔 Hard boiled Free-Range egg')
streamlit.text('🥗🍞 Avocado tost')
 
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

#Set Fruit Column as Index
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

fruits_to_show =my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# streamlit.text(fruityvice_response.json())

# Normalizing the json response
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# Output the table
streamlit.dataframe(fruityvice_normalized)

# New section to display fruityvice api response 
streamlit.header('Fruityvice Fruit Advice')

# Fruityvice Advice
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

fruityvice_response_advice = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# Normalizing the json response for Advice fruit
fruityvice_normalized_advice = pd.json_normalize(fruityvice_response_advice.json())
# Output the table
streamlit.dataframe(fruityvice_normalized_advice)
