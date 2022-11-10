import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import style

city_data_to_load = "C:\\Users\\bpiet\\anaconda3\\envs\\PythonData\\Class\\city_data.csv"
ride_data_to_load = "C:\\Users\\bpiet\\anaconda3\\envs\\PythonData\\Class\\ride_data.csv"

city_data_df = pd.read_csv(city_data_to_load)
ride_data_df = pd.read_csv(ride_data_to_load)

pyber_data_df = pd.merge(ride_data_df, city_data_df, how="left", on=["city", "city"])


count_by_city_type = pyber_data_df.groupby('type').size()

count_drivers_by_type = city_data_df.groupby('type')['driver_count'].sum()

count_fares_by_type = pyber_data_df.groupby('type')['fare'].sum()

left = pd.Series(count_by_city_type, name="count")
right = pd.Series(count_drivers_by_type, name="drivers")
rightmost = pd.Series(count_fares_by_type, name="fares")

interim_df = pd.merge(left, right, left_index=True, right_index=True)

data_by_type_df = pd.merge(interim_df, rightmost, left_index=True, right_index=True)

data_by_type_df["mean_fare"] = data_by_type_df['fares']/data_by_type_df['count']

data_by_type_df["mean_fare_per_driver"] = data_by_type_df['fares']/data_by_type_df['drivers']

data_by_type_df.describe()

pyber_summary_df = data_by_type_df.describe()

pyber_summary_df.index.name = None

data_by_type_df["mean_fare"] = data_by_type_df["mean_fare"].round(2)


data_by_type_df["mean_fare_per_driver"] = data_by_type_df["mean_fare_per_driver"].round(2)

for c in data_by_type_df.columns:
    data_by_type_df[c] = data_by_type_df[c].apply(lambda x : '{0:,}'.format(x))

data_by_type_df = data_by_type_df.applymap(str)

data_by_type_df.iloc[1, 4] = '39.50'

data_by_type_df['fares'] = '$' + data_by_type_df['fares']
data_by_type_df['mean_fare'] = '$' + data_by_type_df['mean_fare']
data_by_type_df['mean_fare_per_driver'] = '$' + data_by_type_df['mean_fare_per_driver']

pyber_data_df = pd.merge(ride_data_df, city_data_df, how="left", on=["city", "city"])

pyber_data_df = pyber_data_df.set_index(['type', 'date'])
sum_fares_by_date = pyber_data_df.groupby('date')['fare'].sum()

pyber_data_pivot = pd.pivot_table(pyber_data_df, values="fare", index='date', columns='type')

pyber_data_pivot_sub1 = pyber_data_pivot.loc['2019-01-01':'2019-04-29']

pyber_data_pivot_sub1.index = pd.to_datetime(pyber_data_pivot_sub1.index)

pyber_data_pivot_resample = pyber_data_pivot_sub1.resample('W').sum()


pyber_data_pivot_resample.plot()

style.use('fivethirtyeight')

plt.xlabel('')
plt.ylabel('Fare $(USD)')
plt.title('Total Fare by City Type')
plt.grid()

plt.show()
plt.savefig('PyBer_fare_summary.png')

