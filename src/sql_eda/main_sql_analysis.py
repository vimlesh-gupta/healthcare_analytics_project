from query_runner import run_query
from queries import *
from src.sql_eda.visualization import plot_bar_city

df_cities=run_query(q_top_5_cities_with_highest_disease)
plot_bar_city(df_cities)