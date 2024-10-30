import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator

# Load CSV file
df = pd.read_csv("risposte_questionario_5_short.csv")

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

# Define labels for Likert scale values
likert_labels = {
    1: 'Strongly Disagree',
    2: 'Disagree',
    3: 'Neutral',
    4: 'Agree',
    5: 'Strongly Agree'
}

# Plotting the stacked horizontal bar chart
fig, ax = plt.subplots(figsize=(2.5 * 3, len(selected_questions) * 0.10 * 3))

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
        height=0.4,  # Reduce bar height for thinner bars
        label=likert_labels[likert_value]  # Use custom label for the legend
    )
    # Update bottom to stack the next bar on top
    bottom += counts_df.loc[likert_value]

# Adjust the x-axis limits based on the maximum sum of responses across all questions
ax.set_xlim(0, counts_df.sum(axis=0).max())

# Set x-axis ticks to show every 2 units
ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True, nbins=10))  # Automatically adjust number of bins
ax.set_xticks(range(0, 20, 2))  # Set major ticks every 2 units

# Add minor ticks every 1 unit
ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))

# Reduce the size of y ticks and x ticks
ax.tick_params(axis='y', labelsize=9)
ax.tick_params(axis='x', labelsize=9)

# Invert the order of questions on the y-axis
ax.invert_yaxis()

# Adding grid and sub-grid
ax.grid(True, which='major', axis='x', linestyle='--', color='grey', alpha=0.7)  # Main grid
ax.grid(True, which='minor', axis='x', linestyle=':', color='grey', alpha=0.5)  # Minor grid

# Adding labels and title
ax.set_xlabel('Number of Responses', fontsize=9)  # Updated label for absolute values
ax.set_ylabel('Question ID', fontsize=9)

plt.savefig("likert.pdf", bbox_inches='tight')

# Display the plot
plt.show()