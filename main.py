from src.loader import DataLoader

loader = DataLoader()

df = loader.merge_sources()

print("\nLoaded Contacts:\n")
print(df.head())
print("\nTotal:", len(df))