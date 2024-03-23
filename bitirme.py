import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import folium
from geopy.geocoders import Nominatim

# Geolocator oluşturma
geolocator = Nominatim(user_agent="streamlit_app")

st.set_option('deprecation.showPyplotGlobalUse', False)
# Kargo şubeleri, iller ve ilçeleri içeren bir sözlük
cargo_data = pd.read_csv("bolge.csv",header=0,parse_dates=["datedelivery"])

# Ana sayfa
def main():
    st.title("İlgili Ay Tahmin Verileri")
    selected_city, selected_district = get_user_selection()
    if selected_district:
        display_results( selected_city, selected_district)

# Kullanıcı seçimlerini al
def get_user_selection():
    selected_city = st.sidebar.selectbox("İl Seçin", ["İstanbul"])  
    #selected_city = st.sidebar.selectbox("İl Seçin", cargo_data["City"].drop_duplicates().tolist())
    selected_district = st.sidebar.selectbox("İlçe Seçin", cargo_data[cargo_data["City"]==selected_city]["State"].drop_duplicates().tolist())
    return  selected_city, selected_district

# Sonuçları görüntüle
def display_results( selected_city, selected_district):
    current_month = datetime.now().month -1 
    #st.subheader(f"Seçilen İl: {selected_city}, Seçilen İlçe: {selected_district}")
    df_filter = cargo_data[(cargo_data["City"]==selected_city) & (cargo_data["State"]==selected_district)]
    df = df_filter[["NumberOfCargo","datedelivery"]]
    df=df[df["datedelivery"].dt.month == current_month]
    df = df.sort_values(by="datedelivery")
    df=df.set_index("datedelivery")
    left_column, right_column = st.columns(2)
    with left_column:
        st.dataframe(df, height=900, width=300)
    with right_column:
        fig, ax = plt.subplots(figsize=(4, 4)) 
        ax.plot(df)
        st.pyplot(fig)
    
    location = geolocator.geocode(selected_district)
    if location:
        selected_lat, selected_lon = location.latitude, location.longitude
    else:
        st.error("Koordinatlar bulunamadı")

    # Harita oluşturma
    data = pd.DataFrame({
    'lat': [selected_lat],
    'lon': [selected_lon]
    })

    st.map(data)
if __name__ == "__main__":
    main()
