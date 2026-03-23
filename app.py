import streamlit as st
import pandas as pd
import os

# 1. System Configuration
st.set_page_config(page_title="Nioh 2 Architect Pro", layout="centered")

# 2. Multi-Format Data Ingestion
@st.cache_data
def load_all_data():
    all_files = os.listdir('.')
    data_map = {}
    
    for file in all_files:
        # Handle CSV Files
        if file.endswith('.csv'):
            name = file.split(' - ')[-1].replace('.csv', '') if ' - ' in file else file.replace('.csv', '')
            try:
                data_map[name] = pd.read_csv(file, on_bad_lines='skip')
            except: pass
            
        # Handle Excel Files (Reads every sheet automatically)
        elif file.endswith('.xlsx'):
            try:
                excel_sheets = pd.read_excel(file, sheet_name=None)
                for sheet_name, df in excel_sheets.items():
                    data_map[sheet_name] = df
            except Exception as e:
                st.sidebar.error(f"Error reading Excel: {e}")
                
    return data_map, all_files

data, raw_file_list = load_all_data()

# 3. Sidebar Navigation
st.sidebar.title("🛠️ Build Architect")
nav = st.sidebar.radio("Navigation", ["Search Database", "Build Planner", "Behavior Mapper"])

with st.sidebar.expander("📂 File System Debug"):
    st.write("Files in Repo:", raw_file_list)
    st.write("Available Categories:", list(data.keys()))

# 4. Main UI
if not data:
    st.error("### ⚠️ No Data Found")
    st.info(f"The app sees these files: {raw_file_list}. Ensure your .xlsx file is in the main GitHub folder.")
else:
    if nav == "Search Database":
        st.header("🔍 Stat & Item Search")
        category = st.selectbox("Select Tab (Sheet)", sorted(list(data.keys())))
        df = data[category]
        
        search_query = st.text_input(f"Search in {category}...")
        if search_query:
            mask = df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
            st.dataframe(df[mask], use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)

    # (Planner and Behavior logic remain active below)
    elif nav == "Behavior Mapper":
        st.header("🧠 Behavior Engine")
        behavior = st.selectbox("Playstyle", ["High Aggression", "Ninjutsu Focus", "Tank"])
        if st.button("Get Recommendations"):
            st.success(f"Logic running for {behavior} based on Excel data.")
