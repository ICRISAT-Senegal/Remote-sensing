import streamlit as st

"""
Created on Thu May  2 00:34:58 2024

@author: Janet.Mutuku
"""
#%%
## Import the libraries
import rasterio
import geopandas as gpd
from shapely.geometry import box
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import plotly.express as px
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import contextily as ctx
from matplotlib.colors import LinearSegmentedColormap
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import streamlit as st
import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose

# Title of the Streamlit App
st.title("Flooding Data (2019-2024)")

# Sidebar for file uploads
st.sidebar.header("Upload Data")

# File upload for Dagana Region (2019-2024)
st.sidebar.subheader("Dagana Region Files")
uploaded_files_dagana = st.sidebar.file_uploader("Upload Dagana region flooding data (2019-2024)", accept_multiple_files=True)

# File upload for agCelerant plots (2019-2024)
st.sidebar.subheader("agCelerant Plots Files")
uploaded_files_ag = st.sidebar.file_uploader("Upload agCelerant flooding data (2019-2024)", accept_multiple_files=True)

# File upload for Credit Data
st.sidebar.subheader("Credit Data Files")
uploaded_credit_files = st.sidebar.file_uploader("Upload Credit Data CSV files", accept_multiple_files=True)

start_planting = datetime.strptime('2023-02-15', '%Y-%m-%d').timetuple().tm_yday
end_planting = datetime.strptime('2023-03-15', '%Y-%m-%d').timetuple().tm_yday
start_harvesting = datetime.strptime('2023-07-05', '%Y-%m-%d').timetuple().tm_yday
end_harvesting = datetime.strptime('2023-09-16', '%Y-%m-%d').timetuple().tm_yday
# Dagana Region Section
st.header("**1. Dagana Region**")

if uploaded_files_dagana:
    dataframes_dagana = []
    for file in uploaded_files_dagana:
        #df_dagana = pd.read_csv(file, index_col=0).drop(columns=['flooding_date'], errors='ignore')
        dataframes_dagana.append(file)
    # Load the CSV files for each year
    df_2019_ = pd.read_csv(dataframes_dagana[0],index_col=0).drop(columns =['flooding_date'],axis=1)
    df_2020_ = pd.read_csv(dataframes_dagana[1],index_col=0).drop(columns =['flooding_date'],axis=1)
    df_2021_ = pd.read_csv(dataframes_dagana[2],index_col=0).drop(columns =['flooding_date'],axis=1)
    df_2022_ = pd.read_csv(dataframes_dagana[3],index_col=0).drop(columns =['flooding_date'],axis=1)
    df_2023_ = pd.read_csv(dataframes_dagana[4],index_col=0).drop(columns =['flooding_date'],axis=1)
    df_2024_ = pd.read_csv(dataframes_dagana[5],index_col=0).drop(columns =['flooding_date'],axis=1)

    # List of dataframes to merge
    dataframes = [df_2019_, df_2020_, df_2021_,df_2022_, df_2023_, df_2024_]
    combined_df_dagana = pd.concat(dataframes, axis=1)
    combined_df_dagana = combined_df_dagana.loc[:, ~combined_df_dagana.columns.duplicated()]
    #combined_df_dagana = pd.concat(dataframes_dagana, axis =1)
    st.write(combined_df_dagana.shape)
    st.subheader("Dagana Combined Data Sample")
    st.dataframe(combined_df_dagana.head())

    def process_rs_data(merged_df):
        rs_df = merged_df.filter(regex=('\d{4}-?\d{2}-?\d{2}$'))
        area_rs = rs_df.sum(axis=0)
        rs_df_combined = pd.DataFrame()
        rs_df_combined['Time'] = list(area_rs.index)
        rs_df_combined['Area(ha)'] = list(area_rs.values)
        rs_df_combined['Year'] = rs_df_combined['Time'].str[:4]
        rs_df_combined['Class'] = 'RS_' + rs_df_combined['Year']
        rs_df_combined['Time'] = pd.to_datetime(rs_df_combined['Time'])
        rs_df_combined['DOY'] = rs_df_combined['Time'].apply(lambda x: x.timetuple().tm_yday)
        return rs_df_combined

    dag_rs_df = process_rs_data(combined_df_dagana)
    st.dataframe(dag_rs_df.head(20))

    # Plotting the Cumulative Area for Dagana
    years = dag_rs_df['Time'].dt.year.unique()
    fig, ax = plt.subplots(figsize=(10, 6))

    for year in years:
        year_df = dag_rs_df[dag_rs_df['Time'].dt.year == year]
        ax.plot(year_df['DOY'], year_df['Area(ha)'], marker='o', linestyle='-', label=f'RS Area {year}')

    start_planting = datetime.strptime('2023-02-15', '%Y-%m-%d').timetuple().tm_yday
    end_planting = datetime.strptime('2023-03-15', '%Y-%m-%d').timetuple().tm_yday
    start_harvesting = datetime.strptime('2023-07-05', '%Y-%m-%d').timetuple().tm_yday
    end_harvesting = datetime.strptime('2023-09-16', '%Y-%m-%d').timetuple().tm_yday

    ax.axvline(start_planting, color='blue', linestyle='--', label='Start Planting (15 Feb)')
    ax.axvline(end_planting, color='green', linestyle='--', label='End Planting (15 Mar)')
    ax.axvline(start_harvesting, color='orange', linestyle='--', label='Start Harvesting (5 Jul)')
    ax.axvline(end_harvesting, color='red', linestyle='--', label='End Harvesting (16 Sep)')

    ax.set_title('2019-2024 Cumulative Flooded Areas using Dagana Plots')
    ax.set_xlabel('Day of Year (DOY)')
    ax.set_ylabel('Area (ha)')
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

