import streamlit as st
import pandas as pd

# Kargo şubeleri, iller ve ilçeleri içeren bir sözlük
cargo_data = {
    "Şube 1": {
        "İstanbul": {
            "Beşiktaş": {"Tahmini Kargo": 100, "Tahmini Gelir": 5000},
            "Kadıköy": {"Tahmini Kargo": 150, "Tahmini Gelir": 7000},
            "Şişli": {"Tahmini Kargo": 120, "Tahmini Gelir": 6000}
        },
        "Ankara": {
            "Çankaya": {"Tahmini Kargo": 80, "Tahmini Gelir": 4000},
            "Keçiören": {"Tahmini Kargo": 90, "Tahmini Gelir": 4500},
            "Yenimahalle": {"Tahmini Kargo": 100, "Tahmini Gelir": 4800}
        },
        "İzmir": {
            "Konak": {"Tahmini Kargo": 110, "Tahmini Gelir": 5500},
            "Karşıyaka": {"Tahmini Kargo": 100, "Tahmini Gelir": 5000},
            "Bornova": {"Tahmini Kargo": 120, "Tahmini Gelir": 6000}
        }
    }
}

# Ana sayfa
def main():
    st.title("Kargo Şube ve İl Seçimi")
    selected_branch, selected_city, selected_district = get_user_selection()
    if selected_district:
        display_results(selected_branch, selected_city, selected_district)

# Kullanıcı seçimlerini al
def get_user_selection():
    selected_branch = st.sidebar.selectbox("Kargo Şubesi Seçin", list(cargo_data.keys()))
    selected_city = st.sidebar.selectbox("İl Seçin", list(cargo_data[selected_branch].keys()))
    selected_district = st.sidebar.selectbox("İlçe Seçin", list(cargo_data[selected_branch][selected_city].keys()))
    return selected_branch, selected_city, selected_district

# Sonuçları görüntüle
def display_results(selected_branch, selected_city, selected_district):
    st.subheader(f"Seçilen İl: {selected_city}, Seçilen İlçe: {selected_district}")
    st.subheader("Kargo Şubesi Tahmini Kargoları")
    df = pd.DataFrame(cargo_data[selected_branch][selected_city][selected_district], index=["Tahmini Değerler"])
    st.write(df)

if __name__ == "__main__":
    main()
