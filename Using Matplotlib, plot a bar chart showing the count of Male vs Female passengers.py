import matplotlib.pyplot as plt
import pandas as pd

# Load the Titanic dataset from a CSV file
titanic_data = pd.read_csv('titanic.csv')

# Count the number of male and female   passengers
gender_counts = titanic_data['Sex'].value_counts()
# Plot a bar chart showing the count of male vs female passengers
plt.bar(gender_counts.index, gender_counts.values, color=['blue', 'pink'])
plt.title('Count of Male vs Female Passengers')
plt.xlabel('Gender')
plt.ylabel('Count')
plt.show()                                          