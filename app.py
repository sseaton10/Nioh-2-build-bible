import streamlit as st
import pandas as pd
import os

# 1. System Configuration
st.set_page_config(page_title="Nioh 2 Architect", layout="centered")

# 2. Robust Data Ingestion
@st.cache_data
def load_all_data():
    # Look for ANY csv file in the current directory
    all_files = [f for f in os.listdir('.') if f.endswith('.csv')]
    data_map = {}
    
    for file in all_files:
        # Simplify the name for the UI: remove long prefixes and extension
        display_name = file.split(' - ')[-1].replace('.csv', '') if ' - ' in file else file.replace('.csv', '')
        try:
            # We use 'on_bad_lines' to handle messy CSV formatting common in game data
            data_map[display_name] = pd.read_csv(file, on_bad_lines='skip')
        except Exception as e:
            st.sidebar.error(f"Error loading {file}: {e}")
            
    return data_map, all_files

data, raw_file_list = load_all_data()

# 3. Sidebar Navigation & Debug
st.sidebar.title("🛠️ Build Architect")
nav = st.sidebar.radio("Navigation", ["Search Database", "Build Planner", "Behavior Mapper"])

# --- DEBUG SECTION (Check this if files are missing) ---
with st.sidebar.expander("📂 Debug: File System"):
    st.write(f"Total CSVs found: {len(raw_file_list)}")
    st.write("Files detected:", raw_file_list)

# 4. Main Logic Controller
if not data:
    st.error("### ⚠️ No Data Found")
    st.markdown(f"""
    The app is running, but it can't see your CSV files. 
    
    **Detected Files in Root:** `{raw_file_list}`
    
    **How to fix:**
    1. Go to your GitHub Repo.
    2. Ensure your CSV files are on the **main page** (not inside a folder called 'data' or 'files').
    3. Ensure the file extension is exactly `.csv` (lowercase).
    """)
else:
    if nav == "Search Database":
        st.header("🔍 Stat & Item Search")
        category = st.selectbox("Select Category", sorted(list(data.keys())))
        df = data[category]
        
        search_query = st.text_input(f"Search in {category} (e.g., 'Damage')")
        if search_query:
            mask = df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
            st.dataframe(df[mask], use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)

    elif nav == "Build Planner":
        st.header("📝 Build Planner")
        st.info("Select items to view details.")
        # Attempt to find a Melee table regardless of naming
        melee_key = next((k for k in data.keys() if "Melee" in k), None)
        if melee_key:
            melee_choice = st.selectbox("Select Weapon", data[melee_key].iloc[:, 0].unique())
            item_data = data[melee_key][data[melee_key].iloc[:, 0] == melee_choice]
            st.table(item_data)
        else:
            st.warning("No 'Melee' data detected. Check your filenames.")

    elif nav == "Behavior Mapper":
        # (Same behavior logic as before)
        st.header("🧠 Pro Behavior Engine")
        behavior_traits = st.multiselect("Select playstyle traits:", ["High Aggression", "Ninjutsu Spammer", "Tank"])
        if st.button("Generate Blueprint"):
            if "High Aggression" in behavior_traits:
                st.subheader("⚔️ Aggressive Melee Blueprint")
                st.markdown("**Core Stats:** Melee Ki Damage, Active Skill Ki Consumption.")
