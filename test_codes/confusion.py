import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

labels = ['LSE', 'LME', 'MBE', 'MSE', 'background']

# custom_matrix = np.array([
#     [0.88, 0.06, 0.00, 0.06, 0.31],  # Predicted LSE
#     [0.03, 0.76, 0.06, 0.12, 0.35],  # Predicted LME
#     [0.00, 0.03, 0.91, 0.04, 0.19],  # Predicted MBE
#     [0.09, 0.12, 0.03, 0.75, 0.15],  # Predicted MSE
#     [0.00, 0.03, 0.00, 0.00, 0.00],  # Predicted background
# ])

custom_matrix = np.array([
    [0.82, 0.00, 0.12, 0.06, 0.00],  # Predicted LSE
    [0.00, 0.82, 0.09, 0.09, 0.00],  # Predicted LME
    [0.04, 0.21, 1.00, 0.08, 0.00],  # Predicted MBE
    [0.33, 0.05, 0.24, 0.67, 0.00],  # Predicted MSE
    [0.00, 0.00, 0.00, 0.00, 0.00],  # Predicted background (optional row)
])

sns.set(font_scale=2.5)

plt.figure(figsize=(10, 8))
ax = sns.heatmap(custom_matrix, annot=True, fmt=".2f", cmap="rocket",
                 xticklabels=labels, yticklabels=labels, cbar_kws={'label': 'Probability'})

# Title and axes
# ax.set_title("Un-augmented Dataset", fontsize=24)
ax.set_title("Augmented Dataset", fontsize=24)
ax.set_xlabel("True", fontsize=22)
ax.set_ylabel("Predicted", fontsize=22)

# Tick label formatting
ax.set_xticklabels(labels, rotation=0, ha='center')
ax.set_yticklabels(labels, rotation=90, va='center')
ax.tick_params(axis='both', which='major', labelsize=18)

# Colorbar font
cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=20)
cbar.set_label('Probability', fontsize=22)

# Layout management
plt.subplots_adjust(left=0.2, right=0.95, top=0.9, bottom=0.2)

plt.show()
