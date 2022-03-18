from cmath import nan
from random import gammavariate
from shutil import copyfileobj
import streamlit as st
import requests
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.graph_objs import *





# ---- Welcome text
st.markdown("""
         # DealCircle recommender
         Welcome to the recommender app 👋. \n
         Let's match investors and target companies for a higher chance of a successful deal!
         """)


# ---- Create an expandable "Help" section for instructions
with st.expander("Help!"):
    st.markdown("""

             To generate a recommendation, open the sidebar, fill in the target information and click on "Display recommendations".

             If you get an error, double-check that you filled in the data accurately.

             The required input data types are:\n

             - Deal ID: number
             - Deal name: words and/or number
             - Target company ID: number
             - Target name: words and/or number
             - Target description: words and/or number
             - Target revenue: number
             - Target EBITDA: number
             - Target EBIT: number
             - Keywords: words, separated by a comma

             """)


# ---- Sidebar with form to get new target information
st.sidebar.image(
    'https://c.smartrecruiters.com/sr-company-logo-prod-dc5/6168ff832f8fb46fc18533dc/huge?r=s3-eu-central-1&_1634271911128')


st.sidebar.markdown("""
                    ***Enter the target information below to generate \
                        recommendations.***
                    """)

deal_id = st.sidebar.text_input('Deal ID', "12340")
deal_name = st.sidebar.text_input('Deal name', "Fresh Air")
deal_type_name = st.sidebar.selectbox(
    'Deal type', ('MAJORITY', 'DISTRESSED', 'MINORITY', 'OTHER', 'VC'))
target_company_id = st.sidebar.text_input('Target company ID', "823401")
target_name = st.sidebar.text_input('Target name', "Filtration Test GmbH")
target_description = st.sidebar.text_input('Target description', "Filtertechnik ist ein weit gefasster Bereich, in dem die verschiedensten Filtertypen, Lösungen und Techniken zum Einsatz gelangen. Effektive Filtration, Adsorption und Separation sind unverzichtbare Bestandteile zahlreicher reibungsloser Abläufe in Industrie, Gewerbe")
target_revenue = st.sidebar.text_input('Target revenue')
target_ebitda = st.sidebar.text_input('Target EBITDA')
target_ebit = st.sidebar.text_input('Target EBIT')
country_name = st.sidebar.selectbox('Target country', ('Germany',
                                                       'Belgium',
                                                       'Bulgaria',
                                                       'Czechia',
                                                       'Egypt',
                                                       'Austria',
                                                       'Italy',
                                                       'Netherlands',
                                                       'Poland',
                                                       'Portugal',
                                                       'Romania',
                                                       'Slovakia',
                                                       'Spain',
                                                       'Switzerland',
                                                       'United States of America'))
region_name = st.sidebar.selectbox('Target region', ('Bavaria',
                                   'Baden-Württemberg',
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

# --- Initialising SessionState ---
if "load_state" not in st.session_state:
     st.session_state.load_state = False


#display = st.sidebar.button('Display recommendations')



response_df = None

# ---- Display recommendations list when clicking on display button
#if display:
if st.sidebar.button('Display recommendations') or st.session_state.load_state:
    st.session_state.load_state = True


    @st.cache
    def get_response():
        api_url = f'https://dealmatch-rec3-jlx73eg7oq-ew.a.run.app/recommend?deal_id={deal_id}&deal_name={deal_name}&deal_type_name={deal_type_name}&target_company_id={target_company_id}&target_name={target_name}&target_description={target_description}&target_revenue={target_revenue}&target_ebitda={target_ebitda}&target_ebit={target_ebit}&country_name={country_name}&region_name={region_name}&sector_name={sector_name}&strs={strs}'
        #api_url_test = f'https://127.0.0.1:8000/recommend?deal_id={deal_id}&deal_name={deal_name}&deal_type_name={deal_type_name}&target_company_id={target_company_id}&target_name={target_name}&target_description={target_description}&target_revenue={target_revenue}&target_ebitda={target_ebitda}&target_ebit={target_ebit}&country_name={country_name}&region_name={region_name}&sector_name={sector_name}&strs={strs}'
        response = requests.get(api_url).json()
        print(response)
        response_df = pd.DataFrame(
            {'name': list(response['name'].values()),
            'match_probability': list(response['match_probability'].values()),
            'description': list(response['description'].values()),
            'distance_target<=>investor': list(response['distance_target<=>investor'].values()),
            'Rationale': list(response['Rationale'].values())})
        response_df = pd.DataFrame(response_df, index=list(range(0, 10)))
        response_df.index = np.arange(1, len(response_df)+1)
        return response_df

    response_df = get_response()
    #st.dataframe(response_df)

    def convert_results(df):
        return df.to_csv().encode('utf-8')

    csv_to_download = convert_results(response_df)

    st.download_button(
        label="Download results",
        data=csv_to_download,
        file_name='deal_match_results.csv'
    )


    #st.markdown("""
     #       **Your results**
      #      """)
    st.write('**The result:**', len(response_df), '**investors**')


if response_df is not None:

    if "row" not in st.session_state:
        st.session_state.row = 0

    def next_row():
        st.session_state.row += 1

    def prev_row():
        st.session_state.row -= 1


    col1, col2, col3, col4, col5 = st.columns(5)

    if st.session_state.row < len(response_df.index)-1:
        col2.button(">", on_click=next_row)

    else:
        col2.write("")

    if st.session_state.row > 0:
        col1.button("<", on_click=prev_row)

    else:
        col1.write("")

    row_df = pd.DataFrame(
        {'name': [list(response_df['name'])[st.session_state.row]],
            'match_probability': [list(response_df['match_probability'])[st.session_state.row]],
            'description': [list(response_df['description'])[st.session_state.row]],
            'distance_target<=>investor': [list(response_df['distance_target<=>investor'])[st.session_state.row]],
            'Rationale': [list(response_df['Rationale'])[st.session_state.row]]},index=[int(st.session_state.row)+1])


    #st.write(row_df)
    st.dataframe(row_df)


    def get_visual_data():
        df = pd.read_csv('sector_investors.csv',sep=';',index_col=0)
        return df

    def create_frame(df, investor_name):
        frame_1 = df[df['deal_stage_id']>=3]
        #frame_1 = df
        frame_2 = frame_1[['name', 'sector_id', 'name_de', 'target_revenue', 'target_ebitda', 'target_ebit', 'region']]
        frame_3 = frame_2[frame_2['name'] == investor_name]
        frame_4 = frame_3.groupby([frame_3['name_de']],as_index=False).agg({
            'sector_id':
            'count',
            'target_revenue':
            'median',
            'target_ebitda':
            'median'})
        frame_4.rename(columns={'sector_id': 'match count'}, inplace=True)

        return frame_4


    def visualize(investor_name):

        df = get_visual_data()

        df = create_frame(df, investor_name)

        if not df.empty and not ((df['target_ebitda'].sum() +  df['target_revenue'].sum()) ==0 ):



            fig = px.scatter(df, x="target_ebitda", y="target_revenue", color="match count",
                     size='match count', hover_data=['name_de'],template='gridon',
                     labels={
                     "target_revenue": "Median Revenue",
                     "target_ebitda": "Median Ebitda",
                     "name_de": "Sector"
                 },width=800, height=500)


            return st.plotly_chart(fig)


        else:

            return st.markdown("""**NO GRAPH DATA AVAILABLE**""")


    st.set_option('deprecation.showPyplotGlobalUse', False)

    try:
        st.pyplot(visualize(row_df['name'].values[0]))

    except:
        pass
