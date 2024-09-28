import pandas as pd
import numpy as np

def load_data():
    """Loads the CSV files and returns them as DataFrames."""
    stores = pd.read_csv('stores.csv')
    features = pd.read_csv('features.csv')
    test = pd.read_csv('test.csv')
    train = pd.read_csv('train.csv')
    return stores, features, test, train

def clean_data(stores, features, train, test):
    """Cleans and transforms the data."""
    
    # Convert store type mapping to integer
    stores['Type'] = stores['Type'].map({'A': 1, 'B': 2, 'C': 3})
    
    # Convert date fields to datetime
    train['Date'] = pd.to_datetime(train['Date'])
    test['Date'] = pd.to_datetime(test['Date'])
    features['Date'] = pd.to_datetime(features['Date'])
    
    # Convert 'IsHoliday' in train and test to integer
    train['IsHoliday'] = train['IsHoliday'].astype(int)
    
    # Replace missing values in markdown fields and other columns with 0
    markdown_cols = [f'MarkDown{i}' for i in range(1, 6)]
    features[markdown_cols] = features[markdown_cols].fillna(0)
    
    # Replace missing values in numerical columns with the mean
    for col in ['Temperature', 'Fuel_Price', 'CPI', 'Unemployment']:
        features[col] = pd.to_numeric(features[col], errors='coerce')
        features[col].fillna(features[col].mean(), inplace=True)

    # Correct CPI outliers (too small/too large)
    cpi_min, cpi_max = 100, 300
    valid_cpi_mean = features.loc[(features['CPI'] > cpi_min) & (features['CPI'] < cpi_max), 'CPI'].mean()
    features['CPI'] = features['CPI'].apply(lambda x: valid_cpi_mean if x <= cpi_min or x >= cpi_max else x)

    # Convert negative Weekly_Sales to column mean
    train['Weekly_Sales'] = train['Weekly_Sales'].apply(lambda x: train['Weekly_Sales'].mean() if x < 0 else x)

    return stores, features, train, test

def create_date_features(df):
    """Creates new time features like week, month, and year."""
    df['Week'] = df['Date'].dt.isocalendar().week
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year
    return df

def merge_data(stores, features, train, test):
    """Merges train/test with stores and features."""
    # Drop 'IsHoliday' from train and test before merging
    train = train.drop('IsHoliday', axis=1)
    test = test.drop('IsHoliday', axis=1)
    
    # Merge train
    merge_train = pd.merge(train, stores, on='Store', how='inner')
    merge_train = pd.merge(merge_train, features, on=['Store', 'Date'], how='inner')
    
    # Merge test
    merge_test = pd.merge(test, stores, on='Store', how='inner')
    merge_test = pd.merge(merge_test, features, on=['Store', 'Date'], how='inner')
    
    return merge_train, merge_test

# Add holidays (excluding Easter) to merge_train
def get_holiday_without_Easter(merge_train):
    # Date definitions
    super_bowl_dates = ['2010-02-12', '2011-02-11', '2012-02-10', '2013-02-08']  # Super Bowl Dates
    labor_day_dates = ['2010-09-10', '2011-09-09', '2012-09-07', '2013-09-06']   # Labor Day Dates
    thanksgiving_dates = ['2010-11-26', '2011-11-25', '2012-11-23', '2013-11-29'] # Thanksgiving Dates
    christmas_dates = ['2010-12-31', '2011-12-30', '2012-12-28', '2013-12-27']    # Christmas Dates

    # Initialize columns in features and set to 0
    merge_train['Super_Bowl'] = 0
    merge_train['Labor_Day'] = 0
    merge_train['Thanksgiving'] = 0
    merge_train['Christmas'] = 0

    # Set 1 in the corresponding column if the date matches and IsHoliday also indicates 1.
    merge_train.loc[(merge_train['IsHoliday'] == 1) & (merge_train['Month'] == 2), 'Super_Bowl'] = 1
    merge_train.loc[(merge_train['IsHoliday'] == 1) & (merge_train['Month'] == 9), 'Labor_Day'] = 1
    merge_train.loc[(merge_train['IsHoliday'] == 1) & (merge_train['Month'] == 11), 'Thanksgiving'] = 1
    merge_train.loc[(merge_train['IsHoliday'] == 1) & (merge_train['Month'] == 12), 'Christmas'] = 1
    
    return merge_train

def get_Easter(merge_train):
    # Initialize columns in merge_train to 0
    merge_train['Easter'] = 0

    # Set 1 for Easter in the corresponding week and year
    # Year 2010, Week 13
    merge_train.loc[(merge_train['Week'] == 13) & (merge_train['Year'] == 2010), 'Easter'] = 1

    # Year 2011, Week 16
    merge_train.loc[(merge_train['Week'] == 16) & (merge_train['Year'] == 2011), 'Easter'] = 1

    # Year 2012, Week 14
    merge_train.loc[(merge_train['Week'] == 14) & (merge_train['Year'] == 2012), 'Easter'] = 1

    return merge_train

def data_preprocessing():
    """Main function for data preparation."""
    # Load data
    stores, features, test, train = load_data()

    # Clean data
    stores, features, train, test = clean_data(stores, features, train, test)

    # Create time features
    train = create_date_features(train)
    test = create_date_features(test)

    # Merge data
    merge_train, merge_test = merge_data(stores, features, train, test)

    # Add holidays (excluding Easter)
    merge_train = get_holiday_without_Easter(merge_train)

    # Add Easter
    merge_train = get_Easter(merge_train)

    return merge_train, merge_test


