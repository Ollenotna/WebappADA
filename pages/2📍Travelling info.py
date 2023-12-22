import streamlit as st
import pandas as pd
import pickle as pkl
import numpy as np
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns

# from dash import Dash, dcc, html, Input, Output
# from jupyter_dash import JupyterDash

# Config
st.set_page_config(page_title='Be(er)AGuide', page_icon=':beer:')

# Title
st.title('The beer guide for travelers')

st.write(
    """
    Do you sometimes realize on the amount of decisions you make every time you plan a new trip? From straightforward choices like selecting restaurants 
    and activities to more complex ones as considering the time of year, the country, the duration and list goes on. Here, we aimed to streamline this 
    decision making process for people that like BEER. We have characterized several countries around the globe in terms of proportion of industrial and 
    local breweries, along with the preferred beer styles during each trimester of the year. Furthermore, we've provided descriptions of beer styles by 
    keywords gathered among all the users in the platforms. Our goal with the following beerlogue is to facilitate the exploration of new beer styles and 
    simplify the decision-making process for your upcoming travels """)

st.write('''
''')

st.markdown("""---""")

st.header("🏭  Querying a country's brewing culture")
st.write(
    """
    We started by surveying breweries in countries containing more than 30 breweries. aiming to delineate between those categorized as 
    industrial breweries and local breweries. The traditional beer terminology (nano, micro and macrobreweries) is linked to annual barrel production,
    rather to the variety of beers produced. In this study, we didn't have information about the anual barrel production for each brewery, therefore,
    we came up with a simpler clasification: breweries producing fewer than 15 beer varieties were classified as local, while those producing 15 or more 
    were categorized as industrial. """)

st.write(
    """
    Our thresholding for local versus industrial breweries pivots on the following factors. First, we consider the availability of beers outside their countries 
    of origin. Industrial breweries tipically reach a broader ranger of countries due to their scale of production. Breweries producing few beers can be 
    probably associated to low production. Secondly, this classification can offer insights about the countries' beer culture. Countries with a higher prevalence
    of local breweries might have a richer craft culture for travelers seeking authentic and diverse beer experiences. 
    """
)

st.write(
    """
    The following plot depicts the level of locality or industriality among countries having more than 30 breweries. Insteristingly, the arrangement of 
    countries according to their levels of locality and industriality matches their current development categorization. Developing countries occupy the upper
    side of the plot, while developed nations tend to position at the bottom. These results can help travelers deliberating between destinations characterized 
    by a perhaps more crafted beer culture or those more industrialized.
    """
)


st.image('figures/locality.jpeg')

st.markdown("""---""")
st.header("🕺🏽 How preferred beer styles vary across countries and seasons")


st.write(
    """
    In our ongoing exploration to find the best travel destinations based on beer experiences, this section dives into the global distribution of the popularity 
    and the rating-based preferences of various beer styles across different countries and seasons. We defined the beer style’s country based on the brewery 
    location. The key ideas here are that, first, we suspect that the period of the year influences the beer consumption patterns, where weather and events influence 
    the preferences towards specific beer styles. Second, one may think that a high number of reviews for a particular beer style often indicates its popularity as a 
    positive characteristic. However, it's crucial to note that this metric doesn't reflect the beer's quality or the reviewer's true sentiment, as reviews can be 
    diverse, and some may just express complaints. 
    """
)

T1_reviews = pd.read_csv('Data/web/T1_reviews.csv', index_col= 0)
T2_reviews = pd.read_csv('Data/web/T2_reviews.csv', index_col= 0)
T3_reviews = pd.read_csv('Data/web/T3_reviews.csv', index_col= 0)
T4_reviews = pd.read_csv('Data/web/T4_reviews.csv', index_col= 0)

