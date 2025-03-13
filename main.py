import matplotlib.pyplot as plt

# Example for minutes
xticks, labels = format_minutes_xticks()
plt.xticks(xticks, labels=labels, rotation=45)

# Example for weeks
week_labels = sorted(data["week"].unique())  # Ensure weeks are sorted
xticks, labels = format_weeks_xticks(week_labels)
plt.xticks(xticks, labels=labels, rotation=45)

# Example for months
month_labels = sorted(data["month"].unique())  # Ensure months are sorted
xticks, labels = format_months_xticks(month_labels)
plt.xticks(xticks, labels=labels, rotation=45)
