import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker  # Import ticker per minor locators
from matplotlib.ticker import MaxNLocator  # Import MaxNLocator per impostare x ticks come interi

# Load CSV file
df = pd.read_csv("risposte_questionario_5.csv")

# Specify the columns corresponding to the questions of interest
selected_questions = ["4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17"]

# Custom colors for each Likert scale value
colors = {
    1: '#aa0503',
    2: '#df3d26',
    3: '#DADDDF',
    4: '#0087bb',
    5: '#005383'
}

# Create a DataFrame to hold the counts of each response for each question
counts_df = pd.DataFrame(index=range(1, 6), columns=selected_questions)

# Populate counts_df with the count of each Likert scale value for each question
for question in selected_questions:
    counts_df[question] = df[question].value_counts().reindex(range(1, 6), fill_value=0)

# (Skip normalization step for absolute values)
# counts_df = counts_df.div(counts_df.sum(axis=0), axis=1) * 100

# Plotting the stacked horizontal bar chart
fig, ax = plt.subplots(figsize=(10, len(selected_questions) * 0.25))

# Initialize the bottom position for stacking bars (start at 0 for all questions)
bottom = pd.Series([0] * len(selected_questions), index=selected_questions)

# Plot each Likert scale value with thinner bars, black borders, and adjusted height
for likert_value in range(1, 6):
    ax.barh(
        y=[f'Q{int(i)+1}' for i in selected_questions],  # Label each bar with the question name
        width=counts_df.loc[likert_value],
        left=bottom,
        color=colors[likert_value],
        edgecolor='black',  # Add black borders
        height=0.6,  # Reduce bar height for thinner bars
        label=f'{likert_value}'
    )
    # Update bottom to stack the next bar on top
    bottom += counts_df.loc[likert_value]

# Adjust the x-axis limits based on the maximum sum of responses across all questions
ax.set_xlim(0, counts_df.sum(axis=0).max())

# Set x-axis ticks to integer values
ax.xaxis.set_major_locator(MaxNLocator(integer=True))

# Adding labels and title
ax.set_xlabel('Number of Responses', fontsize=8)  # Updated label for absolute values
ax.set_ylabel('Question ID', fontsize=8)

ax.set_yticklabels(ax.get_yticklabels(), fontsize=8)  # Riduce la dimensione dei y ticks
ax.set_xticklabels(ax.get_xticklabels(), fontsize=8)  # Riduce la dimensione degli x ticks


# Adding grid and sub-grid
ax.grid(True, which='major', axis='x', linestyle='--', color='grey', alpha=0.7)  # Main grid
ax.grid(True, which='minor', axis='x', linestyle=':', color='lightgrey', alpha=0.7)  # Sub-grid

# Enable minor ticks only on the x-axis
ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(2))  # Adjust number of minor ticks as needed

# Adjusting the legend to be horizontal and placed above the plot
ax.legend(bbox_to_anchor=(0.5, 1.02), loc='lower center', ncol=5, fontsize=8)

plt.savefig("likert.pdf", bbox_inches='tight')

# Display the plot
plt.show()