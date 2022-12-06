import streamlit as st
import pickle 
import numpy as np

def load_model():
    with open('saved_steps.pkl','rb') as file:
        data=pickle.load(file)

    return data

data=load_model()    

reg_loaded=data['model']
edu_loaded=data['label_edu']
country_loaded=data['label_country']
age_loaded=data['label_age']

def show_predict_page():
    st.title("Software Developer Salary Prediction:....")
    st.write(""" ### We need some information to predict the salary""")

    country=('United Kingdom of Great Britain and Northern Ireland',
       'United States of America', 'Canada', 'Germany', 'Poland',
       'Netherlands', 'Brazil', 'Spain', 'France', 'India')    

    education =('Masters', 'Bachelaors', 'Less than Bachelors', 'Post Grad')

    age=('25-34 years old', '18-24 years old', '35-44 years old',
       '55-64 years old', '45-54 years old', 'Other_age')

    country=st.selectbox("Country",country)  
    education=st.selectbox("Education",education) 
    age=st.selectbox("Age",age)   
    experience=st.slider("Years of Experience",0,50,3)

    ok=st.button("Calculate Salary")
    if ok:
        X= np.array([[education,country,experience,age]])
        X[:,3]=age_loaded.transform(X[:,3])
        X[:,1]=country_loaded.transform(X[:,1])
        X[:,0]=edu_loaded.transform(X[:,0])
        X=X.astype(float)
        

        salary=reg_loaded.predict(X)
        st.subheader(f"The estimated Salary is ${salary[0]:.2f}")