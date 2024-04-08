import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import folium
from geopy.geocoders import Nominatim
import plotly.graph_objects as go

# Geolocator oluşturma
geolocator = Nominatim(user_agent="streamlit_app")

st.set_option('deprecation.showPyplotGlobalUse', False)
# Kargo şubeleri, iller ve ilçeleri içeren bir sözlük
cargo_data = pd.read_csv("https://drive.usercontent.google.com/download?id=1Tc5Dt5oJokSWczVUzzpI8Mtc4vNmdaCu&export=download&authuser=0",header=0,parse_dates=["datedelivery"])

# Ana sayfa
def main():
    st.title("Forecast Data in Current Month")
    selected_city, selected_district = get_user_selection()
    if selected_district:
        display_results( selected_city, selected_district)

# Kullanıcı seçimlerini al
def get_user_selection():
    selected_city = st.sidebar.selectbox("Select City", ["İstanbul"])  
    #selected_city = st.sidebar.selectbox("İl Seçin", cargo_data["City"].drop_duplicates().tolist())
    selected_district = st.sidebar.selectbox("Select District", cargo_data[cargo_data["City"]==selected_city]["State"].drop_duplicates().tolist())
    return  selected_city, selected_district

# Sonuçları görüntüle
def display_results( selected_city, selected_district):
    current_month = datetime.now().month -2 
    current_date = datetime(2024,2,5)
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
        #fig, ax = plt.subplots(figsize=(4, 4)) 
        #ax.plot(df)
        #st.pyplot(fig)
        st.text("The number of suggested vehicle in current month: \n{}".format(round(df["NumberOfCargo"].mean()/20)))
        # Metni ortaya hizala
        #st.markdown('<div style="text-align:center">Bu metin ortaya hizalanmıştır.</div>', unsafe_allow_html=True)
        
        st.text("The type of suggested vehicles in current month: \n{}".format("Small Vehicle: {} \n Big Vehicle: {}".format(round(df["NumberOfCargo"].mean()/20)/3,round(df["NumberOfCargo"].mean()/20)*2/3)))

        

    location = geolocator.geocode(selected_district)
    if location:
        selected_lat, selected_lon = location.latitude, location.longitude
    else:
        st.error("Koordinatlar bulunamadı")

    show_map = st.button("Haritayı Göster")

    if show_map:
        # Harita oluşturma
        data = pd.DataFrame({
            'lat': [i for i in np.random.normal(selected_lat,0.005,df.iloc[4,0])],
            'lon': [i for i in np.random.normal(selected_lon,0.005,df.iloc[4,0])],
            'size': [10 for i in range(df.iloc[4,0])]
        }) 
        
        # Create figure
        fig = go.Figure()

        # Add markers
        for i,item in data.iterrows():
            fig.add_trace(go.Scattermapbox(
                lat=[item['lat']],
                lon=[item['lon']],
                mode='markers',
                marker=dict(
                    size=item['size'],
                    color='blue'
                )
            ))

        # Update layout
        fig.update_layout(
            autosize=True,
            hovermode='closest',
            mapbox=dict(
                style='open-street-map',
                zoom=13,
                center=dict(
                lat=selected_lat,
                lon=selected_lon)
            )
        )

        # Plot
        st.plotly_chart(fig,use_container_width=True)

if __name__ == "__main__":
    main()
