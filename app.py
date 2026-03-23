import streamlit as st
import pandas as pd
import glob
import os

# 1. System Configuration
st.set_page_config(page_title="Nioh 2 Architect", layout="centered")

# 2. Data Ingestion Engine (Cached for Speed)
@st.cache_data
def load_all_data():
    csv_files = glob.glob("*.csv")
    data_map = {}
    for file in csv_files:
        # Clean display name
        display_name = file.replace("Copy of Nioh 2 Build Bible.xlsx - ", "").replace(".csv", "")
        try:
            data_map[display_name] = pd.read_csv(file)
        except Exception:
            pass
    return data_map

data = load_all_data()

# 3. Sidebar Navigation
st.sidebar.title("🛠️ Build Architect")
nav = st.sidebar.radio("Navigation", ["Search Database", "Build Planner", "Behavior Mapper"])

# 4. Main Logic Controller
if nav == "Search Database":
    st.header("🔍 Stat & Item Search")
    if data:
        category = st.selectbox("Select Category", list(data.keys()))
        df = data[category]
        search_query = st.text_input(f"Search in {category}")
        if search_query:
            mask = df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
            st.dataframe(df[mask], use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)
    else:
        st.error("No CSV files found. Please upload them to your GitHub repository.")

elif nav == "Build Planner":
    st.header("📝 Build Planner")
    st.info("Select items to view details. Comparison logic is currently in development.")
    if "Melee" in data:
        melee_choice = st.selectbox("Melee Weapon 1", data["Melee"]["Name"].unique())
        item_data = data["Melee"][data["Melee"]["Name"] == melee_choice]
        st.write(item_data)
    else:
        st.warning("Melee.csv not found.")

elif nav == "Behavior Mapper":
    st.header("🧠 Pro Behavior Engine")
    st.markdown("Select your dominant traits to generate a deterministic build blueprint.")
    
    behavior_traits = st.multiselect(
        "Select playstyle traits (Choose up to 2):",
        ["High Aggression (Ki Issues)", "Ninjutsu Spammer", "Elementalist", "Tank (Blocking)"]
    )

    if st.button("Generate Blueprint"):
        if "High Aggression (Ki Issues)" in behavior_traits:
            st.subheader("⚔️ Aggressive Melee Blueprint")
            st.markdown("**Core Stats:** Melee Ki Damage, Active Skill Ki Consumption.")
            st.markdown("**Target Graces:** Susano + Ame-no-Uzume.")
            
        if "Ninjutsu Spammer" in behavior_traits:
            st.subheader("🥷 Ninjutsu Blueprint")
            st.markdown("**Core Stats:** Untouched Ninjutsu, Ninjutsu Power.")
            st.markdown("**Target Sets:** Flying Kato + Marici's Grace.")

        if "Tank (Blocking)" in behavior_traits:
            st.subheader("🛡️ Survival Blueprint")
            st.markdown("**Core Stats:** Damage Taken, Life Recovery (Amrita).")
            st.markdown("**Target Graces:** Oyamatsumi.")
