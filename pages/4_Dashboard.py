import streamlit as st
import sqlite3
import plotly.graph_objects as go

# Connect to the SQLite database
conn = sqlite3.connect('mental_health.db')
cursor = conn.cursor()

# Create the mental_health table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS mental_health (
        id INTEGER PRIMARY KEY,
        date DATE,
        feelings TEXT,
        serenity INTEGER,
        sleep INTEGER,
        productivity INTEGER,
        enjoyment INTEGER
    )
''')

# Function to insert data into the database
def insert_mental_health_data(date, feelings, serenity, sleep, productivity, enjoyment):
    cursor.execute('''
        INSERT INTO mental_health (date, feelings, serenity, sleep, productivity, enjoyment)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (date, feelings, serenity, sleep, productivity, enjoyment))
    conn.commit()

# Streamlit UI
st.title("Mental Health Tracker and Score Meter")

# Input fields for mental health details
date = st.date_input("Date", value=None, key='date_input')
feelings = st.slider("Feelings(1-10)", 1, 10, 5)
serenity = st.slider("Serenity (1-10)", 1, 10, 5)
sleep = st.slider("Sleep quality (1-10)", 1, 10, 5)
productivity = st.slider("Productivity (1-10)", 1, 10, 5)
enjoyment = st.slider("Enjoyment (1-10)", 1, 10, 5)

# Button to submit the data
if st.button("Submit"):
    if feelings:
        insert_mental_health_data(date, feelings, serenity, sleep, productivity, enjoyment)
        st.success("Data submitted successfully!")

# Function to calculate the mental health score
def calculate_mental_health_score():
    cursor.execute("SELECT serenity, sleep, productivity, enjoyment FROM mental_health")
    data = cursor.fetchall()
    if not data:
        return None

    mental_health_score = sum(data[-1]) / 4  # Simple average score

    return mental_health_score

# Calculate the mental health score
mental_health_score = calculate_mental_health_score()

if mental_health_score is not None:
    st.write("Current Mental Health Score:", mental_health_score)

    # Create a gauge chart using Plotly
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=mental_health_score,
        title="Mental Health Score",
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={'axis': {'range': [0, 10]},
               'bar': {'color': "lightblue"},
               'steps': [
                   {'range': [0, 3], 'color': "red"},
                   {'range': [3, 7], 'color': "yellow"},
                   {'range': [7, 10], 'color': "green"}]
               }
    ))

    st.plotly_chart(fig)
else:
    st.warning("No data available. Please enter data first.")

# Close the database connection when the app is done
conn.close()

import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Connect to the SQLite database
conn = sqlite3.connect('mental_health.db')
cursor = conn.cursor()

# Streamlit UI
st.title("Mental Health Data Visualization")

# Function to retrieve data from the database
def retrieve_mental_health_data():
    cursor.execute("SELECT date, serenity, sleep, productivity, enjoyment FROM mental_health")
    data = cursor.fetchall()
    if not data:
        return None

    df = pd.DataFrame(data, columns=['Date', 'Serenity', 'Sleep', 'Productivity', 'Enjoyment'])
    df['Date'] = pd.to_datetime(df['Date'])
    return df

# Function to delete all data from the database
def delete_all_data():
    cursor.execute("DELETE FROM mental_health")
    conn.commit()
    st.success("All data deleted successfully!")

# Retrieve and display the mental health data
mental_health_data = retrieve_mental_health_data()

if mental_health_data is not None:
    st.write("Mental Health Data:")
    st.dataframe(mental_health_data)

    # Create a line chart for all attributes
    fig1 = px.line(mental_health_data, x='Date', y=['Serenity', 'Sleep', 'Productivity', 'Enjoyment'],
                   title="Mental Health Attributes Over Time")
    st.write("Line Plot for Mental Health Attributes:")
    st.plotly_chart(fig1)

    # Function to calculate the mental health score
    def calculate_mental_health_score(data):
        data['Mental Health Score'] = data[['Serenity', 'Sleep', 'Productivity', 'Enjoyment']].mean(axis=1)
        return data

    mental_health_data = calculate_mental_health_score(mental_health_data)

    # Create a line chart for the mental health score
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=mental_health_data['Date'], y=mental_health_data['Mental Health Score'],
                             mode='lines+markers', name='Mental Health Score', line=dict(color='blue')))
    fig2.update_layout(title="Mental Health Score Over Time", xaxis_title="Date", yaxis_title="Mental Health Score")
    st.write("Line Plot for Mental Health Score:")
    st.plotly_chart(fig2)

else:
    st.warning("No data available. Please enter data first.")

# Button to delete all data
if st.button("Delete All Data"):
    delete_all_data()

# Close the database connection when the app is done
conn.close()

#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
#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


import streamlit as st
import sqlite3
import openai

# Set your OpenAI GPT-3 API key here
openai.api_key = "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"

# Connect to the SQLite database
conn = sqlite3.connect('mental_health.db')
cursor = conn.cursor()

# Streamlit UI
st.title("Mental Health Guidelines")

# Function to retrieve data from the database
def retrieve_mental_health_data():
    cursor.execute("SELECT date, serenity, sleep, productivity, enjoyment FROM mental_health")
    data = cursor.fetchall()
    if not data:
        return None

    return data

# Retrieve mental health data from the database
mental_health_data = retrieve_mental_health_data()

# ChatGPT function to generate response based on user input and mental health data
def generate_response(input_text):
    input_text = f"User: {input_text}\n"
    mental_health_data_str = "\n".join([f"{entry[0]} - Serenity: {entry[1]}, Sleep: {entry[2]}, Productivity: {entry[3]}, Enjoyment: {entry[4]}" for entry in mental_health_data])
    prompt = f"{input_text}Mental Health Data:\n{mental_health_data_str}\nChatGPT:"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )

    return response.choices[0].text.strip()

# User input text box
user_input = st.text_input("You:", "")

# Generate ChatGPT response when the user clicks the "Send" button
if st.button("Send"):
    if user_input:
        chatbot_response = generate_response(user_input)
        st.text_area("ChatGPT:", value=chatbot_response)

# Close the database connection when the app is done
conn.close()