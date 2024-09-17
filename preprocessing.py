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


# Unrelevante Spalten aus merge_test entfernen
merge_test.drop(['Date', 'Year', 'MarkDown1', 'MarkDown2', 'MarkDown4', 'MarkDown3', 'MarkDown5', 'CPI', 'Unemployment', 'Temperature', 'Fuel_Price'], axis=1)




# Datumswerte aus features['Temperature'] in Spaltenmittelwert umwandeln

# Zunächst Spalte in numerische Werte transformieren -> Datum wird zu NaN
features['Temperature']=pd.to_numeric(features['Temperature'],errors='coerce')

# Mittelwert der validen Temperatur berechnen (ignoriere NaN-Werte)
mean_temp = features['Temperature'].mean()

# Ersetze die NaN-Werte mit dem Mittelwert
features['Temperature'].fillna(mean_temp,inplace=True)




# Datumswerte aus features['Fuel_Price'] in Spaltenmittelwert umwandeln

# Zunächst Spalte in numerische Werte transformieren -> Datum wird zu NaN
features['Fuel_Price']=pd.to_numeric(features['Fuel_Price'],errors='coerce')

# Mittelwert der validen Temperatur berechnen (ignoriere NaN-Werte)
mean_fuel_price = features['Fuel_Price'].mean()

# Ersetze die NaN-Werte mit dem Mittelwert
features['Fuel_Price'].fillna(mean_fuel_price,inplace=True)





# Datumswerte und Nan-Werte aus features['MarkDown1'] in Spaltenmittelwert umwandeln

# Zunächst Spalte in numerische Werte transformieren -> Datum wird zu NaN
features['MarkDown1']=pd.to_numeric(features['MarkDown1'],errors='coerce')

# Mittelwert der validen Temperatur berechnen (ignoriere NaN-Werte)
mean_md1 = features['MarkDown1'].mean()

# Ersetze die NaN-Werte mit dem Mittelwert
features['MarkDown1'].fillna(mean_md1,inplace=True)





# Datumswerte und Nan-Werte aus features['MarkDown2'] in Spaltenmittelwert umwandeln

# Zunächst Spalte in numerische Werte transformieren -> Datum wird zu NaN
features['MarkDown2']=pd.to_numeric(features['MarkDown2'],errors='coerce')

# Mittelwert der validen Temperatur berechnen (ignoriere NaN-Werte)
mean_md2 = features['MarkDown2'].mean()

# Ersetze die NaN-Werte mit dem Mittelwert
features['MarkDown2'].fillna(mean_md2,inplace=True)





# Datumswerte und Nan-Werte aus features['MarkDown3'] in Spaltenmittelwert umwandeln

# Zunächst Spalte in numerische Werte transformieren -> Datum wird zu NaN
features['MarkDown3']=pd.to_numeric(features['MarkDown3'],errors='coerce')

# Mittelwert der validen Temperatur berechnen (ignoriere NaN-Werte)
mean_md3 = features['MarkDown3'].mean()

# Ersetze die NaN-Werte mit dem Mittelwert
features['MarkDown3'].fillna(mean_md3,inplace=True)





# Datumswerte und Nan-Werte aus features['MarkDown4'] in Spaltenmittelwert umwandeln

# Zunächst Spalte in numerische Werte transformieren -> Datum wird zu NaN
features['MarkDown4']=pd.to_numeric(features['MarkDown4'],errors='coerce')

# Mittelwert der validen Temperatur berechnen (ignoriere NaN-Werte)
mean_md4 = features['MarkDown4'].mean()

# Ersetze die NaN-Werte mit dem Mittelwert
features['MarkDown4'].fillna(mean_md4,inplace=True)






# Datumswerte und Nan-Werte aus features['MarkDown5'] in Spaltenmittelwert umwandeln

# Zunächst Spalte in numerische Werte transformieren -> Datum wird zu NaN
features['MarkDown5']=pd.to_numeric(features['MarkDown5'],errors='coerce')

# Mittelwert der validen Temperatur berechnen (ignoriere NaN-Werte)
mean_md5 = features['MarkDown5'].mean()

# Ersetze die NaN-Werte mit dem Mittelwert
features['MarkDown5'].fillna(mean_md5,inplace=True)






# Tippfehler (zu kleine Werte) ersetzen durch Spaltenmittelwert für CPI

schwelle_min = 100
schwelle_max = 300 

# Berechne den Mittelwert der CPI-Werte, die im gültigen Bereich (zwischen schwelle_min und schwelle_max) liegen
valid_cpi_mean = features[(features['CPI'] > schwelle_min) & (features['CPI'] < schwelle_max)]['CPI'].mean()

# Ersetze alle CPI-Werte, die unter schwelle_min liegen, durch den Mittelwert
features.loc[features['CPI'] <= schwelle_min] = valid_cpi_mean

# Ersetze alle CPI-Werte, die über schwelle_max liegen, durch den Mittelwert
features.loc[features['CPI'] >= schwelle_max] = valid_cpi_mean




# Fehlende Werte bei CPI ersetzen durch Spaltenmittelwert

# Mittelwert der validen CPI berechnen (ignoriere NaN-Werte)
mean_cpi = features['CPI'].mean()

# Ersetze die NaN-Werte mit dem Mittelwert
features['CPI'].fillna(mean_cpi, inplace=True)





# Datumswerte und Nan-Werte aus features['Unemployment'] in Spaltenmittelwert umwandeln

# Zunächst Spalte in numerische Werte transformieren -> Datum wird zu NaN
features['Unemployment']=pd.to_numeric(features['Unemployment'],errors='coerce')

# Mittelwert der validen Temperatur berechnen (ignoriere NaN-Werte)
mean_unemployment = features['Unemployment'].mean()

# Ersetze die NaN-Werte mit dem Mittelwert
features['Unemployment'].fillna(mean_unemployment,inplace=True)





'''
# Feiertage in features integrieren

# Datumsdefinitionen
super_bowl_dates = ['2010-02-12', '2011-02-11', '2012-02-10', '2013-02-08']  # Super Bowl Dates
labor_day_dates = ['2010-09-10', '2011-09-09', '2012-09-07', '2013-09-06']   # Labor Day Dates
thanksgiving_dates = ['2010-11-26', '2011-11-25', '2012-11-23', '2013-11-29'] # Thanksgiving Dates
christmas_dates = ['2010-12-31', '2011-12-30', '2012-12-28', '2013-12-27']    # Christmas Dates

# Spalten in Features initial hinzufügen und auf 0 setzen
features['Super_Bowl'] = 0
features['Labor_Day'] = 0
features['Thanksgiving'] = 0
features['Christmas'] = 0

# 1 in entsprechender Spalte setzen, wenn Datum stimmt und in IsHoliday ebenfalls eine 1 steht.
features.loc[(features['IsHoliday'] == 1) & (features['Date'].isin(pd.to_datetime(super_bowl_dates))), 'Super_Bowl'] = 1
features.loc[(features['IsHoliday'] == 1) & (features['Date'].isin(pd.to_datetime(labor_day_dates))), 'Labor_Day'] = 1
features.loc[(features['IsHoliday'] == 1) & (features['Date'].isin(pd.to_datetime(thanksgiving_dates))), 'Thanksgiving'] = 1
features.loc[(features['IsHoliday'] == 1) & (features['Date'].isin(pd.to_datetime(christmas_dates))), 'Christmas'] = 1


'''