# agCelerant Section
st.header("**2. agCelerant Plots**")

if uploaded_files_ag:
    dataframes_ag = []
    for file in uploaded_files_ag:
        df_ag = pd.read_csv(file, index_col=0).drop(columns=['flooding_date'], errors='ignore')
        dataframes_ag.append(df_ag)

    combined_df_ag = pd.concat(dataframes_ag, ignore_index=True)

    st.subheader("agCelerant Combined Data Sample")
    st.dataframe(combined_df_ag.head())

    ag_rs_df = process_rs_data(combined_df_ag)
    st.dataframe(ag_rs_df.head())

    # Plotting the Cumulative Area for agCelerant
    years = ag_rs_df['Time'].dt.year.unique()
    fig, ax = plt.subplots(figsize=(10, 6))

    for year in years:
        year_df = ag_rs_df[ag_rs_df['Time'].dt.year == year]
        ax.plot(year_df['DOY'], year_df['Area(ha)'], marker='o', linestyle='-', label=f'RS Area {year}')

    ax.axvline(start_planting, color='blue', linestyle='--', label='Start Planting (15 Feb)')
    ax.axvline(end_planting, color='green', linestyle='--', label='End Planting (15 Mar)')
    ax.axvline(start_harvesting, color='orange', linestyle='--', label='Start Harvesting (5 Jul)')
    ax.axvline(end_harvesting, color='red', linestyle='--', label='End Harvesting (16 Sep)')

    ax.set_title('2019-2024 Cumulative Flooded Areas using agCelerant Plots')
    ax.set_xlabel('Day of Year (DOY)')
    ax.set_ylabel('Area (ha)')
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

#___________________________________________________________credit information________________________-

# Header for Credit Information
st.header("**3. Credit Information**")
st.markdown("General Information: The dataset contains 4,608 rows and 258 columns. "
            "The `parcel_cod` column has 596 unique values, indicating multiple parcels. "
            "The `operating_account` column contains 163 unique types of operations, "
            "with 'Assurance CNAAS' being the most frequent. "
            "There are missing data in `credit_auth_date` and `credit_exec_date`.")

