import streamlit as st
import pandas as pd
import numpy as np

st.markdown("# Multi-language Enterprise Generative AI Platform 🎉")
st.sidebar.markdown("Contact Info & Controller ")



# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

st.sidebar.text_area('Contact Infomation', 
                      'Please leave your contact information on here! We would reach out to you!!')


tab1, tab2, tab3 = st.tabs(["Key Problems & Solutions","Why us?","Service & Product"])

with tab2:
    col1, col2 = st.columns(2,gap = "medium")
    with col1:
       st.image('src/IMG_5301 2.JPG', width = 360)

    with col2:
       st.markdown('### Why Us?')
       '''
       1. **User-Friendly Interface:** The platform features a user-friendly interface that allows users to easily visualize, manipulate, and explore their data, without requiring specialized technical skills.

       2. **Advanced Analytics:** The platform includes advanced analytics capabilities, such as machine learning algorithms, predictive modeling, and statistical analysis, allowing users to uncover insights and make data-driven decisions.
       
       3. **Scalability and Security:** The platform is designed to be scalable and secure, ensuring that it can accommodate growing amounts of data and protect sensitive information.
       '''
    st.image('src/22391676133642_.pic.jpg')
with tab1:
    st.markdown('## Data Growth Hacker!')
    st.video('src/pexels-rostislav-uzunov-7385122.mp4')

    '''
    ### Key Problems!
    1. Does your business facing a Data swamp?
    2. Does you always difficult to find insight from complex data, uncleaned data, and data that cannot provide real-time analysis?
   
    '''
    col1, col2 = st.columns(2,gap = "medium")
    with col1:
        '''
        #### 1.KYC:
        **(Know your Customers)**
        1. What age group is best to target your business with?
        2. What user characteristics are most important for your business to focus on?
        3. Which users have the strongest spending power?
        4. Which customer segment has the highest customer value?
        
        -------------- RUN Your Business ---------------->>>>
        '''
    with col2:
        '''
        ------
        #### 2.KYB:  
        **(Know your Business)**
        1. What industry is the key account strategy area that your business needs to focus on？
        2. Where are the components and growth points of the company's business？
        3. Specify your brand's profitability and financial situation!
        4. How should your brand do product differentiation strategy in market share?
        '''
    '''
    -------
    ### Solutions
    - KPMG helps you give solid data suggestions from multiple dimensions including customers, company status, and market analysis to help your business grow at a high speed.
    - Know your customer! Know your business! And Empower one-step solution to make **GROWTH & REVENUE**!
    ####        ---  "You can be the DATA GROWTH HACKER FAST!!"
    '''    
with tab3:
    
    col1, col2 = st.columns(2)
    with col1:
       st.markdown('## Build your Own Data Report！')
       '''
        1. **Deep understanding your data profile!**
            KYC,KYB and Know your data!
            
        2. **Check your data Quality!**
            Ensure your data quality from 6 dimensions and not be deceived!
            
        3. **Powerful Analytics tools!**
           Analyze your data set in multiple dimensions and give you the most comprehensive advice！
           
        4. **Intelligent Suggestion!**
            Intelligently provide valuable insights for your preprocessing procedure.
            
        5. **Visualization and Dashboard!**
            Quick, colorful, informative dashboard to let you aim your target users.
        '''

    with col2:
       st.image('src/BIG-DATA.jpeg')
       st.image('src/7d5fd7da8b1a41799087aa517ef44a24.jpeg')
       









# @st.experimental_memo
# def load_data(url):
#     df = pd.read_csv(url)
#     return df

# df = load_data("https://github.com/plotly/datasets/raw/master/uber-rides-data1.csv")
# st.dataframe(df)

# st.button("Rerun")
