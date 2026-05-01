import io
import zipfile

def extract_nested_zips(zip_data, file_types):
    result = []
    with zipfile.ZipFile(io.BytesIO(zip_data), 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            if file_info.filename.lower().endswith('.zip'):
                nested_zip_data = zip_ref.read(file_info.filename)
                result.extend(extract_nested_zips(nested_zip_data, file_types))
            else:
                file_extension = file_info.filename.lower().split('.')[-1]
                if file_extension in file_types:
                    result.append((file_info.filename, zip_ref.read(file_info.filename)))

    return result


zip_file_path = 'C:\\Users\\coditas\\Downloads\\parcels-db4fe35a-geo-test.zip'
file_types = ['geojson']
# Replace 'your_nested.zip' with the actual path to your top-level zip file
with open(zip_file_path, 'rb') as top_zip_file:
    top_zip_data = top_zip_file.read()
    final_files = extract_nested_zips(top_zip_data, file_types)

for filename, content in final_files:
    print(f"File: {filename}")
    print(f"Content: {content[:100]}...")  # Displaying only the first 100 characters of content
    print("=" * 50)
