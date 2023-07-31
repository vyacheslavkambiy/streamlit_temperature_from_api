import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

def generate_url(start_date, end_date):
    base_url = "https://archive-api.open-meteo.com/v1/archive"
    url = f"{base_url}?latitude={60.996}&longitude={24.4643}&start_date={start_date}&end_date={end_date}&hourly=temperature_2m"
    return url

def fetch_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            st.error(f"Error: Unable to fetch data. Status Code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
        return None

def main():
    st.title("First I generate URL and then call API with this URL")
    st.write("My latitude and longitude to generate the URL.")

    start_date = st.text_input("Start Date (YYYY-MM-DD):", "2023-07-05")
    #end_date = st.text_input("End Date (YYYY-MM-DD):", "2023-07-05")
    end_date = start_date
    url = generate_url(start_date, end_date)

    #st.write("Generated URL:")
    #st.write(url)

    if st.button("Fetch Data"):
        data = fetch_data(url)
        if data:
            #st.write("Fetched Data:")
            #st.write(data)

            # Extract the hourly temperature data
            hourly_temperatures = data["hourly"]["temperature_2m"]
            time = data["hourly"]["time"]

            # Create a DataFrame to plot the data
            df = pd.DataFrame({"Time": time, "Temperature (°C)": hourly_temperatures})

            # Convert the time column to datetime format
            df["Time"] = pd.to_datetime(df["Time"])

            # Plot the line chart
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(df["Time"], df["Temperature (°C)"], marker="o", linestyle="-", color="b")
            ax.set_xlabel("Time")
            ax.set_ylabel("Temperature (°C)")
            ax.set_title("Hourly Temperature Trend")
            ax.grid(True)

            # Display the chart in Streamlit
            st.pyplot(fig)

if __name__ == "__main__":
    main()