def pie_chart(country):

        fig = make_subplots(rows=2, cols=2, subplot_titles= ['January-March', 'April-June', 'July-September', 'October-December'],
                                specs=[[{'type': 'domain'}, {'type': 'domain'}], [{'type': 'domain'}, {'type': 'domain'}]])


        T1_pie = px.pie(T1_reviews.T, values= country, names=T1_reviews.T.index.values, hole=0.3)
        fig.add_trace(T1_pie['data'][0], 1, 1)

        # Add pie chart for winter_reviews
        T2_pie = px.pie(T2_reviews.T, values= country, names=T2_reviews.T.index.values, hole=0.3)
        fig.add_trace(T2_pie['data'][0], 1, 2)

        # Add pie chart for summer_reviews
        T3_pie = px.pie(T3_reviews.T, values= country, names=T3_reviews.T.index.values, hole=0.3)
        fig.add_trace(T3_pie['data'][0], 2, 1)

        T4_pie = px.pie(T4_reviews.T, values= country, names=T4_reviews.T.index.values, hole=0.3)
        fig.add_trace(T4_pie['data'][0], 2, 2)

        # Update layout if needed
        fig.update_layout(
                title_text="Top4 most reviewed beer styles in a country per season", 
                width = 800, height = 800)
        
        #Add annotations in the center of the donut pies.
        fig.update_traces(textposition = 'inside')
        return fig


option = st.selectbox('Select a country you are interested in visiting?',
        (np.sort(T2_reviews.index.unique())))

fig = pie_chart(option)
    
st.plotly_chart(fig)

st.write(
    """
    Fortunately, by considering user information such as ratings for each beer style and the number of reviews they've contributed, we can calculate a 
    weighted average. We assume that users with a substantial number of reviews are beer experts, giving their opinions more significance. This approach 
    helps us identify the best beer styles, steering clear of being overly influenced by subjective complaints from amateurs, like those who dislike the 
    bitterness of IPAs.
    """
)


world_preference = pd.read_csv('Data/web/World_map_beer_preferences.csv', index_col= 0)

palette_styles = {'Bock': (0.12156862745098039, 0.4666666666666667, 0.7058823529411765),
 'Hybrid Beer': (0.6823529411764706, 0.7803921568627451, 0.9098039215686274),
 'Pale Ale': (1.0, 0.4980392156862745, 0.054901960784313725),
 'Pilsner & Pale Lager': (1.0, 0.7333333333333333, 0.47058823529411764),
 'Dark Lager': (0.17254901960784313, 0.6274509803921569, 0.17254901960784313),
 'Stout': (0.596078431372549, 0.8745098039215686, 0.5411764705882353),
 'Amber Ale': (0.8392156862745098, 0.15294117647058825, 0.1568627450980392),
 'IPA': (1.0, 0.596078431372549, 0.5882352941176471),
 'Brown/Dark Ale': (0.5803921568627451, 0.403921568627451, 0.7411764705882353),
 'Porter': (0.7725490196078432, 0.6901960784313725, 0.8352941176470589),
 'Herbs/Vegetables': (0.5490196078431373,
  0.33725490196078434,
  0.29411764705882354),
 'Wheat Beer': (0.7686274509803922, 0.611764705882353, 0.5803921568627451),
 'Smoked': (0.8901960784313725, 0.4666666666666667, 0.7607843137254902),
 'Strong Pale Ale': (0.9686274509803922,
  0.7137254901960784,
  0.8235294117647058),
 'Ale': (0.4980392156862745, 0.4980392156862745, 0.4980392156862745),
 'Strong Brown/Dark Ale': (0.7803921568627451,
  0.7803921568627451,
  0.7803921568627451),
 'Strong Ale': (0.7372549019607844, 0.7411764705882353, 0.13333333333333333),
 'Wild/Sour Beer': (0.8588235294117647,
  0.8588235294117647,
  0.5529411764705883),
 'Low Alcohol': (0.09019607843137255, 0.7450980392156863, 0.8117647058823529),
 'Cocktails': (0.6196078431372549, 0.8549019607843137, 0.8980392156862745)}

winter, spring, summer, autumn = st.tabs(['Jan-Mar', 'Apr-Jun', 'Jul-Sep', 'Oct-Dec'])

beer_style_color_map_rgb = {key: f'rgb({int(r * 255)},{int(g * 255)},{int(b * 255)})'
                                for key, (r, g, b) in palette_styles.items()}

