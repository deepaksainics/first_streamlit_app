import streamlit
import pandas as pd

streamlit.title('My pararent new healthy dinner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 and blueberry Oatmeal')
streamlit.text('🥑 Kale, Spinach and Rocket Smoothie')
streamlit.text('🐔 Hard boiled Free-Range egg')
streamlit.text('🥗🍞 Avocado tost')
 
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

streamlit.dataframe(my_fruit_list)
