import streamlit as st
import pandas as pd
import os

# 1. System Configuration
st.set_page_config(page_title="Nioh 2 Search Engine", layout="centered")

# 2. Unified Data Ingestion
@st.cache_data
def load_master_data():
    all_files = os.listdir('.')
    excel_file = next((f for f in all_files if f.endswith('.xlsx')), None)
    
    if not excel_file:
        return None

    # Sheets to IGNORE (The "Not every sheet" filter)
    ignore_list = ["!Notice", "Main Page", "Buff Values", "Armor WeightToughness"]
    
    try:
        # Load all sheets
        all_sheets = pd.read_excel(excel_file, sheet_name=None)
        master_frames = []
        
        for name, df in all_sheets.items():
            if name not in ignore_list:
                # Add a 'Type' column so we know where the data came from
                df['Source_Category'] = name
                master_frames.append(df)
        
        # Merge everything into one Master List
        master_df = pd.concat(master_frames, ignore_index=True, sort=False)
        return master_df
    except Exception as e:
        st.error(f"Error merging data: {e}")
        return None

master_db = load_master_data()

# 3. Simple UI (No Tabs, Just Search)
st.title("🥷 Nioh 2 Build Search")
st.markdown("Type any Weapon, Grace, or Stat name below.")

if master_db is not None:
    # The Single Search Bar
    search_query = st.text_input("Search for anything...", placeholder="e.g. Susano, Melee Damage, Sword...")

    if search_query:
        # Case-insensitive search across all data
        mask = master_db.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
        results = master_db[mask]

        if not results.empty:
            st.write(f"Found {len(results)} matches:")
            
            # Smart View: Hide columns that are 100% empty for these specific results
            # This prevents the "too many columns" confusion
            clean_results = results.dropna(axis=1, how='all')
            
            # Display results as individual "cards" or a table
            st.dataframe(clean_results, use_container_width=True)
        else:
            st.warning("No matches found. Try a different keyword.")
    else:
        st.info("The database is ready. Enter a search term above to begin.")
else:
    st.error("⚠️ Excel file not found in GitHub. Please ensure your .xlsx file is uploaded.")

# Footer - No clutter
st.sidebar.markdown("---")
st.sidebar.caption("System: Pro Build Engine v3.0")