# Credit data file uploader
uploaded_credit_files = st.file_uploader("Click to upload Credit Data CSV files", accept_multiple_files=True)
import math
if uploaded_credit_files:
    #file = r"G:\My Drive\Remote_sensing\SRV_flooding_detection_models\Dagana\agcelerant_working_files\dry_season_agcelerant\data\dhs\merged_cr_rs_data.csv"
    for file in uploaded_credit_files:
        #file = r"G:\My Drive\Remote_sensing\SRV_flooding_detection_models\Dagana\agcelerant_working_files\dry_season_agcelerant\data\dhs\merged_cr_rs_data.csv"
        combined_df_credit = pd.read_csv(file, index_col=0,na_values=np.nan)



    st.markdown("**Sample of the Credit Data:**")
    st.dataframe(combined_df_credit.head(), height=200)

    # Separate rows with and without credit details
    has_credit_details = combined_df_credit.dropna(subset=['credit_req_date', 'credit_auth_date', 'credit_exec_date'])
    no_credit_details = combined_df_credit[combined_df_credit[['credit_req_date', 'credit_auth_date', 'credit_exec_date']].isna().all(axis=1)]

    # Function to process the remote sensing data for cumulative area
    def process_rs_data(merged_df):
        rs_df = merged_df.filter(regex=('\d{4}-?\d{2}-?\d{2}$'))  # Date columns
        area_rs = rs_df.sum(axis=0)  # Summing values row-wise
        rs_df_combined = pd.DataFrame()
        rs_df_combined['Time'] = list(area_rs.index)
        rs_df_combined['Area(ha)'] = list(area_rs.values)
        rs_df_combined['Year'] = rs_df_combined['Time'].str[:4]
        rs_df_combined['Class'] = 'RS_' + rs_df_combined['Year']
        rs_df_combined['Time'] = pd.to_datetime(rs_df_combined['Time'])
        rs_df_combined['DOY'] = rs_df_combined['Time'].apply(lambda x: x.timetuple().tm_yday)
        return rs_df_combined

    # Process both datasets
    has_credit_df = process_rs_data(has_credit_details)
    no_credit_df = process_rs_data(no_credit_details)

    # Convert credit dates to DOY
    def convert_to_doy(date_string):
        date = pd.to_datetime(date_string)
        return date.dayofyear

    # Extract DOY for all credit request, authorization, and execution dates
    credit_req_doy = has_credit_details['credit_req_date'].apply(convert_to_doy).values
    credit_auth_doy = has_credit_details['credit_auth_date'].dropna().apply(convert_to_doy).values
    credit_exec_doy = has_credit_details['credit_exec_date'].dropna().apply(convert_to_doy).values
      # Visualization: Lagged Correlation and Box Plot in same row but different columns
    fig, (ax_lag, ax_box) = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))

    # Display dataframes in two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**agCelerant data with Credit Details**")
        st.dataframe(has_credit_df.head(), height=200)
    
    with col2:
        st.markdown("**agCelerant data without Credit Details**")
        st.dataframe(no_credit_df.head(), height=200)

    # List of years to plot
    years = has_credit_df['Time'].dt.year.unique()

    # Visualization: Plot cumulative flooded areas by year with two categories
    fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(18, 12))
    axs = axs.flatten()  # Flatten the grid to iterate over each axis easily
 

    # Define event study function
    def event_study(df, credit_date, window):
        before = df[(df['DOY'] >= credit_date - window) & (df['DOY'] < credit_date)]
        after = df[(df['DOY'] <= credit_date + window) & (df['DOY'] > credit_date)]
        return before, after

    ## 5. Boxplot Before and After Credit Events
    
    window = 7  # Days before and after the event
    # Loop through each year and plot the cumulative flooded areas
    for i, year in enumerate(years):
        if i >= len(axs):  # Avoid index out of bounds
            break

        ax = axs[i]

        # Plot "With Credit" data
        year_df_with_credit = has_credit_df[has_credit_df['Time'].dt.year == year]
        ax.plot(year_df_with_credit['DOY'], year_df_with_credit['Area(ha)'], marker='o', linestyle='-', label=f'With Credit {year}', color='blue')

        # Plot "Without Credit" data
        year_df_without_credit = no_credit_df[no_credit_df['Time'].dt.year == year]
        ax.plot(year_df_without_credit['DOY'], year_df_without_credit['Area(ha)'], marker='x', linestyle='--', label=f'Without Credit {year}', color='red')

        # Customize each subplot
        ax.set_title(f'Cumulative Flooded Areas {year}', fontsize=10)
        ax.set_xlabel('Day of Year (DOY)')
        ax.set_ylabel('Cumulative Flooded Area (ha)')
        ax.legend()
        ax.grid(True)

        #  # Prepare a figure for plotting lagged correlations
        # fig_lag, ax_lag = plt.subplots(figsize=(10, 6))

        # # Loop through each year, calculate lagged correlations, and plot them
        # lags = list(range(1, 15))  # Test lags from 1 to 14 days
        # for year in years:
        #     # Filter data for the current year
        #     year_df_with_credit = has_credit_df[has_credit_df['Time'].dt.year == year]

        #     # Calculate lagged correlations
        #     correlations = [lagged_correlation(year_df_with_credit, lag) for lag in lags]

        #     # Plot lagged correlations for the current year
        #     ax_lag.plot(lags, correlations, marker='o', linestyle='-', label=f'{year}')
        # for i, year in enumerate(years):
        #     if i >= len(axs):  # Avoid index out of bounds
        #         break

        #     axs_box = axs[i]
        #     def plot_boxplot_before_after(ax, df, credit_date, label):
        #         before_date = df[df['DOY'] < credit_date]
        #         after_date = df[df['DOY'] >= credit_date]
        #         ax.boxplot([before_date['Area(ha)'], after_date['Area(ha)']], labels=[f'{label} Before', f'{label} After'])
        #         ax.set_title(f'Flooded Area Before and After {label}')
        #     fig_box, axs_box = plt.subplots(1, 3, figsize=(15, 5))

        #     # Credit request DOY
        #     if len(credit_req_doy) > 0:
        #         plot_boxplot_before_after(axs_box[0], year_df_with_credit, credit_req_doy[0], 'Credit Request')
        #     # Credit authorization DOY
        #     if len(credit_auth_doy) > 0:
        #         plot_boxplot_before_after(axs_box[1], year_df_with_credit, credit_auth_doy[0], 'Credit Authorization')
        #     # Credit execution DOY
        #     if len(credit_exec_doy) > 0:
        #         plot_boxplot_before_after(axs_box[2], year_df_with_credit, credit_exec_doy[0], 'Credit Execution')



    st.subheader("Is there any difference in the flooded areas for plots with credit and without credit details?")
   
    # Hide unused subplots if there are fewer than 6 years
    for i in range(len(years), 6):
        fig.delaxes(axs[i])
    # Adjust layout to avoid overlapping subplots
    plt.tight_layout()
    st.pyplot(fig)

    # Display the plot
    st.subheader("Is there any relationship between credit and flooding activities for all years?")
    st.markdown("""
    - There seems to be a clear short-term relationship between credit execution and flooding, especially within the first few days after credit is granted. This is more evident in some years, particularly 2023 and 2024.
    - The box plots reinforce the finding that, for some years (particularly 2023 and 2024), flooded areas tend to increase after credit execution, possibly indicating that these years experienced more significant events (such as floods) in response to financial interventions.
    """)
    #st.pyplot(fig_lag)
    # st.markdown("""
    # #### Boxplots:
    # """)
    # # plt.tight_layout()
    # st.pyplot(fig_box)
    # Define function to plot boxplots with colors and label adjustments
    def plot_boxplot_before_after(ax, df, credit_date, label):
        before_date = df[df['DOY'] < credit_date]
        after_date = df[df['DOY'] >= credit_date]
        # Plot boxplots with colors and rotated labels
        box = ax.boxplot([before_date['Area(ha)'], after_date['Area(ha)']], labels=[f'{label} Before', f'{label} After'], patch_artist=True)

        # Customize the colors of the boxplots
        colors = ['#1f77b4', '#ff7f0e']  # Blue for before, orange for after
        for patch, color in zip(box['boxes'], colors):
            patch.set_facecolor(color)

        ax.set_title(f'Flooded Area Before and After {label}')
        # ax.set_xticklabels([f'{label} Before', f'{label} After'], rotation=45, ha='right')  
        ax.set_xticks([1, 2])  # Ensure 2 ticks for "Before" and "After"
        #ax.set_xticklabels([f'{label} Before', f'{label} After'], rotation=45, ha='right') 
        ax.set_xticklabels([f'Before Credit Execution', f'After Credit Execution'], rotation=45, ha='right') 
        ax.tick_params(axis='x', labelsize=10)  # Set the font size for the labels


    # Boxplot Before and After Credit Events for each year (in 3 columns and 2 rows)
    fig_box, axs_box = plt.subplots(2, 3, figsize=(18, 12))
    axs_box = axs_box.flatten()  # Flatten to easily iterate over each subplot

    for i, year in enumerate(years):
        if i >= len(axs_box):  # Avoid index out of bounds
            break

        year_df_with_credit = has_credit_df[has_credit_df['Time'].dt.year == year]

        # Credit request DOY
        if len(credit_req_doy) > 0:
            plot_boxplot_before_after(axs_box[i], year_df_with_credit, credit_req_doy[0], f'{year} Credit Request')
        # Credit authorization DOY
        if len(credit_auth_doy) > 0:
            plot_boxplot_before_after(axs_box[i], year_df_with_credit, credit_auth_doy[0], f'{year} Credit Authorization')
        # Credit execution DOY
        if len(credit_exec_doy) > 0:
            plot_boxplot_before_after(axs_box[i], year_df_with_credit, credit_exec_doy[0], f'{year} Credit Execution')

    # Adjust layout to avoid overlapping subplots
    st.markdown('Before and After Credit Events for each year')
    plt.tight_layout()
    st.pyplot(fig_box)
    st.markdown("""
    **Box Plots for Flooded Area Before and After Credit Execution**:
    - **Visual Comparison**:
        - In most years (2019, 2020, 2021, 2022), the median flooded area appears relatively stable before and after credit execution, but **2023** and **2024** stand out with larger differences.
        - **2023** shows a much larger flooded area after credit execution, while **2024** also indicates a noticeable increase in flooded area after credit execution.
    - **Outliers**: Some outliers (like in 2023) suggest that there were exceptional cases of increased flooded areas after credit execution.
    - **Conclusion**: While credit execution doesn't seem to drastically change the median flooded area for all years, **2023** and **2024** show significant increases in flooded areas after credit execution, which could point to a stronger relationship between credit and increased flooding activity in these years.
    """)

