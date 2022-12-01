# PIZZAS 2015

### INTRODUCTION

This code is an ETL which predicts the ingredients that a certain pizzeria
has to buy in a specific week based on various DataFrames from the orders
made in the year 2015

Disclaimer: some variables and comments are in spanish as it is my native tongue

### 1. Libraries used
- 'pandas': used for managing the DataFrame
- 're': used for splitting strings and detecting re patterns
- 'matplotlib.pyplot': drawing plots
- 'seaborn': drawing plots
- 'os': used for detecting whether the csv already exists
- 'warnings': to ignore certain warnings concerning data types

### 2. ETL
#### 1) Extract
We simply read the csvs with the names on the list 'file_names' with the 'read_csv' function from pandas

#### 2) Transform
It gets the prediction of the ingredients for the week 'semana'. My prediction is calculated using the previous and following week, aswell as the one asked. 

We calculate the pizzas ordered for each week with both 'orders' and 'order_details' dataframes and save it in a dictionary 'pizzas_dict'. If the week we are calculating is the previous or following, we multiply it by 0.3, whereas the current one is multiplied by 0.4. That way, we give more importance to the actual week but also even it out with the other ones. 

Once we have the dictionary, we use the dataframe 'pizza_types_df', which contains the pizzas and their ingredients. Depending on the size of the pizza, we multiply it by 0.75 (m), 1 (m), 1.5 (l), 2 (xl), and 3 (xxl). Finally, we gather the data from the ingredients prediction in a dictionary 'ingredients_dict'

#### 3) Load
In this function we first load the prediction in a csv 'ingredients_week_x.csv' and plot it in a barplot
