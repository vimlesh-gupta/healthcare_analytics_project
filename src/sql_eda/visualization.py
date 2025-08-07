import matplotlib.pyplot as plt
import seaborn as sns
from IPython.core.pylabtools import figsize

output_path=r"D:\Data Analytics Project\helthcare_analytics_project\outputs\visuals\sql"

def plot_bar_city(df):
    plt.figure(figsize(10,6))
    plt.bar(df['city'],df['no_of_patients'],color='b')
    plt.xlabel('City')
    plt.ylabel('Disease Count')
    plt.title('Top 5 cities by Disease Count')
    plt.tight_layout()
    plt.savefig(f'{output_path}/top_5_cities_with_highest_diseases.png', bbox_inches="tight",dpi=300)
    plt.show()

