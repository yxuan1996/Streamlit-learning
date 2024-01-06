# Streamlit-learning

Demo app based on the tutorial: https://docs.streamlit.io/get-started/tutorials/create-an-app

EDA (Exploratory Data Analysis) app based on https://blog.streamlit.io/building-a-streamlit-and-scikit-learn-app-with-chatgpt/ 

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

