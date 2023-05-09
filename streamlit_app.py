import streamlit as sl
import pandas as pd
import requests
import json
import snowflake.connector
from urllib.error import URLError


sl.title('My Parents New Healthy Diner')
sl.subheader('Breakfast Menu')
sl.text('🥣 Omega 3 & Bluberry Oatmeal')
sl.text('🥗 Kale, Spinach & Rocket Smoothie')
sl.text('🐔 Hard-Boiled Free-Range Egg')
sl.text('🥑🍞 Avocado Toast')

sl.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = sl.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])

fruits_to_show = my_fruit_list.loc[fruits_selected]
sl.dataframe(fruits_to_show)

sl.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = sl.text_input('What fruit would you like information about?')
  if not fruit_choice:
          sl.error('Please select fruit to get information')
  else: 
       fruityvice_response = requests.get('https://://fruityvice.com/api/fruit/'+ fruit_choice)
       fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
       sl.dataframe(fruityvice_normalized)
except URLError as e:
        sl.error()

my_cnx = snowflake.connector.connect(**sl.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM pc_rivery_db.public.fruit_load_list")
my_data_rows = my_cur.fetchall()
sl.header("The fruit load list contains:")
sl.dataframe(my_data_rows)

add_my_fruit = sl.text_input('What fruit would you like to add?')
sl.write('Thanks for adding', add_my_fruit)

my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('from streamlit')")
sl.stop()


        
    
