import pandas as pd

# Sample data
# data = [
#     ('John', 25),
#     ('Jane', 30),
#     ('Bob', 22),
# ]
data = []
id = "1"
num = "saf"
data.append((id, num, ""))
data.append((id, num, ""))
# Create a DataFrame
df = pd.DataFrame(data, columns=['Name', 'Age', 'A'])

# Specify the file path
csv_file_path = 'output.csv'

# Write to CSV without headers
df.to_csv(csv_file_path, header=False, index=False)

print(f"Data has been written to {csv_file_path} without headers.")
