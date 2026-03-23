import streamlit as st
import pandas as pd
import os

# 1. System Configuration
st.set_page_config(page_title="Nioh 2 Architect: Search", layout="centered")

# 2. Advanced Data Ingestion & Merging
@st.cache_data
def load_master_db():
    all_files = os.listdir('.')
    excel_file = next((f for f in all_files if f.endswith('.xlsx')), None)
    if not excel_file: return None

    ignore_list = ["!Notice", "Main Page", "Buff Values"]
    try:
        all_sheets = pd.read_excel(excel_file, sheet_name=None)
        master_frames = []
        for name, df in all_sheets.items():
            if name not in ignore_list:
                df['Source'] = name  # Label where the item came from
                master_frames.append(df)
        
        # Merge all data; numerical columns (Weight, Toughness) are preserved
        return pd.concat(master_frames, ignore_index=True, sort=False)
    except: return None

master_db = load_master_db()

# 3. Sidebar: Property Filters (The "Pro" Controls)
st.sidebar.title("⚙️ Property Filters")
st.sidebar.info("Narrow down your search by specific gear properties.")

min_weight, max_weight = 0.0, 100.0
min_tough, max_tough = 0, 500

with st.sidebar.expander("⚖️ Weight & Toughness"):
    if master_db is not None:
        # Weight Slider (if Weight column exists)
        if 'Weight' in master_db.columns:
            w_min = float(master_db['Weight'].min())
            w_max = float(master_db['Weight'].max())
            weight_range = st.slider("Weight Range", w_min, w_max, (w_min, w_max))
        else: weight_range = (0.0, 100.0)

        # Toughness Slider (if Toughness column exists)
        if 'Toughness' in master_db.columns:
            t_min = int(master_db['Toughness'].min())
            t_max = int(master_db['Toughness'].max())
            tough_range = st.slider("Toughness Range", t_min, t_max, (t_min, t_max))
        else: tough_range = (0, 1000)

# 4. Main Search Interface
st.title("🥷 Unified Build Search")

if master_db is not None:
    search_query = st.text_input("Search by Name or Stat (e.g., 'Susano', 'Melee', 'Katana')", "")

    # Apply Filters
    filtered_df = master_db.copy()
    
    # Text Filter
    if search_query:
        mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
        filtered_df = filtered_df[mask]

    # Property Filters
    if 'Weight' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Weight'].between(weight_range[0], weight_range[1])]
    if 'Toughness' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Toughness'].between(tough_range[0], tough_range[1])]

    # Results Display
    if not filtered_df.empty:
        st.write(f"Showing {len(filtered_df)} matches:")
        # Drop columns that are entirely empty for this specific search result
        display_df = filtered_df.dropna(axis=1, how='all')
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.warning("No matches found for this combination of keyword and properties.")
else:
    st.error("⚠️ Excel file not found. Check your GitHub repository.")

st.sidebar.markdown("---")
st.sidebar.caption("v3.1 | Property-Aware Search")
