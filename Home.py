import streamlit as st
import plotly.graph_objs as go
import numpy as np
from scipy.stats import norm


st.set_page_config(page_title="Dashboard",page_icon="🌍" ,layout="wide")
st.subheader("Confidence Level:")

#all graphs we use custom css not streamlit 
theme_plotly = None 

# load Style css
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

#sidebar
st.sidebar.image("logo1.png")

def z_score_from_confidence_level(confidence_level):
    if confidence_level <= 1:
        z_score = norm.ppf(1 - (1 - confidence_level) / 2)
    else:
        confidence_level = confidence_level / 100  # convert percentage to decimal
        z_score = norm.ppf(1 - (1 - confidence_level) / 2)
    return z_score

def main():
    
    confidence_input = st.text_input("Confidence Level")

    if confidence_input:
        try:
            confidence = float(confidence_input.strip('%')) if '%' in confidence_input else float(confidence_input)
            z_score = z_score_from_confidence_level(confidence)

            x = np.linspace(-3, 3, 1000)
            y = norm.pdf(x, 0, 1)

            data = [
                go.Scatter(x=x, y=y, mode='lines', name='Normal Distribution'),
                go.Scatter(x=[z_score, z_score], y=[0, norm.pdf(z_score)], mode='lines', name=f'Z-score: {z_score:.2f}', line=dict(color='red', dash='dash')),
                go.Scatter(x=[0, 0], y=[0, norm.pdf(0)], mode='lines', name='Mean', line=dict(color='green', dash='dash'))
            ]

            layout = go.Layout(title='',
                               xaxis=dict(title='Z-score'),
                               yaxis=dict(title='Probability Density'))

            if confidence <= 1:
                shade_x = np.linspace(-3, z_score, 1000)
            else:
                shade_x = np.linspace(-3, z_score, 1000)
            shade_y = norm.pdf(shade_x, 0, 1)

            data.append(go.Scatter(x=shade_x, y=shade_y, mode='lines', fill='tozeroy', name=f'{confidence*100}% CI', fillcolor='rgba(0,100,80,0.2)'))

            fig = go.Figure(data=data, layout=layout)
            st.success(f"Z-score for {confidence_input} confidence level: {z_score:.4f}")
            with st.expander("VIEW NORMAL CURVE"):
             st.plotly_chart(fig,use_container_width=True)

            
        except ValueError:
            st.error("Please enter a valid confidence level")
main()

      