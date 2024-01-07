# Streamlit-learning

Demo app based on the tutorial: https://docs.streamlit.io/get-started/tutorials/create-an-app

EDA (Exploratory Data Analysis) app based on https://blog.streamlit.io/building-a-streamlit-and-scikit-learn-app-with-chatgpt/ 

Adding Authentication to Streamlit: See Authentication Section below
- https://blog.streamlit.io/streamlit-authenticator-part-1-adding-an-authentication-component-to-your-app/
- https://blog.streamlit.io/streamlit-authenticator-part-2-adding-advanced-features-to-your-authentication-component/

Further Reading: https://www.amazon.com/Web-Application-Development-Streamlit-Applications/dp/1484281101?linkCode=sl1&tag=kho_abd_her-20&linkId=ee9e303b3445d601f8ab440ddc81a4fc&language=en_US&ref_=as_li_ss_tl&ref=blog.streamlit.io

## Basics
### Installation
`pip install streamlit`

### Demo app
`streamlit hello`

### Running the app
```
streamlit run your_script.py
or
python -m streamlit run your_script.py
```

We can also pass an URL containing a python file to streamlit run
```
streamlit run https://raw.githubusercontent.com/streamlit/demo-uber-nyc-pickups/master/streamlit_app.py
```

## Displaying Data
### st.write() 

We can use `st.write()` to display data in streamlit apps. Streamlit will automatically infer the data format, whether it is text, dataframe or chart. 

```python
import streamlit as st
import pandas as pd

st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))
```

When we output a variable name by itself, streamlit will automatically display the data in the app using st.write()

```python
df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

df
```

### Charts
Line Chart
```python
st.line_chart(df)
```

Plot a Map (map_data dataframe should have ['lat', 'lon'] columns)
```python
st.map(map_data)
```

## Input Widgets
Widgets are used as data inputs. Example widgets are
- slider (To select a number)
- text_input
- checkbox
- selectbox

We should set the value of a widget as a variable. The variable will represent whatever the user has selected. 

```python
x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)
```

Use selectbox to select from a series of options
```python
option = st.selectbox(
    'Which number do you like best?',
     df['first column'])

'You selected: ', option
```

### Using Checkboxes to Show / Hide data
```python
if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    chart_data
```

### Show Progress
We can use `st.progress` to display the progress of a status in real-time (0-100)

```python
# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)
```


## Layout
### Sidebar
We can organize our input widgets on the left panel sidebar. 

If we want to add an input element to the sidebar, we use `st.sidebar.[widget]` instead of `st.[widget]`

Example
```python
# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)
```

### Columns
`st.columns()` allows us to place widgets and items side by side

```python
# Create 2 columns
left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
left_column.button('Press me!')

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")
```

## Cache
Cache allows us to store the results of computationally expensive function calls. 

To cache a function, we just need to decorate it with `@st.cache.data`

```python
@st.cache_data
def long_running_function(param1, param2):
    return …
```

## Session State
- Session State is a dictionary that persists data when the streamlit app reruns itself.
- We can save and retrieve data using dictionary notation `st.session_state["my_key"]`
- Session State is reactive (Similar to state in React JS). When the underlying value changes, the displayed state is updated automatically. 

Example Counter Page. 
- Everytime the button is clicked, the entire script is re-run and the `session_state.counter` is incremented.  
```python
import streamlit as st

if "counter" not in st.session_state:
    st.session_state.counter = 0

st.session_state.counter += 1

st.header(f"This page has run {st.session_state.counter} times.")
st.button("Run it again")
```

