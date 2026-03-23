elif nav == "Behavior Mapper":
    st.header("🧠 Pro Behavior & Playstyle Engine")
    
    st.markdown("Select your dominant traits to generate a deterministic build blueprint.")
    
    # 1. User Input: Behaviors
    behavior_traits = st.multiselect(
        "Select your dominant playstyle traits (Choose up to 2):",
        [
            "High Aggression (I run out of Ki constantly)", 
            "Ninjutsu Spammer (I prefer ranged items)", 
            "Elementalist (I apply confusion/status effects)", 
            "Tank (I prefer to block or face-tank hits)"
        ]
    )

    # 2. Logic Mapping Matrix
    if st.button("Generate Blueprint"):
        if not behavior_traits:
            st.warning("Please select at least one behavior.")
        
        if "High Aggression (I run out of Ki constantly)" in behavior_traits:
            st.subheader("⚔️ Aggressive Melee Blueprint")
            st.markdown("**Core Stat Needs:** Melee Ki Damage, Active Skill Damage, Active Skill Ki Consumption.")
            st.markdown("**Target Graces (DotW/DotN):** Susano (Versatility) + Ame-no-Uzume.")
            st.markdown("**Search the Database for:** 'Ki Consumption' or 'Damage (Melee)'.")
            
        if "Ninjutsu Spammer (I prefer ranged items)" in behavior_traits:
            st.subheader("🥷 Ninjutsu Blueprint")
            st.markdown("**Core Stat Needs:** Untouched Ninjutsu, Ninjutsu Power, Shuriken & Kunai Damage.")
            st.markdown("**Target Graces/Sets:** Marici's Grace + Flying Kato.")
            st.markdown("**Suggested Guardian Spirit:** Nekomata (for Anima Bonus on Ninjutsu Hit).")
            
        if "Tank (I prefer to block or face-tank hits)" in behavior_traits:
            st.subheader("🛡️ Survival Blueprint")
            st.markdown("**Core Stat Needs:** Damage Taken %, Elemental Damage Taken, Life Recovery (Amrita Absorption).")
            st.markdown("**Target Graces:** Oyamatsumi's Grace + Honda Clan.")
            st.markdown("**System Note:** Ensure your Armor Weight is high enough for 'Toughness AA'.")
            
        st.info("Next steps: Take these 'Target Graces' to the Build Planner tab to slot them into your gear.")
