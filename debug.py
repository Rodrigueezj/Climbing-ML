import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plot_hold_matrix(matrix, title="Hold Matrix"):
    """
    Visualizes an 18x11 climbing hold matrix as a MoonBoard-style grid.
    
    Values:
    - 0 → black (no hold)
    - 1 → green (hold present)

    Parameters:
    - matrix: numpy array of shape (18, 11), binary matrix representing holds.
    - title: title for the plot (default is "Hold Matrix").
    """
    
    fig, ax = plt.subplots(figsize=(6, 9))
    for i in range(matrix.shape[0]):  # filas
        for j in range(matrix.shape[1]):  # columnas
            color = "green" if matrix[i, j] == 1 else "black"
            rect = plt.Rectangle((j, 17 - i), 1, 1, facecolor=color)
            ax.add_patch(rect)

    ax.set_xlim(0, 11)
    ax.set_ylim(0, 18)
    ax.set_xticks(np.arange(0, 11))
    ax.set_yticks(np.arange(0, 18))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_title(title)
    ax.set_aspect('equal')
    ax.grid(True)
    plt.gca().invert_yaxis()
    plt.show()



# loading CSV
df = pd.read_csv("final_data.csv", converters={"matrix": eval})

# Select a random sample
sample = df.sample(1).iloc[0]

# Key information
print("🖼️ Image filename:", sample["filename"])
print("🎯 Grade:", sample["grade"])
print("⭐ Benchmark:", sample["benchmark"])
print("🌟 Stars:", sample["stars"])

matrix_flipped = np.flipud(sample["matrix"])
plot_hold_matrix(matrix_flipped)