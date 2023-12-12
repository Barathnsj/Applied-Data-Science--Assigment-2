import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import scipy.stats as stats

def executing_data(data, indicator_name):
    # Read the CSV file and filter relevant data
    dt = pd.read_csv(data, skiprows=3)
    countrys = ['India', 'United Kingdom', 'china','Pakistan', 'Brazil', 'Australia']
    data = dt[(dt['Indicator Name'] == indicator_name) & (dt['Country Name'].isin(countrys))]
    
    # Drop unnecessary columns and transpose the DataFrame
    data_dff = data.drop(['Country Code','Indicator Name','Indicator Code','1960','1961','1962','1963','1964','1965','1966','1967','1968',
    '1969','1970','1971','1972','1973','1974','1975','1976','1977','1978','1979','1980','1981','1982','1983','1984','1985','1986',
    '1987','1988','1989','1990','1991','1992','1993','1994','1995','1996','1997','1998','1999','2000','2001','2002','2003','2004',
    '2005','2020','2021','2022','Unnamed: 67'], axis=1).reset_index(drop=True)
    # Transpose the DataFrame
    data_df = data_dff.transpose()
    
    # Set the first row as column headers
    data_df.columns = data_df.iloc[0]
    
    # Remove the first row (redundant headers)
    data_df = data_df.iloc[1:]
    
    # Convert index to numeric and create a new 'Years' column
    data_df.index = pd.to_numeric(data_df.index)
    data_df['Years'] = data_df.index
    
    # Returning the data
    return data_dff, data_df

def dataframe(df):
    # Slice the DataFrame to keep only selected columns
    df = df[['Country Name', '2019']]
    return df

def merge_df(d1, d2, d3, d4):
    # Merge multiple DataFrames on the 'Country Name' column
    mer_1 = pd.merge(d1, d2, on='Country Name', how='outer')
    mer_2 = pd.merge(mer_1, d3, on='Country Name', how='outer')
    mer_3 = pd.merge(mer_2, d4, on='Country Name', how='outer')
    mer_3 = mer_3.reset_index(drop=True)
    return mer_3

def lineplot(dt):
    # Plot a line chart for population growth over the years
    plt.figure()
    dt.plot(x='Years', y=['India', 'United Kingdom', 'Pakistan', 'Brazil', 'Australia'], 
            kind='line', xlabel='Years', ylabel='total(%)', marker='o')
    plt.legend(loc='upper right', fontsize='5', labelspacing=1)
    plt.title('Population growth (annual %)')
    plt.show()

def barplot(dt):
    # Plot a bar chart for CO2 emissions over the years
    plt.figure()
    dt.plot(x='Years', y=['India', 'United Kingdom', 'Pakistan', 'Brazil', 'Australia'], 
            kind='bar', xlabel='Years', ylabel='Kg per hectare')
    plt.legend(loc='upper left', fontsize='5', labelspacing=1)
    plt.title('CO2 emissions (kt)')
    plt.show()

def skewkurt_plot(dt):
    # Plot a histogram and print skewness and kurtosis for agricultural land
    dt_numeric = pd.to_numeric(dt, errors='coerce')
    dt_numeric = dt_numeric.dropna()
    skewness = stats.skew(dt_numeric)
    kurtosis = stats.kurtosis(dt_numeric)
    print(f"Skewness: {skewness}")
    print(f"Kurtosis: {kurtosis}") 
    plt.figure()
    plt.hist(dt, bins='auto', alpha=0.7, color= 'green', edgecolor='black')
    plt.grid(True)
    plt.title("Agricultural land from 2006-2019")
    plt.xlabel("United Kingdom Agri Land Area(sq)m")
    plt.ylabel('Frequency')
    plt.show()

def boxplot(dt, countries):
    # Plot a boxplot for population growth of selected countries
    plt.figure(figsize=(10, 6))  # Set the figure size (optional)
    sns.boxplot(data=dt[countries], palette='Set3')
    plt.title('Agriculture, forestry, and fishing, value added (% of GDP)')
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)  
    plt.xlabel('Countries')
    plt.ylabel('GDP Growth')
   
    # Adjust layout to prevent clipping of labels
    plt.tight_layout() 
   
    # Save the figure (optional)
    plt.savefig('boxplot.png')  
    plt.show()

def heatmap(dt):
    # Plot a heatmap for the correlation matrix of selected indicators
    plt.figure()
    numeric_dt = dt.select_dtypes(include='number')
    correlation_matrix = numeric_dt.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation')
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    plt.show()

# Read and process data for different indicators
po, po_t  = executing_data('data.csv', 'Population growth (annual %)')
co2, co2_t  = executing_data('data.csv', 'CO2 emissions (kt)')
ag, ag_t  = executing_data('data.csv', 'Agricultural land (% of land area)')
aff, aff_t  = executing_data('data.csv', 'Agriculture, forestry, and fishing, value added (% of GDP)')

# Slice and rename columns for better readability
po_cor = dataframe(po).rename(columns={'2019': 'Population growth'})
co2_cor = dataframe(co2).rename(columns={'2019': 'CO2_emission'})
ag_cor = dataframe(ag).rename(columns={'2019': 'Agricultural land'})
aff_cor = dataframe(aff).rename(columns={'2019': 'Agri,Forestry & Fishing'})

# Merge the DataFrames for analysis
hm = merge_df(po_cor, co2_cor , ag_cor, aff_cor)

# Generate and display visualizations
plt.savefig('visual.png') # for saving the images
barplot(co2_t)
lineplot(po_t)
skewkurt_plot(po_t['United Kingdom'])
countries = ['India', 'United Kingdom', 'Pakistan', 'Brazil', 'Australia']
boxplot(po_t, countries)
heatmap(hm)