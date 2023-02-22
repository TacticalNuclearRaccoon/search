from scrap_helpers import get_source, scrape_google, text_extractor_html, generate_summary

import streamlit as st

#from transformers import pipeline


#pipe = pipeline("summarization", model="plguillou/t5-base-fr-sum-cnndm")

header = st.container()
features = st.container()

with header:
	st.title('Search and summarize')
	
with features:
    
    #max_length = st.slider('Maximum summary length (words)', min_value=30, max_value=150, value=60, step=10)

    query = st.text_area('Enter Keyword:' ) 
    
    submit = st.button('Generate')  

    if submit:
    
        st.subheader("Results:")
    
        with st.spinner(text="This may take a moment..."):
            
            results = scrape_google(query)
            
            for result in results:
                try:
                    text = text_extractor_html(result)
                    summary = generate_summary(text)
                    st.write(f'{result} \n {summary}\n')
                except:
                    st.write(f'{result} text is forbidden (403)')
