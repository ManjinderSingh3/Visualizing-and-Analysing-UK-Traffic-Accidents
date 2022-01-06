import pandas as pd

def pre_processing():
    dataset = pd.read_csv('accidents.csv')

    # <----------- Step 1: Checking NaN values in each column ----------->
    # print("Count of NULL Values in each Column:\n",dataset.isna().sum())
    # There were 14 rows in dataset where location_easting_osgr, location_northing_osgr, longitude and latitude columns
    # had Null values. So, I have dropped those 14 rows as they were less than 1% of entire dataset
    dataset.dropna(inplace=True)

    # <----------- Step 2: Checking duplicate values ----------------->
    # print("DUPLICATE RECORDS:\n", dataset.duplicated().sum())
    # There were no duplicate record found in the dataset

    # <----- Step 3: Dropping Columns which are not required in the context of requirements mentioned in problem ------>
    required_columns = ['accident_index', 'longitude', 'latitude', 'accident_year', 'accident_severity',
                        'number_of_vehicles', 'number_of_casualties', 'date', 'day_of_week', 'time',
                        'local_authority_district', 'speed_limit', 'urban_or_rural_area', 'light_conditions',
                        'road_surface_conditions']
    for column in dataset.columns:
        if column not in required_columns:
            dataset.drop(column, axis=1, inplace= True)

    # <--------- Step 4: Fetching Day, month and year from date column ----------->
    dataset['Day'] = pd.DatetimeIndex(dataset['date']).day
    dataset['Month'] = pd.DatetimeIndex(dataset['date']).month
    dataset['Year'] = pd.DatetimeIndex(dataset['date']).year
    return dataset


if __name__ == "__main__":
    pre_processing()