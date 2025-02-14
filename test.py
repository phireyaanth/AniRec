import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv("animes_updated.csv")  # Replace with the actual file path

# Print the first 3 columns
print(df.head(3))