# Post hoc analysis
st.subheader('Post hoc analysis for only 2023 data')
st.markdown("""
            - The linear regression suggests a positive relationship between days_since_credit and Area(ha), but this relationship is not statistically significant (p-value = 0.225).
            - The model explains 60% of the variability in the Area(ha) data, which is moderate, but the overall significance of the model is weak.
             - P>|t| for days_since_credit is 0.225, which is higher than the significance level of 0.05, meaning this predictor is not statistically significant. 
            In simpler terms, we cannot conclude with high confidence that days_since_credit has a significant effect on the Area(ha).
            
            """)

sub_2023 = has_credit_df[has_credit_df['Year']=='2023']
def linear_regression(df, credit_date):
    df['days_since_credit'] = df['DOY'] - credit_date
    X = sm.add_constant(df['days_since_credit'])  # Adding constant for intercept
    y = df['Area(ha)']
    model = sm.OLS(y, X).fit()
    return model

# Running linear regression for the period after credit execution
regression_model = linear_regression(sub_2023[sub_2023['DOY'] >= credit_exec_doy[0]], credit_exec_doy[0])

# Displaying regression results
st.write(regression_model.summary())


# # ________________________Decomposition models
# def time_series_decomposition(df):
#     df.set_index('Time', inplace=True)
#     decomposition = seasonal_decompose(df['Area(ha)'], model='additive', period=5)
#     return decomposition

