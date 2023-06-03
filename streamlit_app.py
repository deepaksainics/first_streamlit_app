import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

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

def get_fruityvice_data(this_fruit_choice):
	fruityvice_response_advice = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
	# Normalizing the json response for Advice fruit
	fruityvice_normalized_advice = pd.json_normalize(fruityvice_response_advice.json())
	return fruityvice_normalized_advice


try:
	# Fruityvice Advice
	fruit_choice = streamlit.text_input('What fruit would you like information about?')
	if not fruit_choice:
		streamlit.error('Please select a fruit to get information')
	else:
		back_from_function = get_fruityvice_data(fruit_choice)
		# Output the table
		streamlit.dataframe(back_from_function)

except URLError as e:
	streamlit.error()

#printing hello Snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)

# Snowflake related Functions
def get_fruit_load_list():
	with my_cnx.cursor() as my_cur:
		my_cur.execute("select * from fruit_load_list")
		return my_cur.fetchall()
#Quering snowflake tables
#my_cur.execute("select * from fruit_load_list")
#my_data_rows = my_cur.fetchall()
#streamlit.header("The fruit load list contains:")
#streamlit.dataframe(my_data_rows)

#Add a button to load the fruit
if streamlit.button('Get fruit Load List'):
	my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
	my_data_rows = get_fruit_load_list()
	streamlit.dataframe(my_data_rows)

#streamlit.stop()	
# Allow the end user to add a fruit to the list
#add_my_fruit = streamlit.text_input('What fruit would you to add?','jackfruit')
#streamlit.write('The user entered ', add_my_fruit)
#my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('" + add_my_fruit + "')")
#streamlit.text("Thanks for adding" +add_my_fruit)

def insert_row_snowflake(new_fruit):
	with my_cnx.cursor() as my_cur:
		my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('" + new_fruit + "')")
		return new_fruit

add_my_fruit = streamlit.text_input('What fruit would you to add?')
if streamlit.button('Add a fruit to the list'):
	my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
	back_from_function = insert_row_snowflake(add_my_fruit)
	streamlit.text("Thank for adding new fruit: " +back_from_function)
