import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def shorten_age(categories,cut_off):
    categorical_map={}
    for i in range(len(categories)):
        if categories.values[i] >=cut_off:
             categorical_map[categories.index[i]]=categories.index[i]
        else:
            categorical_map[categories.index[i]]='Other_age'
    return categorical_map    

def shorten_categories(categories,cut_off):
    categorical_map={}
    for i in range(len(categories)):
        if categories.values[i] >=cut_off:
             categorical_map[categories.index[i]]=categories.index[i]
        else:
            categorical_map[categories.index[i]]='Other'
    return categorical_map   

def Clean_yearcoding(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)   

def clean_education(x):
    if 'Master’s degree ' in x:
        return 'Masters'
    if 'Bachelor’s degree' in x:
        return "Bachelaors"
    if 'Other doctoral degree' in x :
        return 'Post Grad'
    return 'Less than Bachelors'     

@st.cache
def load_data():

    df=pd.read_csv("survey_results_public.csv")
    df=df.rename({'ConvertedCompYearly':'Salary'},axis=1)

    df=df[['EdLevel','Country','YearsCodePro','Age','Salary']]
    df=df.dropna()
    df=df[df['Salary']<= 250000]
    df=df[df['Salary']>= 10000]



    age_map=shorten_age(df.Age.value_counts(),500)
    df['Age']=df['Age'].map(age_map)

    country_map=shorten_categories(df.Country.value_counts(),600)
    df['Country']=df['Country'].map(country_map)
    df1 = df[df['Country'] == "Other"].index 
    df.drop(df1, inplace = True)
    

    df['YearsCodePro']=df['YearsCodePro'].apply(Clean_yearcoding)
    df['EdLevel']=df['EdLevel'].apply(clean_education)
    return df

df=load_data()

def show_explore_page():
    st.title('Explore the Software Engineer Salaries:.........')
    st.write("""
    
    ### Stack Overflow Developer Survey 2022
     """)
    data= df['Country'].value_counts()

    fig1,ax1=plt.subplots()
    ax1.pie(data,labels=data.index,autopct="%1.1f%%",shadow=True,startangle=90)
    ax1.axis("equal")

    st.write(""" ### Number of Data from Different Countries:""")
    st.pyplot(fig1)

    st.write("""
    ### Mean Salary Based on Country :...""")


    data =df.groupby(['Country'])['Salary'].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write(""" 
    ### Mean Salary based on the Experience:  """)

    data=df.groupby(['YearsCodePro'])['Salary'].mean().sort_values(ascending=True)
    st.line_chart(data)

    st.write("""
    ### Mean Salary Based on Education level :...""")
    data =df.groupby(['EdLevel'])['Salary'].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write("""
    ### Mean Salary Based on Age groups ...""")

    data =df.groupby(['Age'])['Salary'].mean().sort_values(ascending=True)
    st.bar_chart(data)




    