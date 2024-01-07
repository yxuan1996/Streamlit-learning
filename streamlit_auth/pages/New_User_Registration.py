import streamlit_authenticator as stauth
import streamlit as st
import pandas as pd
import numpy as np
import yaml
from yaml.loader import SafeLoader

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

st.title('New User Registration')

try:
    if authenticator.register_user('Register user', preauthorization=False):
        st.success('User registered successfully')
        with open('./config.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
except Exception as e:
    st.error(e)