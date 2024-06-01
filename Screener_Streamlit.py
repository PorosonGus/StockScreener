import streamlit as st
import pandas as pd
import sqlite3

# Set page configuration
st.set_page_config(layout="wide")

def load_data():
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(r'StockScreener_Entry_01.06.2024.db')
        query = 'SELECT * FROM measures'  # Replace with your measures table name
        df_measures = pd.read_sql(query, conn)
        conn.close()
        return df_measures
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of an error

# Load data
df = load_data()

# Set "symbol" column as the index and rename index column
df.set_index('symbol', inplace=True)
df.rename_axis('Symbol', inplace=True)

# Sidebar
st.sidebar.header("STOCK SCREENER")

# Add a dropdown menu for calendarYear (sorted in descending order)
year_values = sorted(df['calendarYear'].unique(), reverse=True)
selected_year = st.sidebar.selectbox("Select a Calendar Year", year_values)

# Multiselect for sector with "Select All" option
all_sectors_option = "Select All Sectors"
selected_sectors = st.sidebar.multiselect("Select Sectors", [all_sectors_option] + list(df['sector'].unique()), default=[all_sectors_option])
if all_sectors_option in selected_sectors:
    selected_sectors = df['sector'].unique()

# Multiselect for exchangeShortName with "Select All" option
all_exchanges_option = "Select All Exchanges"
selected_exchanges = st.sidebar.multiselect("Select Exchanges", [all_exchanges_option] + list(df['exchangeShortName'].unique()), default=[all_exchanges_option])
if all_exchanges_option in selected_exchanges:
    selected_exchanges = df['exchangeShortName'].unique()

# Multiselect for reportedCurrency with "Select All" option
all_currencies_option = "Select All Currencies"
selected_currencies = st.sidebar.multiselect("Select Currencies", [all_currencies_option] + list(df['reportedCurrency'].unique()), default=[all_currencies_option])
if all_currencies_option in selected_currencies:
    selected_currencies = df['reportedCurrency'].unique()

# Checkbox for each filter
show_revenue_growth_filter = st.sidebar.checkbox("Revenue Growth (YoY)")
min_revenue_yoy_growth = st.sidebar.slider("Minimum",
                                           min_value=0,
                                           max_value=100,  # Adjust the max_value to 100 for percentages
                                           value=None,
                                           step=1,  # Add the appropriate step size
                                           format="%d%%", key="revenue_yoy") if show_revenue_growth_filter else None  # Display as percentage

show_revenue_cagr_5y_filter = st.sidebar.checkbox("Revenue Growth (5y)")
min_revenue_cagr_5y_growth = st.sidebar.slider("Minimum",
                                              min_value=0,
                                              max_value=100,
                                              value=None,
                                              step=1,
                                              format="%d%%", key="revenue_cagr_5y") if show_revenue_cagr_5y_filter else None

show_ebitda_yoy_growth_filter = st.sidebar.checkbox("EBITDA Growth (YoY)")
min_ebitda_yoy_growth = st.sidebar.slider("Minimum",
                                          min_value=0,
                                          max_value=100,
                                          value=None,
                                          step=1,
                                          format="%d%%", key="ebitda_yoy") if show_ebitda_yoy_growth_filter else None

show_ebitda_cagr_5y_filter = st.sidebar.checkbox("EBITDA Growth (5y)")
min_ebitda_cagr_5y_growth = st.sidebar.slider("Minimum",
                                              min_value=0,
                                              max_value=100,
                                              value=None,
                                              step=1,
                                              format="%d%%", key="ebitda_cagr_5y") if show_ebitda_cagr_5y_filter else None

show_fcf_yoy_growth_filter = st.sidebar.checkbox("FCF Growth (YoY)")
min_fcf_yoy_growth = st.sidebar.slider("Minimum",
                                       min_value=0,
                                       max_value=100,
                                       value=None,
                                       step=1,
                                       format="%d%%", key="fcf_yoy") if show_fcf_yoy_growth_filter else None