with winter:
    
    fig = px.choropleth(world_preference, locations="iso_alpha", 
                        color='T1', # lifeExp is a column of gapminder
                        hover_name="country_brewery", # column to add to hover information
                        color_discrete_map= beer_style_color_map_rgb
                        ) #Color
    st.plotly_chart(fig)

with spring:

    fig = px.choropleth(world_preference, locations="iso_alpha", 
                        color='T2', # lifeExp is a column of gapminder
                        hover_name="country_brewery", # column to add to hover information
                        color_discrete_map= beer_style_color_map_rgb
                        ) #Color
    st.plotly_chart(fig)

with summer:

    fig = px.choropleth(world_preference, locations="iso_alpha", 
                        color='T3', # lifeExp is a column of gapminder
                        hover_name="country_brewery", # column to add to hover information
                        color_discrete_map= beer_style_color_map_rgb
                        ) #Color
    st.plotly_chart(fig)

with autumn:

    fig = px.choropleth(world_preference, locations="iso_alpha", 
                        color='T4', # lifeExp is a column of gapminder
                        hover_name="country_brewery", # column to add to hover information
                        color_discrete_map= beer_style_color_map_rgb
                        ) #Color
    st.plotly_chart(fig)

st.write(
    """
Therefore, when we analyze the graphs, by observing the color distribution, we can see the distinction between the most reviewed beer styles and those that 
people genuinely prefer based on ratings. This aids us in pinpointing the truly outstanding beer styles.
    """
)

st.markdown("""---""")


st.header("🖋️ Words beyond numbers and beer styles")


st.markdown('''During our exploration, we delved into the dataset, scrutinizing various aspects such as countries, 
            distinctive brewery characteristics, and favored beer styles. Concluding our analysis, we want to shift 
            our focus to user perspectives, particularly honing in on reviews.''')
            
st.markdown('''In the realm of reviews, a score serves as a condensed summary of the overall user experience, but the true 
            essence lies in the narrative conveyed through words. For this reason, we analyzed the reviews provided by the users. Our text analysis focuses only 
            on the English reviews has they constitutes the largest portion of the data. Another reason for choosing English 
            reviews is based on the natural language processing (NLP) pipeline we used. Following language detection, we prepared 
            the text by eliminating stop words, punctuation, emojis, and other not-relevant elements described in the 
            Text_prepocessing.py function. To facilitate the creation of a TF-IDF matrix and reduce sparsity, our final step 
            involved text normalization.''')

st.image('figures/language.jpeg')


st.markdown('''To identify keywords describing each review, we then identified the top-3-words for each review based on the TF-IDF 
            score to identify. Grouping these keywords by the different columns in the data frame (macro_style, year, abv) allowed us 
            to appreciate the descriptive power of words in conveying concepts beyond numerical scores.''')

st.markdown('''Considering our audience comprised both by novice and expert beer enthuasiasts, we sought to delve into the prevalent words used in describing specific beer 
            styles. Our approach helps individuals exploring new beer styles or those looking to deepen their appreciation for other styles
             rather than the established favorites. Notably, the analysis revealed intriguing associations between certain keywords and beer
             styles:''')
st.markdown('''- **Conventional terminology**: These words are commonly describing the category they fall into. For instance, the cocktail 
            category was characterized by words like "liquor," "apple," "alcohol," and "watermelon," directly evoking the style or its 
            ingredients and the same effect can be noticed in the herbs/vegetable category.''')
st.markdown('''- **Unconventional terminology**: Exploration of smoked macro styles unearthed words such as "bacon," "ham," and "campfire," 
            indicating users' tendency to exploit unconventional vocabulary for linking concepts through sensory expression. The same effect 
            was observable for the herbs/vegetable category. ''')
st.markdown('''- **Geographical insights:** Moreover, the analysis unveiled words indicative of the geographical origins of beer styles. For 
            instance, reviews associated with Ale and Strong Ale categories frequently featured the term "Belgium," reflecting the beers' 
            English and Belgian roots. It must be taken into account that these observation can be biased by the group construction.''')

st.image('figures/wordclouds.jpeg')