import zipfile
import io

li = []

def nested_unzip(query_output, depth=0, **kwargs):
    # if depth > 3:
    #     print('Unzip level exceeded more than the limit (limit=3)')
    #     return

    with zipfile.ZipFile(query_output) as zip_file:
        file_names = [file_name for file_name in zip_file.namelist() if file_name.endswith(".zip")]
        print('Unzipping level - %s', depth)
        print('List of files - %s', file_names)

        for file_name in file_names:
            with zip_file.open(file_name) as inner_file:
                if file_name.endswith(".zip"):
                    inner_file_data = io.BytesIO(inner_file.read())
                    nested_unzip(inner_file_data, depth + 1)
                else:
                    # Found the innermost file, read the contents of the innermost file
                    inner_file_data = inner_file.read()
                    li.append(inner_file_data)
                    return
    return li


if __name__ == '__main__':
    zip_file_path = 'C:\\Users\\coditas\\Downloads\\20230627-parcels-db4fe35a-geo.zip'

    # Read the contents of the ZIP file into a BytesIO object
    with open(zip_file_path, 'rb') as zip_file:
        zip_data = io.BytesIO(zip_file.read())
    nested_unzip(zip_data)
