# Bibliotheken importieren

import pandas as pd



# Einlesen CSV-Dateien 

stores_raw = pd.read_csv('stores.csv')
features_raw = pd.read_csv('features.csv')
test_raw = pd.read_csv('test.csv')
train_raw = pd.read_csv('train.csv')




# Data Frames erzeuen

stores = pd.DataFrame(stores_raw)
features = pd.DataFrame(features_raw)
train = pd.DataFrame(train_raw)
test = pd.DataFrame(test_raw)



# Data Cleaning

# In stores['Type'] zum Integer casten

def transform_Type(row):

    if row == 'A':
        return 1
    elif row == 'B':
        return 2
    elif row == 'C':
        return 3
    else:
        pass

stores.Type = stores.Type.apply(transform_Type)

# Type A ist jetzt Type 1
# Type B ist jetzt Type 2
# Type C ist jetzt Type 3

# Train['Date], Test['Date'] in Datumsformat casten

train['Date'] = pd.to_datetime(train['Date'])
test['Date'] = pd.to_datetime(test['Date'])

# Train/Test['IsHoliday'] zum Integer casten

train['IsHoliday'] = train['IsHoliday'].apply(lambda x: 1 if x == True else 0)

# Features['Date'] in Datumsformat casten

features['Date'] = pd.to_datetime(features['Date'])

# Features.MarkDown 1-5: NaN-Werte provisorisch durch 0 ersetzen

features['MarkDown1'].fillna(0, inplace=True)
features['MarkDown2'].fillna(0, inplace=True)
features['MarkDown3'].fillna(0, inplace=True)
features['MarkDown4'].fillna(0, inplace=True)
features['MarkDown5'].fillna(0, inplace=True)

# Features['IsHoliday'] zum Integer casten

features['IsHoliday'] = features['IsHoliday'].apply(lambda x: 1 if x == True else 0)




# Data Frames mergen


# Da die Spalte 'IsHoliday' doppelt vorkommt, wird sie aus dem train Data Frame vor dem mergen gelöscht

# Train mergen mit stores und features
merge_train_stores = pd.merge(train.drop('IsHoliday',axis=1),stores,how='inner',on='Store', left_on=None, right_on=None, left_index=False, right_index=False, sort=False,suffixes=('_x','_y'),copy=True,indicator=False)
merge_train = pd.merge(merge_train_stores,features, how='inner', on=['Store','Date'],left_on=None, right_on=None, left_index=False, right_index=False, sort=False,suffixes=('_x','_y'),copy=True,indicator=False)

# Test mergen mit stores und features
merge_test_stores = pd.merge(test.drop('IsHoliday',axis=1),stores,how='inner',on='Store', left_on=None, right_on=None, left_index=False, right_index=False, sort=False,suffixes=('_x','_y'),copy=True,indicator=False)
merge_test = pd.merge(merge_test_stores,features, how='inner', on=['Store', 'Date'],left_on=None, right_on=None, left_index=False, right_index=False, sort=False,suffixes=('_x','_y'),copy=True,indicator=False)


# 3 neue Features aus der Date-Spalte erzeugen

merge_train['Week'] = merge_train['Date'].dt.isocalendar().week
merge_train['Month'] = merge_train['Date'].dt.month
merge_train['Year'] = merge_train['Date'].dt.year

merge_test['Week'] = merge_test['Date'].dt.isocalendar().week
merge_test['Month'] = merge_test['Date'].dt.month
merge_test['Year'] = merge_test['Date'].dt.year

print(merge_train)