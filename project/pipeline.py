# Methods of Advanced Data Engineering Projekt

import re
import pandas as pd
import requests
from io import BytesIO
from zipfile import ZipFile

# URLs of datasets
urls = {
    "world_bank_mortality_rate_adult": "https://api.worldbank.org/v2/en/indicator/SP.DYN.AMRT.MA?downloadformat=csv",
    "world_bank_mortality_rate_infant": "https://api.worldbank.org/v2/en/indicator/SP.DYN.IMRT.IN?downloadformat=csv",
    "world_bank_life_expectancy_at_birth": "https://api.worldbank.org/v2/en/indicator/SP.DYN.LE00.IN?downloadformat=csv",
    "who_domestic_general_government_health_expenditure": "https://ghoapi.azureedge.net/api/GHED_GGHE-DCHE_SHA2011"
}

# Define the country names for North, Central, and South America
americas_country_names = [
    'Argentina', 'Bahamas', 'Barbados', 'Belize', 'Bolivia', 'Brazil', 'Canada', 'Chile', 'Colombia', 'Costa Rica',
    'Cuba', 'Dominica', 'Dominican Republic', 'Ecuador', 'El Salvador', 'Grenada', 'Guatemala', 'Guyana', 'Haiti',
    'Honduras', 'Jamaica', 'Mexico', 'Nicaragua', 'Panama', 'Paraguay', 'Peru', 'Saint Kitts and Nevis',
    'Saint Lucia', 'Saint Vincent and the Grenadines', 'Suriname', 'Trinidad and Tobago', 'United States',
    'Uruguay', 'Venezuela'
]

# Define the country codes for North, Central, and South America (for OData)
americas_country_codes = [
    'ARG', 'BHS', 'BRB', 'BLZ', 'BOL', 'BRA', 'CAN', 'CHL', 'COL', 'CRI', 'CUB', 'DMA', 'DOM', 'ECU', 'SLV', 'GRD',
    'GTM', 'GUY', 'HTI', 'HND', 'JAM', 'MEX', 'NIC', 'PAN', 'PRY', 'PER', 'KNA', 'LCA', 'VCT', 'SUR', 'TTO', 'USA',
    'URY', 'VEN'
]

# Functions
def get_indicator_name_from_url(url):
    match = re.search(r'/indicator/(.+?)\?downloadformat=csv', url)
    return match.group(1) if match else None