show_fcf_cagr_5y_filter = st.sidebar.checkbox("Free Cash Flow Growth (5y)")
min_fcf_cagr_5y_growth = st.sidebar.slider("Minimum",
                                           min_value=0,
                                           max_value=100,
                                           value=None,
                                           step=1,
                                           format="%d%%", key="fcf_cagr_5y") if show_fcf_cagr_5y_filter else None

show_ebit_margin_filter = st.sidebar.checkbox("EBIT Margin")
min_ebit_margin = st.sidebar.slider("Minimum",
                                     min_value=0,
                                     max_value=100,
                                     value=None,
                                     step=1,
                                     format="%d%%", key="ebit_margin") if show_ebit_margin_filter else None

show_fcf_margin_filter = st.sidebar.checkbox("Free Cash Flow Margin")
min_fcf_margin = st.sidebar.slider("Minimum",
                                   min_value=0,
                                   max_value=100,
                                   value=None,
                                   step=1,
                                   format="%d%%", key="fcf_margin") if show_fcf_margin_filter else None

show_netdebt_ebitda_filter = st.sidebar.checkbox("Net Debt to EBITDA")
max_netdebt_ebitda = st.sidebar.slider("Maximum",
                                       min_value=0,
                                       max_value=100,
                                       value=None,
                                       step=1,
                                       key="netdebt_ebitda") if show_netdebt_ebitda_filter else None

show_roic_filter = st.sidebar.checkbox("ROIC")
min_roic = st.sidebar.slider("Minimum",
                             min_value=0,
                             max_value=100,
                             value=None,
                             step=1,
                             format="%d%%", key="roic") if show_roic_filter else None

show_roiic_filter = st.sidebar.checkbox("ROIIC")
min_roiic = st.sidebar.slider("Minimum",
                              min_value=0,
                              max_value=100,
                              value=None,
                              step=1,
                              format="%d%%", key="roiic") if show_roiic_filter else None

show_ev_fcf_filter = st.sidebar.checkbox("EV/FCF")
max_ev_fcf = st.sidebar.slider("Maximum",
                               min_value=0,
                               max_value=100,
                               value=None,
                               step=1,
                               key="ev_fcf") if show_ev_fcf_filter else None

show_ev_ebitda_filter = st.sidebar.checkbox("EV/EBITDA")
max_ev_ebitda = st.sidebar.slider("Maximum",
                                  min_value=0,
                                  max_value=100,
                                  value=None,
                                  step=1,
                                  key="ev_ebitda") if show_ev_ebitda_filter else None

