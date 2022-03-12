from cmath import nan
from shutil import copyfileobj
import streamlit as st
import requests
import pandas as pd

st.markdown("""
         # DealCircle Recommender
         Welcome to the recommender app. Match investors and companies \
             for a higher chance of a successful deal.
         """)

st.sidebar.image(
    'https://c.smartrecruiters.com/sr-company-logo-prod-dc5/6168ff832f8fb46fc18533dc/huge?r=s3-eu-central-1&_1634271911128')

st.sidebar.markdown("""
                    ***Enter the target information below to generate \
                        recommendations.***
                    """)
deal_id = st.sidebar.text_input('Deal ID')
deal_name = st.sidebar.text_input('Deal name')
deal_type_name = st.sidebar.selectbox(
    'Deal type', ('DISTRESSED', 'MAJORITY', 'MINORITY', 'OTHER', 'VC'))
target_company_id = st.sidebar.text_input('Target company ID')
target_name = st.sidebar.text_input('Target name')
target_description = st.sidebar.text_input('Target description')
target_revenue = st.sidebar.text_input('Target revenue')
target_ebitda = st.sidebar.text_input('Target EBITDA')
target_ebit = st.sidebar.text_input('Target EBIT')
country_name = st.sidebar.selectbox('Target country', ('Austria',
                                                       'Belgium',
                                                       'Bulgaria',
                                                       'Czechia',
                                                       'Egypt',
                                                       'Germany',
                                                       'Italy',
                                                       'Netherlands',
                                                       'Poland',
                                                       'Portugal',
                                                       'Romania',
                                                       'Slovakia',
                                                       'Spain',
                                                       'Switzerland',
                                                       'United States of America'))
region_name = st.sidebar.selectbox('Target region', ('Baden-Württemberg',
                                   'Bavaria',
                                   'Berlin',
                                   'Brandenburg',
                                   'Bremen',
                                   'Hamburg',
                                   'Hesse',
                                   'Lower Saxony',
                                   'Mecklenburg-Vorpommern',
                                   'North Rhine-Westphalia',
                                   'Rhineland-Palatinate',
                                   'Saarland',
                                   'Saxony',
                                   'Saxony-Anhalt',
                                   'Schleswig-Holstein',
                                   'Thuringia'))
sector_name = st.sidebar.selectbox('Target sector', ('Agriculture',
                                   'Automotive',
                                   'Biotechnology & Life Sciences',
                                   'Chemicals',
                                   'Computer Hardware & Equipment',
                                   'Construction',
                                   'Consumer Goods & Apparel',
                                   'Defense',
                                   'Electronics',
                                   'Energy',
                                   'Financial Services',
                                   'Food & Beverages',
                                   'Food & Staples Retailing',
                                   'Health Care Equipment & Services',
                                   'IT services',
                                   'Industrial automation',
                                   'Industrial products and services',
                                   'Insurance',
                                   'Internet/ecommerce',
                                   'Leisure & consumer services',
                                   'Manufacturing (other)',
                                   'Media',
                                   'Mining',
                                   'Pharmaceuticals',
                                   'Professional Services (B2B)',
                                   'Real Estate',
                                   'Retailing',
                                   'Semiconductors & Semiconductor Equipment',
                                   'Software & Services',
                                   'Telecommunication Hardware',
                                   'Telecommunication Services',
                                   'Transportation',
                                   'Utilities'))
strs = st.sidebar.text_input('Keywords')
display = st.sidebar.button('Display recommendations')


if display:
    st.markdown("""
            **Your results**
            """)

    unsupervised_api_url = f'https://dealmatchrec-1-jlx73eg7oq-ew.a.run.app/recommend?deal_id={deal_id}&deal_name={deal_name}&deal_type_name={deal_type_name}&target_company_id={target_company_id}&target_name={target_name}&target_description={target_description}&target_revenue={target_revenue}&target_ebitda={target_ebitda}&target_ebit={target_ebit}&country_name={country_name}&region_name={region_name}&sector_name={sector_name}&strs={strs}'
    response = requests.get(unsupervised_api_url).json()
    response_df = pd.DataFrame(response, index=list(range(0, 10)))
    st.dataframe(response_df)

    def convert_results(df):
        return df.to_csv().encode('utf-8')

    csv_to_download = convert_results(response_df)

    st.download_button(
        label="Download results",
        data=csv_to_download,
        file_name='deal_match_results.csv'
    )

# API https://dealmatchrec-1-jlx73eg7oq-ew.a.run.app
