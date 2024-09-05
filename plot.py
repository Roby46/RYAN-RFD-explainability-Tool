import pandas as pd
import matplotlib.pyplot as plt

# Load CSV file
df = pd.read_csv("risposte_questionario_5.csv")

print(df)

# Specify the columns corresponding to the questions of interest (adjusted for indexing)
selected_questions = [ "4","5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17"] 

# Custom colors for each Likert scale value
colors = {
    1: '#aa0503',
    2: '#df3d26',
    3: '#ACB4BA',
    4: '#0087bb',
    5: '#005383'
}

#aa0503,#df3d26,#5c6f7e,#0087bb,#005383


# Create a DataFrame to hold the counts of each response for each question
counts_df = pd.DataFrame(index=range(1, 6), columns=selected_questions)

# Populate counts_df with the count of each Likert scale value for each question
for question in selected_questions:
    counts_df[question] = df[question].value_counts().reindex(range(1, 7), fill_value=0)

print(counts_df)

# Normalize counts to percentages
counts_df = counts_df.div(counts_df.sum(axis=0), axis=1) * 100

# Plotting the stacked horizontal bar chart
fig, ax = plt.subplots(figsize=(10, len(selected_questions) * 0.5))

# Initialize the bottom position for stacking bars (start at 0 for all questions)
bottom = pd.Series([0] * len(selected_questions), index=selected_questions)

# Plot each Likert scale value
for likert_value in range(1, 6):
    ax.barh(
        y=[f'Q{int(i)+1}' for i in selected_questions],  # Label each bar with the question name
        width=counts_df.loc[likert_value],
        left=bottom,
        color=colors[likert_value],
        label=f'Likert {likert_value}'
    )
    # Update bottom to stack the next bar on top
    bottom += counts_df.loc[likert_value]

# Adding labels and title
ax.set_xlabel('Percentage of Responses')
ax.set_ylabel('Question Number')
ax.set_title('Stacked Horizontal Bar Chart of Selected Questions')

# Adjusting the legend to be horizontal and placed above the plot
ax.legend(title='Likert Scale', bbox_to_anchor=(0.5, 1.05), loc='lower center', ncol=6)

# Display the plot
plt.show()