# # Decompose the time series
# decomposition = time_series_decomposition(sub_2023)
# #st.dataframe(has_credit_df)
# # Plot the decomposition
# fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 8))
# decomposition.observed.plot(ax=ax1, title='Observed')
# decomposition.trend.plot(ax=ax2, title='Trend')
# decomposition.seasonal.plot(ax=ax3, title='Seasonal')
# decomposition.resid.plot(ax=ax4, title='Residual')

# plt.tight_layout()
# st.pyplot(fig)

# _________________Anova analysis

# Function to divide data into 'before' and 'after' credit execution
def divide_before_after(df, credit_date):
    before_credit = df[df['DOY'] < credit_date]['Area(ha)']
    after_credit = df[df['DOY'] >= credit_date]['Area(ha)']
    return before_credit, after_credit

# Assuming you have 'has_credit_df' dataframe and 'credit_exec_doy' contains the execution dates for each year
years = has_credit_df['Time'].dt.year.unique()

# Initialize an empty list to store ANOVA results
anova_results = []

# Loop through each year and perform ANOVA
for year in years:
    #st.write(f"### Year: {year}")

    # Filter data for the current year
    year_df_with_credit = has_credit_df[has_credit_df['Time'].dt.year == year]

    # Get the credit execution date for the current year
    credit_exec_date = credit_exec_doy[0]  # Replace with actual execution date per year if available

    # Divide the flooded area data into before and after credit execution
    before_credit, after_credit = divide_before_after(year_df_with_credit, credit_exec_date)

    # Perform one-way ANOVA
    anova_result = stats.f_oneway(before_credit, after_credit)

    # Store results in the list as a dictionary
    anova_results.append({
        'Year': year,
        'F-statistic': round(anova_result.statistic, 3),
        'p-value': round(anova_result.pvalue, 4),
        'Significant': 'Yes' if anova_result.pvalue < 0.05 else 'no statistically significant difference between the flooded areas before and after credit execution for {year}'
    })

    # Write ANOVA result
    # st.write(f"ANOVA Result for {year}: F-statistic = {anova_result.statistic}, p-value = {anova_result.pvalue}")
    # if anova_result.pvalue < 0.05:
    #     st.write(f"There is a statistically significant difference between the flooded areas before and after credit execution for {year}.")
    # else:
    #     st.write(f"There is no statistically significant difference between the flooded areas before and after credit execution for {year}.")

