import streamlit as st
import pandas as pd

st.title("🧭 Pathfinder Career Mapping")

st.write("""
### Welcome to Pathfinder Career Mapping!
This app provides tools to explore and match your interests and values with potential career paths. 
You can navigate through the app using the sidebar:
- **Occupation Matching Tool**: Select your interests and values to match with potential occupations.
- **Occupation Profiles**: Search and explore detailed profiles of various occupations.

Simply follow the prompts in each section and enjoy exploring your career possibilities!
""")

# RIASEC Occupation Matching and Work Values Alignment Function
def matching_tool():
    st.title("🧩 Occupation Matching Tool")

    # User input for interests (RIASEC)
    st.subheader("RIASEC Interests")
    realistic_interest = st.checkbox("Realistic (e.g., Build, Repair, Work with hands)")
    investigative_interest = st.checkbox("Investigative (e.g., Research, Analyze, Investigate)")
    artistic_interest = st.checkbox("Artistic (e.g., Create, Design, Express)")
    social_interest = st.checkbox("Social (e.g., Help, Teach, Counsel)")
    enterprising_interest = st.checkbox("Enterprising (e.g., Lead, Manage, Persuade)")
    conventional_interest = st.checkbox("Conventional (e.g., Organize, Calculate, Detail-oriented)")

    selected_riasec_interests = []
    if realistic_interest:
        selected_riasec_interests.append('Realistic')
    if investigative_interest:
        selected_riasec_interests.append('Investigative')
    if artistic_interest:
        selected_riasec_interests.append('Artistic')
    if social_interest:
        selected_riasec_interests.append('Social')
    if enterprising_interest:
        selected_riasec_interests.append('Enterprising')
    if conventional_interest:
        selected_riasec_interests.append('Conventional')

    # User input for work values
    st.subheader("Work Values")
    achievement_value = st.checkbox("Achievement (Success, Accomplishments)")
    working_conditions_value = st.checkbox("Working Conditions (Environment, Safety)")
    recognition_value = st.checkbox("Recognition (Respect, Awards)")
    relationships_value = st.checkbox("Relationships (Teamwork, Collaboration)")
    support_value = st.checkbox("Support (Guidance, Mentoring)")

    selected_work_values = []
    if achievement_value:
        selected_work_values.append('Achievement')
    if working_conditions_value:
        selected_work_values.append('Working Conditions')
    if recognition_value:
        selected_work_values.append('Recognition')
    if relationships_value:
        selected_work_values.append('Relationships')
    if support_value:
        selected_work_values.append('Support')

    # Number of occupations to display
    top_n = st.select_slider("Select the number of top matching occupations to display:", options=range(1, 21), value=5)

    # Finding matching occupations based on selected interests and work values
    if st.button("Find Matching Occupations"):
        riasec_matched_occupations = work_values_matched_occupations = []

        # RIASEC matching logic if selected
        if selected_riasec_interests:
            riasec_matched_occupations = interests_df[
                (interests_df['Element Name'].isin(selected_riasec_interests)) &
                (interests_df['Data Value'] > 5)
            ]['Title'].unique()

        # Work Values matching logic if selected
        if selected_work_values:
            work_values_matched_occupations = work_values_df[
                (work_values_df['Element Name'].isin(selected_work_values)) &
                (work_values_df['Data Value'] > 5)
            ]['Title'].unique()

        # Combine and intersect the matches
        matched_occupations = list(set(riasec_matched_occupations) | set(work_values_matched_occupations))[:top_n]

        # Displaying the matched occupations with descriptions in tabular form
        st.subheader("Matched Occupations")
        if matched_occupations:
            matched_data = []
            for occupation in matched_occupations:
                description = occupation_data_df[occupation_data_df['Title'] == occupation]['Description'].values[0]
                matched_data.append([occupation, description])

            matched_df = pd.DataFrame(matched_data, columns=['Occupation', 'Description'])
            st.table(matched_df)
        else:
            st.write("No matching occupations found. Please modify your selections.")

# Occupation Profiles Function
def occupation_profiles():
    st.title("🏢 Occupation Profiles")

    # User search for specific occupations
    search_query = st.text_input("Search for an occupation (e.g., Engineer, Doctor):")
    if search_query:
        matched_occupations = occupation_data_df[
            occupation_data_df['Title'].str.contains(search_query, case=False)
        ]['Title'].tolist()
        selected_occupation = st.selectbox("Select an occupation from the list:", matched_occupations)
        if selected_occupation:
            st.header(f"Overview of {selected_occupation}")
            occupation_description = occupation_data_df[occupation_data_df['Title'] == selected_occupation]['Description'].values[0]
            st.write(occupation_description)

# Loading necessary data files
interests_df = pd.read_excel("Interests.xlsx")
work_values_df = pd.read_excel("Work Values.xlsx")
occupation_data_df = pd.read_excel("Occupation Data.xlsx")

# App navigation
st.sidebar.title("🧭 Pathfinder Career Mapping")
section = st.sidebar.radio("Choose a section:", ["🧩 Occupation Matching Tool", "🏢 Occupation Profiles"])

if section == "🧩 Occupation Matching Tool":
    matching_tool()
elif section == "🏢 Occupation Profiles":
    occupation_profiles()
