import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import plotly.express as px

# Config
st.set_page_config(page_title='Be(er)AGuide', page_icon=':beer:')

# Title
st.title('Where do beer reviews come from?')
st.markdown("""---""")

st.write(
    '''
    Beer Advocate and Rate Beer datasets consist of beer reviews coming from [beeradvocate](https://www.beeradvocate.com/) 
    and [ratebeer](https://www.ratebeer.com/) platforms respectively. Both dataset spans a period of more than 10 years,
    and include more than 2 million reviews. Moreover, both datasets contain general information about the users and the beers,
    for instance country of origin from the user, beer style, brewery in which the beer was produced and brewery locations.
    Moreover detailed information on the beer reviews is also provided, including numeric ratings in terms of five "aspects": 
    appearance, aroma, palate, taste, and overall impression, as well as text data provided by the reviewer and time and date 
    of each review.''')

st.write('''In this project we wanted to provide the travelers with a suggestion on where to go for their next holidays based on their 3 
    preferred beer styles. In this sense, to make the best prediction and have a better generalization, 
    we had to use as many data as possible, which in practical terms meant merging both datasets together. Thanks to the work done 
    by Prof. West (https://doi.org/10.1145/3178876.3186160), breweries, beers and users being common to both webpages had been 
    identified. Thus, to unify the data, the IDs of the so mentioned breweries, beers and users where unified to one (randomly 
    chosen to be RateBeer). The unique data from BearAdvocate was randomly assigned a new ID, excluding the IDs already used in 
    RateBeer to avoid confusion and allow to track back the data. ''')
    
st.write('''However, there is something else we need to consider: the herding effect! This can be described as a psychological phenomenon 
    that results in users adapting their rating to align to that of previous users. This happens, and it was demonstrated in P. 
    Wests article, since both webpages, when introducing a new rating, show the user giving the rating the average until that moment. 
    In order for the ratings to be comparable between both webpages, a detrending of the data was introduced. Analogous as to how 
    this phenomenon occurs, a linear regression was used to predict the difference between the users new rating and what was shown 
    to him on the webpage (the average until that moment, a.k.a an expanding average) and this was detrended from the scores, 
    individually for each database.''')

st.write('''With this unified and corrected data, we performed some data exploration included in the Github repository. Based on these 
         data exploration, we filtered the data as follows: we remove breweries with no beers associated to them, we deleted users that 
         did less than 20 reviews in total, we filtered out countries that had less than 30 breweries and we only kept countries that had
         at least 3 beer styles per trimester. The previous filtering parameters were applied in a consistent manner to all datasets.
         A detailed description of the filtering can be found on the main_preprocessing pipeline in the Github repository. ''')
         
st.write('''Countries that were split into different states/regions were further unified to keep the same configuration for all nations. 
         As an example, beer reviews originating from the different states of United States were unfied as one country named Unites States of America.
         This unification process was repeated for Canada and United Kindom too. Finally, due to the strict filtering on the countries, we provide 
         the following choropleth graph that depicts the retained countries as 'YES' and the filtered out countries as 'NO''')

data_map = pd.read_csv('Data/web/data_map.csv')

fig = px.choropleth(
    data_map,
    locations="iso",
    color="Used"
)

fig.update_geos(fitbounds="locations", visible=False)

st.plotly_chart(fig)

st.write('''To improve the interpretability of the beer styles, given their high number (180), we opted to reduce dimensionality by categorizing them into 
        20 classes named macro_styles. These classes were defined based on shared properties among the beers. Initially, ChatGPT was employed to extract 
        the general structure, but it proved incomplete results. Subsequently, [Craft Beer](https://www.craftbeer.com/) 's comprehensive database, grouping 
        styles by production procedure, color, bitterness, and alcohol level, was utilized for a more accurate classification. The following bar chart depicts 
         the 20 macro-styles that we have defined with their corresponding total number of reviews across both unified datasets.''')

st.image('figures/style_distribution.png')

st.write(
    """
    To enable the traveler to visualize and interpret our new macro-styles categorization, we have computed the following pie charts that enable you to visualize 
    what beer styles were grouped into each macro-style along with their proportion of reviews. 
    """
)

pie_chart_styles = pd.read_csv('Data/web/style_grouping.csv', index_col=0)

def styles_pie_chart(macro_style):
    df = pie_chart_styles # replace with your own data source
    fig = px.pie(df, values=macro_style, names=pie_chart_styles.index.values, hole=.3)
    return fig

option = st.selectbox('Select the macro-style you are interested in understanding its composition?', 
                      (np.sort(pie_chart_styles.columns.values)))

fig = styles_pie_chart(option)

st.plotly_chart(fig)