## DB connections
We save our database credentials in a TOML file (https://realpython.com/python-toml/)

The TOML file should be located in the `.streamlit/secrets.toml` directory relative to the main streamlit file. 

```
your-LOCAL-repository/
├── .streamlit/
│   └── secrets.toml # Make sure to gitignore this!
└── streamlit_app.py
```

Inside our `secrets.toml` file, we can save our credentials in the following format
```
[connections.my_database]
    type="sql"
    dialect="mysql"
    username="xxx"
    password="xxx"
    host="example.com" # IP or URL
    port=3306 # Port number
    database="mydb" # Database name
```

We can then establish a connection to our DB using `st.connection`

```python
conn = st.connection("my_database")
df = conn.query("select * from my_table")
st.dataframe(df)
```

## Multi-Pages
- In the folder containing your main script, create a new pages folder. Let’s say your main script is named main_page.py.
- Add new .py files in the pages folder to add more pages to your app.
- Run streamlit run main_page.py as usual.

- main_page.py will correspond to the main page of the app
- The filenames of the .py files in the pages folder will be the other pages

```
your-LOCAL-repository/
├── pages/
│   └── page2.py
│   └── page3.py
│   └── page4.py
└── main_page.py
```

## Authentication

https://github.com/mkhorasani/Streamlit-Authenticator

Install libraries
```
pip install streamlit-authenticator
```

Import library
```python
import streamlit_authenticator as stauth
```

#### Define Credentials
In the given example, we will storing our user credentials in a YAML file. 

In our YAML file we will define
- usernames
- hashed passwords
- JWT cookie settings such as expiry duration

We use the Hasher function to convert plaintext passwords to hashed passwords
```python
hashed_passwords = stauth.Hasher(['abc', 'def']).generate()
```

In our Python file, we load the credentials into the app
```python
import yaml
from yaml.loader import SafeLoader

with open('../config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
```

#### Login Widget
```python
name, authentication_status, username = authenticator.login('Login', 'main')
```

- 1st Arg: Name of Login Form
- 2nd Arg: Where to render (Main or Sidebar)

#### Authentication Check

We use the `authentication_status` variable to check if a user is authenticated or not. 

The key parameter is required for multipage applications. 

```python
if authentication_status:
    authenticator.logout('Logout', 'main', key='unique_key')
    st.write(f'Welcome *{name}*')
    st.title('Some content')
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
```

We can also access the same values using `st.session_state`

```python
if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main', key='unique_key')
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('Some content')
elif st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] == None:
    st.warning('Please enter your username and password')
```

We can use the `username` variable to further define user privileges

```python
name, authentication_status, username = authenticator.login('Login', 'main')
if authentication_status:
    authenticator.logout('Logout', 'main')
    if username == 'jsmith':
        st.write(f'Welcome *{name}*')
        st.title('Application 1')
    elif username == 'rbriggs':
        st.write(f'Welcome *{name}*')
        st.title('Application 2')
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
```

#### Reset Password
```python
if st.session_state["authentication_status"]:
    try:
        if authenticator.reset_password(st.session_state["username"], 'Reset password'):
            st.success('Password modified successfully')
    except Exception as e:
        st.error(e)
```

#### New User Registration
```python
try:
    if authenticator.register_user('Register user', preauthorization=False):
        st.success('User registered successfully')
except Exception as e:
    st.error(e)
```

#### Forgot Password
```python
try:
    username_of_forgotten_password, email_of_forgotten_password, new_random_password = authenticator.forgot_password('Forgot password')
    if username_of_forgotten_password:
        st.success('New password to be sent securely')
        # Random password should be transferred to user securely
    else:
        st.error('Username not found')
except Exception as e:
    st.error(e)
```

#### Forgot Username
```python
try:
    username_of_forgotten_username, email_of_forgotten_username = authenticator.forgot_username('Forgot username')
    if username_of_forgotten_username:
        st.success('Username to be sent securely')
        # Username should be transferred to user securely
    else:
        st.error('Email not found')
except Exception as e:
    st.error(e)
```

#### Update user details
```python
if st.session_state["authentication_status"]:
    try:
        if authenticator.update_user_details(st.session_state["username"], 'Update user details'):
            st.success('Entries updated successfully')
    except Exception as e:
        st.error(e)
```

#### Update Config File
After making changes to the user credentials, we need to update the YAML config file
```python
with open('../config.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)
```