# Filter the DataFrame based on the selected filters
filtered_df = df[
    (df['calendarYear'] == selected_year) &
    (df['sector'].isin(selected_sectors)) &
    (df['exchangeShortName'].isin(selected_exchanges)) &
    (df['reportedCurrency'].isin(selected_currencies)) &
    ((df['revenue_yoy_growth'] >= min_revenue_yoy_growth / 100) if show_revenue_growth_filter else True) &
    ((df['revenue_cagr_5y'] >= min_revenue_cagr_5y_growth / 100) if show_revenue_cagr_5y_filter else True) &
    ((df['ebitda_yoy_growth'] >= min_ebitda_yoy_growth / 100) if show_ebitda_yoy_growth_filter else True) &
    ((df['ebitda_cagr_5y'] >= min_ebitda_cagr_5y_growth / 100) if show_ebitda_cagr_5y_filter else True) &
    ((df['fcf_yoy_growth'] >= min_fcf_yoy_growth / 100) if show_fcf_yoy_growth_filter else True) &
    ((df['fcf_cagr_5y'] >= min_fcf_cagr_5y_growth / 100) if show_fcf_cagr_5y_filter else True) &
    ((df['ebit_margin'] >= min_ebit_margin / 100) if show_ebit_margin_filter else True) &
    ((df['fcf_margin'] >= min_fcf_margin / 100) if show_fcf_margin_filter else True) &
    ((df['netdebt_ebitda'] <= max_netdebt_ebitda / 100) if show_netdebt_ebitda_filter else True) &
    ((df['roic'] >= min_roic / 100) if show_roic_filter else True) &
    ((df['roiic'] >= min_roiic / 100) if show_roiic_filter else True) &
    ((df['ev_fcf'] <= max_ev_fcf / 100) if show_ev_fcf_filter else True) &
    ((df['ev_ebitda'] <= max_ev_ebitda / 100) if show_ev_ebitda_filter else True)
]
# Multiply 'revenue_yoy_growth' by 100 in the filtered DataFrame
filtered_df.loc[:, 'revenue_yoy_growth'] = filtered_df['revenue_yoy_growth'] * 100
filtered_df.loc[:, 'revenue_cagr_5y'] = filtered_df['revenue_cagr_5y'] * 100
filtered_df.loc[:, 'ebitda_yoy_growth'] = filtered_df['ebitda_yoy_growth'] * 100
filtered_df.loc[:, 'ebitda_cagr_5y'] = filtered_df['ebitda_cagr_5y'] * 100
filtered_df.loc[:, 'fcf_yoy_growth'] = filtered_df['fcf_yoy_growth'] * 100
filtered_df.loc[:, 'fcf_cagr_5y'] = filtered_df['fcf_cagr_5y'] * 100
filtered_df.loc[:, 'ebit_margin'] = filtered_df['ebit_margin'] * 100
filtered_df.loc[:, 'fcf_margin'] = filtered_df['fcf_margin'] * 100
filtered_df.loc[:, 'roic'] = filtered_df['roic'] * 100
filtered_df.loc[:, 'roiic'] = filtered_df['roiic'] * 100

# Leave 'netdebt_ebitda', 'ev_fcf', 'ev_ebitda' as numeric values (remove multiplication by 100)
filtered_df.loc[:, 'netdebt_ebitda'] = filtered_df['netdebt_ebitda']
filtered_df.loc[:, 'ev_fcf'] = filtered_df['ev_fcf']
filtered_df.loc[:, 'ev_ebitda'] = filtered_df['ev_ebitda']

# Display the filtered DataFrame with specific columns
filtered_df_display = filtered_df[['companyName', 'sector', 'revenue_yoy_growth', 'revenue_cagr_5y', 'ebitda_yoy_growth', 'ebitda_cagr_5y', 'fcf_yoy_growth', 'fcf_cagr_5y', 'ebit_margin', 'fcf_margin', 'netdebt_ebitda', 'roic', 'roiic', 'ev_fcf', 'ev_ebitda']]

# Rename columns for display
filtered_df_display.columns = ['Company Name', 'Sector', 'Revenue Growth (YoY)', 'Revenue Growth (5y)', 'EBITDA YoY Growth', 'EBITDA Growth (5y)', 'FCF YoY Growth', 'Free Cash Flow Growth (5y)', 'EBIT Margin', 'Free Cash Flow Margin', 'Net Debt EBITDA', 'ROIC', 'ROIIC', 'EV/FCF', 'EV/EBITDA']

# Display the DataFrame with the correct percentage format
st.dataframe(filtered_df_display.style.format({
    'Revenue Growth (YoY)': "{:.2f}%",
    'Revenue Growth (5y)': "{:.2f}%",
    'EBITDA YoY Growth': "{:.2f}%",
    'EBITDA Growth (5y)': "{:.2f}%",
    'FCF YoY Growth': "{:.2f}%",
    'Free Cash Flow Growth (5y)': "{:.2f}%",
    'EBIT Margin': "{:.2f}%",
    'Free Cash Flow Margin': "{:.2f}%",
    'Net Debt EBITDA': "{:.2f}",  # Display as numeric
    'ROIC': "{:.2f}%",
    'ROIIC': "{:.2f}%",
    'EV/FCF': "{:.2f}",  # Display as numeric
    'EV/EBITDA': "{:.2f}"  # Display as numeric
}))