def download_and_load_csv(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        # Extract indicator name from URL
        indicator_name = get_indicator_name_from_url(url)
        if not indicator_name:
            print(f"Could not extract indicator name from URL: {url}")
            return None

        # Check if response is a ZIP file
        if response.headers.get('Content-Type') == 'application/zip':
            with ZipFile(BytesIO(response.content)) as zip_file:
                # List files in ZIP for debugging
                print(f"Files in ZIP for {indicator_name}: {zip_file.namelist()}")

                # Look for main data file in ZIP
                for file_name in zip_file.namelist():
                    if file_name.startswith("API_") and indicator_name in file_name and file_name.endswith('.csv'):
                        with zip_file.open(file_name) as file:
                            # Load relevant CSV, skip first 4 rows (metadata)
                            return pd.read_csv(file, skiprows=4)
            print(f"No data file matching '{indicator_name}' found in the ZIP from {url}")
            return None
        else:
            # Handle direct CSV files with extra header lines
            try:
                return pd.read_csv(BytesIO(response.content), encoding="utf-8", skiprows=4)
            except UnicodeDecodeError:
                print(f"UTF-8 encoding failed for {url}, trying ISO-8859-1 encoding.")
                return pd.read_csv(BytesIO(response.content), encoding="ISO-8859-1", skiprows=4)

    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return None
    except pd.errors.ParserError as e:
        print(f"Error parsing the CSV file from {url}: {e}")
        return None
    except pd.errors.EmptyDataError as e:
        print(f"Empty data error: {e}")
        return None


def download_and_load_odata(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error if download fails
        data = response.json()  # Parse JSON response
        # Extract relevant data
        records = data.get('value', data)
        return pd.DataFrame.from_records(records)
    except requests.exceptions.RequestException as e:
        print(f"Error accessing OData endpoint {url}: {e}")
        return None
    except ValueError as e:
        print(f"Error parsing JSON data from OData endpoint {url}: {e}")
        return None

def filter_americas_data_csv(df):
    if 'Country Name' in df.columns:
        return df[df['Country Name'].isin(americas_country_names)]
    else:
        print("No 'Country Name' column found in DataFrame.")
        return df

def filter_americas_data_odata(df):
    if 'SpatialDim' in df.columns:
        return df[df['SpatialDim'].isin(americas_country_codes)]
    else:
        print("No 'SpatialDim' column found in DataFrame.")
        return df

def verify_filtering(df, data_type):
    if data_type == 'csv' and 'Country Name' in df.columns:
        # Check if remaining country names are in americas_country_names
        unique_countries = set(df['Country Name'].unique())
        if unique_countries.issubset(americas_country_names):
            print("Filtering successful: only American countries remain.")
        else:
            print("Warning: some non-American countries were found.")
    elif data_type == 'odata' and 'SpatialDim' in df.columns:
        # Check if all remaining country codes are in americas_country_codes
        unique_codes = set(df['SpatialDim'].unique())
        if unique_codes.issubset(americas_country_codes):
            print("Filtering successful: only American countries remain.")
        else:
            print("Warning: some non-American country codes were found.")
    else:
        print("Verification failed: Required column not found.")

def print_remaining_countries(df, data_type):
    if data_type == 'csv' and 'Country Name' in df.columns:
        print("Remaining countries (CSV):", df['Country Name'].unique())
    elif data_type == 'odata' and 'SpatialDim' in df.columns:
        print("Remaining country codes (OData):", df['SpatialDim'].unique())
    else:
        print("No valid column found to display remaining countries.")


def drop_columns_before_2000_and_unnamed(df):
    columns_to_drop = [col for col in df.columns if ("Unnamed" in col or (col.isdigit() and int(col) < 2000))]
    df.drop(columns=columns_to_drop, inplace=True, errors='ignore')
    print(f"Dropped columns: {columns_to_drop}")
    return df


def clean_and_structure_data(df, dataset_name):
    # Remove unnecessary columns
    essential_columns = {
        "world_bank_mortality_rate_adult": [
            'Country Name', 'Country Code', 'Indicator Name', 'Indicator Code',
            *[str(year) for year in range(2000, 2023)]
        ],
        "world_bank_mortality_rate_infant": [
            'Country Name', 'Country Code', 'Indicator Name', 'Indicator Code',
            *[str(year) for year in range(2000, 2023)]
        ],
        "world_bank_life_expectancy_at_birth": [
            'Country Name', 'Country Code', 'Indicator Name', 'Indicator Code',
            *[str(year) for year in range(2000, 2023)]
        ],
        "who_domestic_general_government_health_expenditure": [
            'SpatialDim', 'ParentLocation', 'TimeDim', 'NumericValue'
        ]
    }

    if dataset_name in essential_columns:
        df = df[essential_columns[dataset_name]]

    year_columns = [str(year) for year in range(2000, 2023)]
    if dataset_name != "who_domestic_general_government_health_expenditure":
        df.dropna(subset=year_columns, how="all", inplace=True)
    else:
        df.dropna(subset=['NumericValue'], inplace=True)

    if dataset_name == "who_domestic_general_government_health_expenditure":
        df.rename(columns={
            'SpatialDim': 'Country Code',
            'TimeDim': 'Year',
            'NumericValue': 'Health Expenditure (% of Government Spending)'
        }, inplace=True)
    elif "mortality_rate" in dataset_name:
        df.rename(columns={'Indicator Name': 'Mortality Rate'}, inplace=True)
    elif "life_expectancy" in dataset_name:
        df.rename(columns={'Indicator Name': 'Life Expectancy'}, inplace=True)

    return df


# Actions
# Download and load data
dataframes = {}
for name, url in urls.items():
    print(f"Starting download for: {name}")

    if "ghoapi" in url:
        # Handle ghoapi URL and apply OData-specific filter
        dataframes[name] = download_and_load_odata(url)
        if dataframes[name] is not None:
            dataframes[name] = filter_americas_data_odata(dataframes[name])
            verify_filtering(dataframes[name], 'odata')
            print_remaining_countries(dataframes[name], 'odata')
    elif "/indicator/" in url and "downloadformat=csv" in url:
        # Handle World Bank CSV download URL and apply CSV-specific filter
        dataframes[name] = download_and_load_csv(url)
        if dataframes[name] is not None:
            dataframes[name] = filter_americas_data_csv(dataframes[name])
            verify_filtering(dataframes[name], 'csv')
            print_remaining_countries(dataframes[name], 'csv')
    else:
        print(f"Unknown URL format for {name}: {url}")
        dataframes[name] = None  # Skip unknown formats

    if dataframes[name] is None:
        print(f"Error: Data for {name} could not be loaded.")
    else:
        print(f"Download, filtering, and verification of {name} successful.")

# Drop unnecessary columns and clean data
for name, df in dataframes.items():
    if 'world_bank' in name:  # Assuming World Bank datasets need this operation
        dataframes[name] = drop_columns_before_2000_and_unnamed(df)

# Clean and structure data
for name, df in dataframes.items():
    dataframes[name] = clean_and_structure_data(df, name)

# Merge data
country_code_to_name = dict(zip(
    dataframes['world_bank_mortality_rate_adult']['Country Code'],
    dataframes['world_bank_mortality_rate_adult']['Country Name']
))

who_data = dataframes['who_domestic_general_government_health_expenditure'].copy()
who_data['Country Name'] = who_data['Country Code'].map(country_code_to_name)

who_data.dropna(subset=['Country Name'], inplace=True)

years = [str(year) for year in range(2000, 2023)]
merged_data = who_data

for name, df in dataframes.items():
    if name != 'who_domestic_general_government_health_expenditure':
        indicator_name = df.columns[2]

        df = df.rename(columns={indicator_name: 'TempIndicator'})

        long_df = df.melt(
            id_vars=['Country Name', 'Country Code', 'Indicator Code'],
            value_vars=years,
            var_name='Year',
            value_name=indicator_name
        )

        long_df['Year'] = long_df['Year'].astype(int)

        merged_data = pd.merge(
            merged_data,
            long_df,
            on=['Country Name', 'Year'],
            how='left',
            suffixes=('', '_other')
        )

print(merged_data.head())

output_path = "data/consolidated_health_data.csv"

merged_data.to_csv(output_path, index=False)

print(f"Consolidated dataset successfully exported to {output_path}")
print("Data Pipeline completed successfully.")

