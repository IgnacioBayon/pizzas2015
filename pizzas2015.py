import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings

warnings.filterwarnings("ignore")


file_names = ['data_dictionary.csv','order_details.csv','orders.csv','pizza_types.csv','pizzas.csv']

def extract(files):
    df_lst = []
    for name in files:
        df_lst.append(pd.read_csv(f'files2015/{name}', encoding='latin_1'))
    return df_lst


def transform(df_lst: list[pd.DataFrame], semana: int):
    # Vamos a coger las pizzas que se han pedido en la ultima semana de cada tipo.
    # Vamos a guardar los datos por semanas mediante Time Series de Pandas
    # Dividimos el dataframe de 'orders' por semanas, pues llevan la fecha y lo 
    # juntamos con el de 'order_details'
    orders = df_lst[2]  # Dataframe del fichero 'orders'
    order_details = df_lst[1] # Dataframe del fichero 'order_details'
    orders['date'] = pd.to_datetime(orders['date'], format="%d/%m/%Y")
    
    pizzas_df = df_lst[4]
    pizzas_dict = {}
    for index in range(len(pizzas_df)):
        pizzas_dict[pizzas_df['pizza_id'][index]] = 0

    # Esta es la semana que hemos escogido. Se puede cambiar la semana aquí
    for week in range(-1,2):
        # Vamos elegir una semana
        for i in range(len(orders)):
            if orders['date'][i].week == semana - 1 + week:
                init = i+1 #orders['order_id'][i]
            if orders['date'][i].week == semana + week:
                end = i+1 #orders['order_id'][i]
        
        for i in range(len(order_details)):
            if order_details['order_id'][i] == init:
                init_order_details = i
            if order_details['order_id'][i] == end:
                end_order_details = i + 1

        week_df = order_details.iloc[init_order_details:end_order_details, :]
        
        ##########################################
        # Ahora vamos a contar las pizzas que se han pedido en esa semana
        # Primero creamos un diccionario cuyas claves sean todos los tipos
        # de pizzas y cuyos respectivos valores sea el número de veces que
        # se ha pedido cada pizza
        
        week_df.reset_index(drop=True)

        # Damos un peso diferente a cada semana: 0.3, 0.4 y 0.3 (anterior,
        # actual y siguiente)
        
        if week in [-1,1]:
            for index in range(1,len(week_df)):
                # Así accedemos a un valor concreto: df.iloc[columna].iloc[fila]
                pizzas_dict[week_df['pizza_id'].iloc[index]] += 0.3*week_df['quantity'].iloc[index]
        else:
            for index in range(1,len(week_df)):
                # Así accedemos a un valor concreto: df.iloc[columna].iloc[fila]
                pizzas_dict[week_df['pizza_id'].iloc[index]] += 0.4*week_df['quantity'].iloc[index]
    
    # Ahora redondeamos todo el dataframe
    for key in pizzas_dict.keys():
        pizzas_dict[key] = round(pizzas_dict[key])
    
    # Una vez tenemos las pizzas necesarias, tenemos que obtener los ingredientes
    comma = re.compile(r',')
    espacio = re.compile(r'\s')
    pizza_types_df = df_lst[3]

    ingredients_dict = {}
    for pizza1_ingredients in pizza_types_df['ingredients']:
        pizza1_ingredients = espacio.sub('',pizza1_ingredients)
        ingredients = comma.split(pizza1_ingredients)
        for ingredient in ingredients:
            if ingredient not in ingredients_dict:
                ingredients_dict[ingredient] = 0
    
    for key in pizzas_dict:
        if key[-1] == 's':
            end_str, count = 2, 0.75
        elif key[-1] == 'm':
            end_str, count = 2, 1
        elif key[-1] == 'l' and key[-2] != 'x':
            end_str, count = 2, 1.5
        elif key[-2:] == 'xl' and key[-3] != 'x': # xl
            end_str, count = 3, 2
        else: # xxl
            end_str, count = 4, 3
        
        pizza = key[:-end_str]
        current_pizza_ingredients = pizza_types_df[pizza_types_df['pizza_type_id'] == pizza]["ingredients"].head(1).item()
        current_pizza_ingredients = espacio.sub('',current_pizza_ingredients)
        ingredients_lst = comma.split(current_pizza_ingredients)
        
        for ingredient in ingredients_lst:
            ingredients_dict[ingredient] += count

    # Multiplicamos el diccionario por 1.2 para tener un margen de ingredientes
    # y redondeamos el resultado (ya que no podemos tener fracciones de ingredientes)
    for key in ingredients_dict.keys():
        ingredients_dict[key] = round(ingredients_dict[key]*1.2)

    return ingredients_dict

def load(ingredients_dict: dict, week: int):
    series_ingredients_week = pd.DataFrame({0: ingredients_dict})
    if not os.path.exists(f'ingredients_week_{week}.csv'):
        series_ingredients_week.to_csv(f'ingredients_week_{week}.csv')
    
    series_ingredients_week.columns = ["quantity"]
    series_ingredients_week["ingredients"] = series_ingredients_week.index
    series_ingredients_week.index = range(series_ingredients_week.shape[0])

    # Visualizar los datos
    plt.figure(figsize=(12,6))
    plt.title(f"Ingredients needed for week {week}")
    ax = sns.barplot(x='ingredients', y='quantity', data=series_ingredients_week,palette='rocket_r') # rocket_r
    plt.xticks(rotation=90)
    plt.show()

if __name__ == "__main__":
    df = extract(file_names)
    semana = 25
    pizzas_dict = transform(df, semana)
    load(pizzas_dict, semana)