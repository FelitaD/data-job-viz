import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from collections import Counter


from config.definitions import DB_STRING


def load_data():
    engine = create_engine(DB_STRING)
    query = """SELECT * FROM relevant ORDER BY created_at DESC"""
    jobs = pd.read_sql_query(query, engine)
    return jobs


def count_technos(data, nitems):
    stacks = data['stack']
    new_stacks = [stack.strip('{}').split(',') for stack in stacks]
    concatenated_stacks = [item for sublist in new_stacks for item in sublist]
    techno_count = Counter(concatenated_stacks)
    sorted_items = sorted(techno_count.items(), key=lambda x: x[1], reverse=True)
    words = [item[0] for item in sorted_items]
    counts = [item[1] for item in sorted_items]
    return words[:nitems], counts[:nitems]



st.title('Data engineer technologies')

data = load_data()

st.subheader('Raw data')
st.write(data)


nrows = st.slider('Number of technologies', min_value=0, max_value=25, value=15)

words, counts = count_technos(data, nrows)

fig, ax = plt.subplots()
plt.bar(words, counts)
plt.xlabel('Technos')
plt.ylabel('Count')
plt.title('Techno Count Visualization')
plt.xticks(rotation=45, ha='right')

st.pyplot(fig)

