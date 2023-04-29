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
    st.markdown('## Let us Talking with Data by Generative AI!')
    st.video('src/pexels-rostislav-uzunov-7385122.mp4')

    '''
    ### Key Problems!
   - According to statistics, in 2021, Over 60 million (about 18.7% of the total), Chinese, French, Arabic, German, Russian, Korean, Vietnamese and so on. 
   - Therefore, it can be said that the United States has a considerable number of multilingual speakers, and a revolutionary product  should break down the language barrier(eg: Tiktok, youtube, Chrome, Office365). That is the 1st pain point the product needs to solve.
   - On the other side, with ChatGPT arise, we witnessed the LLM’s power, but it still has two 3 technical limitations need to pay attention to, that’s 2nd painpoint:
  
   
    '''
    col1, col2 = st.columns(2,gap = "medium")
    with col1:
        '''
        #### Limitations:
    1. Timeliness：The corpus GPT pretrained until 2021, which means that it could not give users a good answer if this information/data after 2021.
    
    2. Specific Domain：The corpus GPT pretrained comes from general Corpus in internet, but it just include external data instead of some core internal data owned by some specific domain’s and specific organizations(company, government, university)
    Prompt Input.
    
    3. Prompt Engineering: The prompt engineering is very useful in specific domains, especially in AIGC domain(Art, music, essay design etc.) But, it has a high bar that users could not control, so they usually just get not optimal results. We need to let users easily use and get an optimal result if products go to enterprise level and goto market.
Therefore, based on the aforementioned 2 main pain points and requirements and 3  limitations of LLM. We would develop an AI product that functions as a “Stepstone(AGI)” Or “Lego Block” 
        
        -------------- RUN Your Business ---------------->>>>
        '''
    with col2:
    '''
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