# Convert the results into a DataFrame
anova_df = pd.DataFrame(anova_results)

# Display the results in a table format
st.write("### ANOVA Results Table")
st.dataframe(anova_df)

# Adjust layout to avoid overlap
plt.tight_layout()

# Display the full grid of plots
st.pyplot(fig)

#_____________________________________GIE analysis________________________________________-_______________________________
st.header("GIE Analysis")
# Load the merged data
data = combined_df_credit.copy()
# Convert None to empty strings
data = data.fillna('')

# Filter out rows with empty strings in the specified columns
has_credit_details = data[
    (data['credit_req_date'] != '') &
    (data['credit_auth_date'] != '') &
    (data['credit_exec_date'] != '')
]
#data = data.replace({None: np.nan})
# Move filters to the sidebar
st.sidebar.header("GIE Based Analysis-Has")
# Filter GIEs with all credit details (credit_req_date, credit_auth_date, credit_exec_date)
#has_credit_details = data.dropna(subset=['credit_req_date', 'credit_auth_date', 'credit_exec_date'],how='all')
gies_with_credit_details = has_credit_details['gie_name'].unique()
#%%
# Select GIE for analysis in the sidebar
selected_gie = st.sidebar.selectbox('Select GIE:', has_credit_details['gie_name'].unique())
# Combine all uploaded files into one DataFrame
#combined_df_credit = pd.concat([pd.read_csv(file, index_col=0) for file in uploaded_credit_files], ignore_index=True)

# Display number of all unique GIEs
all_gies = data['gie_name'].unique()
st.write(f"- Total number of GIEs available for analysis: {len(all_gies)}")

# Filter GIEs with all credit details (credit_req_date, credit_auth_date, credit_exec_date)
#has_credit_details = data.dropna(subset=['credit_req_date', 'credit_auth_date', 'credit_exec_date'])
gies_with_credit_details = has_credit_details['gie_name'].unique()

# Display number of GIEs with complete credit details
st.write(f"- Number of GIEs with complete credit details: {len(gies_with_credit_details)}")
st.write('-Time to execution: the number of days from credit request to execution')

