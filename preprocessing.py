import pandas as pd

def load_data():
    """Lädt die CSV-Dateien und gibt sie als DataFrames zurück."""
    stores = pd.read_csv('stores.csv')
    features = pd.read_csv('features.csv')
    test = pd.read_csv('test.csv')
    train = pd.read_csv('train.csv')
    return stores, features, test, train

def clean_data(stores, features, train, test):
    """Führt die Bereinigung und Transformation der Daten durch."""
    
    # Mapping für Store Typ in Integer umwandeln
    stores['Type'] = stores['Type'].map({'A': 1, 'B': 2, 'C': 3})
    
    # Datumsfelder in datetime umwandeln
    train['Date'] = pd.to_datetime(train['Date'])
    test['Date'] = pd.to_datetime(test['Date'])
    features['Date'] = pd.to_datetime(features['Date'])
    
    # 'IsHoliday' in train und test in Integer umwandeln
    train['IsHoliday'] = train['IsHoliday'].astype(int)
    
    # Fehlende Werte bei MarkDown-Feldern und anderen Spalten durch 0 ersetzen
    markdown_cols = [f'MarkDown{i}' for i in range(1, 6)]
    features[markdown_cols] = features[markdown_cols].fillna(0)
    
    # Fehlende Werte bei numerischen Spalten durch den Mittelwert ersetzen
    for col in ['Temperature', 'Fuel_Price', 'CPI', 'Unemployment']:
        features[col] = pd.to_numeric(features[col], errors='coerce')
        features[col].fillna(features[col].mean(), inplace=True)

    # Fehleingaben bei CPI korrigieren (zu klein/zu groß)
    cpi_min, cpi_max = 100, 300
    valid_cpi_mean = features.loc[(features['CPI'] > cpi_min) & (features['CPI'] < cpi_max), 'CPI'].mean()
    features['CPI'] = features['CPI'].apply(lambda x: valid_cpi_mean if x <= cpi_min or x >= cpi_max else x)

    # Negative Weekly_Sales in Spaltenmittelwert umwandeln

    train['Weekly_Sales'] = train['Weekly_Sales'].apply(lambda x: train['Weekly_Sales'].mean() if x < 0 else x)


    
    

    return stores, features, train, test

def create_date_features(df):
    """Erzeugt neue Zeit-Features wie Woche, Monat und Jahr."""
    df['Week'] = df['Date'].dt.isocalendar().week
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year
    return df

def merge_data(stores, features, train, test):
    """Merged train/test mit stores und features."""
    # Drop 'IsHoliday' aus train und test vor dem Merging
    train = train.drop('IsHoliday', axis=1)
    test = test.drop('IsHoliday', axis=1)
    
    # Train mergen
    merge_train = pd.merge(train, stores, on='Store', how='inner')
    merge_train = pd.merge(merge_train, features, on=['Store', 'Date'], how='inner')
    
    # Test mergen
    merge_test = pd.merge(test, stores, on='Store', how='inner')
    merge_test = pd.merge(merge_test, features, on=['Store', 'Date'], how='inner')
    
    return merge_train, merge_test

def data_preprocessing():
    """Hauptfunktion zur Datenvorbereitung."""
    # Daten laden
    stores, features, test, train = load_data()

    # Daten bereinigen
    stores, features, train, test = clean_data(stores, features, train, test)

    # Zeit-Features erzeugen
    train = create_date_features(train)
    test = create_date_features(test)

    # Daten mergen
    merge_train, merge_test = merge_data(stores, features, train, test)

    return merge_train, merge_test


merge_train, merge_test = data_preprocessing()

#print(merge_train[merge_train['Weekly_Sales'] < 0])


