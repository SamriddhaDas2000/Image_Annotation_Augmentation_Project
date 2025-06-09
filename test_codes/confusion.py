import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Define your custom class labels
labels = ['LSE', 'LME', 'MBE', 'MSE', 'background']

# Your custom normalized confusion matrix

# custom_matrix = np.array([
#     [0.82, 0.00, 0.12, 0.06, 0.00],  # Predicted LSE
#     [0.00, 0.82, 0.09, 0.09, 0.00],  # Predicted LME
#     [0.04, 0.21, 1.00, 0.08, 0.00],  # Predicted MBE
#     [0.33, 0.05, 0.24, 0.67, 0.00],  # Predicted MSE
#     [0.00, 0.00, 0.00, 0.00, 0.00],  # Predicted background (optional row)
# ])



custom_matrix = np.array([
    [0.88, 0.06, 0.00, 0.06, 0.31],  # Predicted LSE
    [0.03, 0.76, 0.06, 0.12, 0.35],  # Predicted LME
    [0.00, 0.03, 0.91, 0.04, 0.19],  # Predicted MBE
    [0.09, 0.12, 0.03, 0.75, 0.15],  # Predicted MSE
    [0.00, 0.03, 0.00, 0.00, 0.00],  # Predicted background
])

# Set global font scale for seaborn (affects heatmap annotations)
sns.set(font_scale=2.25)  # Increase this value for larger text

# Plotting
plt.figure(figsize=(12, 10))
ax = sns.heatmap(custom_matrix, annot=True, fmt=".2f", cmap="rocket",
                 xticklabels=labels, yticklabels=labels, cbar_kws={'label': 'Probability'})

# Set font sizes manually
ax.set_title("Confusion Matrix for Un-Augmented Dataset Normalized", fontsize=24)
# ax.set_title("Confusion Matrix for Augmented Dataset Normalized", fontsize=24)
ax.set_xlabel("True", fontsize=20)
ax.set_ylabel("Predicted", fontsize=20)
ax.tick_params(axis='both', which='major', labelsize=18)  # For tick labels

# Adjust colorbar label font size
cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=18)
cbar.set_label('Probability', fontsize=20)

plt.tight_layout()
plt.show()