st.markdown(f"**Details for GIE: {selected_gie}**")
filtered_data = has_credit_details[has_credit_details['gie_name'] == selected_gie]

# Convert the 'credit_req_date', 'credit_auth_date', and 'credit_exec_date' columns to datetime for analysis
filtered_data['credit_req_date'] = pd.to_datetime(data['credit_req_date'], errors='coerce')
filtered_data['credit_auth_date'] = pd.to_datetime(data['credit_auth_date'], errors='coerce')
filtered_data['credit_exec_date'] = pd.to_datetime(data['credit_exec_date'], errors='coerce')

# Calculate the time between request and execution
filtered_data['time_to_execution'] = (filtered_data['credit_exec_date'] - filtered_data['credit_req_date']).dt.days

# Display basic statistics for the time to execution
time_to_execution_stats = filtered_data['time_to_execution'].describe()

# Plotting a histogram of time to execution
fig2 = plt.figure(figsize=(10, 6))
plt.hist(filtered_data['time_to_execution'].dropna(), bins=20, color='skyblue', edgecolor='black')
plt.title(f'Distribution of Time to Execution for Credit Requests for GIE: {selected_gie}')
plt.xlabel('Days from Credit Request to Execution')
plt.ylabel('Frequency')
plt.grid(True)

# Show the plot
plt.show()
st.pyplot(fig2)

# Process RS data (you can define this function)
gie_rs_df = process_rs_data(filtered_data)

# Plotting the Cumulative Area for the selected GIE
years = gie_rs_df['Time'].dt.year.unique()
fig, ax = plt.subplots(figsize=(10, 6))

for year in years:
    year_df = gie_rs_df[gie_rs_df['Time'].dt.year == year]
    ax.plot(year_df['DOY'], year_df['Area(ha)'], marker='o', linestyle='-', label=f'RS Area {year}')

start_planting = datetime.strptime('2023-02-15', '%Y-%m-%d').timetuple().tm_yday
end_planting = datetime.strptime('2023-03-15', '%Y-%m-%d').timetuple().tm_yday
start_harvesting = datetime.strptime('2023-07-05', '%Y-%m-%d').timetuple().tm_yday
end_harvesting = datetime.strptime('2023-09-16', '%Y-%m-%d').timetuple().tm_yday

ax.axvline(start_planting, color='blue', linestyle='--', label='Start Planting (15 Feb)')
ax.axvline(end_planting, color='green', linestyle='--', label='End Planting (15 Mar)')
ax.axvline(start_harvesting, color='orange', linestyle='--', label='Start Harvesting (5 Jul)')
ax.axvline(end_harvesting, color='red', linestyle='--', label='End Harvesting (16 Sep)')

ax.set_title(f'2019-2024 Cumulative Flooded Areas for GIE: {selected_gie}')
ax.set_xlabel('Day of Year (DOY)')
ax.set_ylabel('Area (ha)')
ax.grid(True)
ax.legend()
st.pyplot(fig)

# Bar chart for Irrigation Type
st.subheader(f"Count of Irrigation Types for: {selected_gie}")
irrigation_type_counts = filtered_data['irrigation_type'].value_counts()
fig_irrigation, ax_irrigation = plt.subplots(figsize=(8, 4))
ax_irrigation.bar(irrigation_type_counts.index, irrigation_type_counts.values, color='skyblue')
ax_irrigation.set_title('Irrigation Type Count')
ax_irrigation.set_xlabel('Irrigation Type')
ax_irrigation.set_ylabel('Count')
ax_irrigation.grid(True)
st.pyplot(fig_irrigation)


# Prepare the data for timeline visualization
timeline_data = []
for idx, row in filtered_data.iterrows():
    timeline_data.append(dict(Task=row['operating_account'], Start=row['credit_req_date'], Finish=row['credit_auth_date'], Stage='Credit Requested'))
    timeline_data.append(dict(Task=row['operating_account'], Start=row['credit_auth_date'], Finish=row['credit_exec_date'], Stage='Credit Authorized'))
    timeline_data.append(dict(Task=row['operating_account'], Start=row['credit_exec_date'], Finish=row['credit_exec_date'], Stage='Credit Executed'))

