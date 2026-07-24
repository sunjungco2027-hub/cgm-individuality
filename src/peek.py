"""quick look at one meal to see what a glucose response looks like."""
import load_data as ld

files = ld.subject_files()
df = ld.load_subject(files[0])
meals = ld.meal_events(df)

m = meals.iloc[0]["Timestamp"]
print("first meal at", m)

# grab a few hours around it
win = df[(df["Timestamp"] >= m) & (df["Timestamp"] <= m + __import__("pandas").Timedelta(hours=4))]
print(win[["Timestamp", "Libre GL"]].head(20))
