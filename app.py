from shutil import copyfileobj
import streamlit as st
import requests
import pandas as pd

st.markdown("""
         # Deal Match
         Welcome to the recommender app. Match investors and companies \
             for a higher chance of a successful deal. Please enter the \
                 target's information below to generate the list of \
                     recommendations.
         """)

deal_id = st.text_input('Deal ID')
deal_name = st.text_input('Deal name')
deal_type_name = st.text_input('Deal type')
target_company_id = st.text_input('Target company ID')
target_name = st.text_input('Target name')
target_description = st.text_input('Target description')
target_revenue = st.text_input('Target revenue')
target_ebitda = st.text_input('Target EBITDA')
target_ebit = st.text_input('Target EBIT')
country_name = st.text_input('Target country')
region_name = st.text_input('Target region')
sector_name = st.text_input('Target sector')
strs = st.text_input('Keywords')

st.markdown("""
            #### Your results:
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