# Convert the timeline data into a DataFrame
timeline_df = pd.DataFrame(timeline_data)

# Custom color map for stages
custom_colors = {
    'Credit Requested': 'dodgerblue',
    'Credit Authorized': 'orange',
    'Credit Executed': 'green'
}

# Create a Gantt-style timeline using Plotly with customizations
fig_timeline = px.timeline(
    timeline_df,
    x_start="Start",
    x_end="Finish",
    y="Task",
    color="Stage",
    color_discrete_map=custom_colors,  # Use custom colors for each stage
    title=f"Credit Request, Authorization, and Execution Timeline for GIE: {selected_gie}",
    hover_data={
        'Start': '|%B %d, %Y',  # Customize hover date format
        'Finish': '|%B %d, %Y',  # Customize hover date format
        'Stage': True,
        'Task': True
    },
    labels={"Task": "Operation Account", "Stage": "Credit Stage"}
)

# Customizing the layout
fig_timeline.update_layout(
    xaxis_title="Date",
    yaxis_title="Operation Account",
    showlegend=True,
    height=600,
    margin=dict(l=100, r=50, t=50, b=50),  # Adjust margins for readability
    font=dict(family="Arial, sans-serif", size=12)  # Customize font
)

# Improve x-axis readability
fig_timeline.update_xaxes(
    tickformat="%b %d, %Y",  # Date format on the x-axis
    tickangle=45,  # Rotate x-axis labels
    nticks=20  # Control number of ticks
)


# Display the timeline
st.plotly_chart(fig_timeline)


# Assuming 'melted_data' is your DataFrame and it has a 'geometry' column
# Load GeoDataFrame (GIE credit and RS data with geometries)
st.dataframe(filtered_data)


# Prediction
import streamlit as st
import pandas as pd
import numpy as np
from growth_curve_tools_modified import CurveLibrary
from updated_compare_model_with_logistic_final import compare_model

# Title and description
st.title("Growth Curve Prediction: Logistic vs Gompertz")
st.write("This app predicts growth curves using Logistic and Gompertz models for flooding data.")

# File upload
data_file = st.file_uploader("Upload your flooding data CSV", type=["csv"])

if data_file is not None:
    # Load data
    data_log = pd.read_csv(data_file)
    #data_log['Class'] = 'Log_pred_2024'
    data_log['Time'] = pd.to_datetime(data_log['Time'])
    data_log['DOY'] = data_log['Time'].apply(lambda x: x.timetuple().tm_yday)

    st.write("### Data Preview")
    st.dataframe(data_log)
    
    # Allow user to select model
    model_choice = st.selectbox("Choose the model for prediction", ["Logistic", "Gompertz"])

    # Input fields for the year and interval
    year = st.number_input("Enter the year for prediction", min_value=2000, max_value=2100, value=2023)
    interval = st.number_input("Enter the interval (in days) for predictions", min_value=1, max_value=365, value=5)

    # Button to run the prediction
    if st.button("Run Prediction"):
        st.write(f"Running {model_choice} prediction for the year {year}...")
        fig, ax = plt.subplots(figsize=(10, 6))
        #ax = axs[i]
    
        combined_df_g = pd.concat([dag_rs_df,data_log],axis = 0)
        st.dataframe(combined_df_g)
       # Plot each class in the 'Class' column
        for cls in combined_df_g['Class'].unique():
            class_data = combined_df_g[combined_df_g['Class'] == cls]
            ax.plot(class_data['DOY'], class_data['Area(ha)'], marker='x', linestyle='--', label=cls)

        # Customize plot
        ax.set_title(f'Cumulative Flooded Areas {year}', fontsize=10)
        ax.set_xlabel('Day of Year (DOY)')
        ax.set_ylabel('Cumulative Flooded Area (ha)')
        ax.legend(title='Classes')
        ax.grid(True)

        # Optionally run the compare_model function (uncomment when needed)
        # compare_model(out_path, data, data_ha, data_hist, year, interval=interval, method=model_choice.lower())

        st.write(f"{model_choice} model prediction completed.")
        st.write("Check the output directory for results.")
        st.pyplot(fig)
