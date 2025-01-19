import kagglehub

# Download latest version
path = kagglehub.dataset_download("vatsalmavani/spotify-dataset")

print("Path to dataset files:", path)