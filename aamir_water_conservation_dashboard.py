import streamlit as st
import pandas as pd

# Sample data for demonstration purposes
data = {
    "Date": ["2024-10-01", "2024-10-08", "2024-10-15", "2024-10-22"],
    "Water Usage (gallons)": [50, 45, 30, 25],
    "Conservation Tips": [
        "Fix leaks in faucets and toilets.",
        "Use a broom instead of a hose to clean driveways.",
        "Install water-efficient fixtures.",
        "Limit outdoor watering to early morning."
    ]
}

# Create a DataFrame
usage_data = pd.DataFrame(data)

st.title("Personalized Water Conservation Dashboard")
st.write("Track your water usage and discover ways to save!")

# Input for setting conservation goals
goal = st.number_input("Set your weekly water usage goal (in gallons):", min_value=0, value=30)

# Display current water usage
st.subheader("Current Water Usage")
st.write("Here's a summary of your water usage over the past weeks:")
st.line_chart(usage_data.set_index("Date")["Water Usage (gallons)"])

# Calculate and display progress towards goal
total_usage = usage_data["Water Usage (gallons)"].sum()
st.write(f"Total water used in the past {len(usage_data)} weeks: {total_usage} gallons")
if total_usage > goal:
    st.warning(f"You have exceeded your goal by {total_usage - goal} gallons. Consider more conservation efforts!")
else:
    st.success(f"You are within your goal! You have {goal - total_usage} gallons left to use.")

# Display conservation tips based on usage
st.subheader("Personalized Conservation Tips")
for index, row in usage_data.iterrows():
    st.write(f"**Tip for Week {index + 1}:** {row['Conservation Tips']}")

# Form for submitting questions about water conservation
with st.form(key="conservation_chat"):
    user_prompt = st.text_input("Ask a question about water conservation:")
    submitted = st.form_submit_button("Submit")

    if submitted:
        response = f"You asked: '{user_prompt}'. Here are some general tips: "
        response += "1. Collect rainwater for gardening.\n"
        response += "2. Take shorter showers.\n"
        response += "3. Use mulch in gardens to retain moisture."
        st.write(response)
