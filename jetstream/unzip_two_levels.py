# import zipfile
# import io
# from zipfile import ZipFile
# from io import TextIOWrapper
#
# zip_file_path = 'C:\\Users\\coditas\\Downloads\\20230123-community-info-block-groups-a1897c57-tsv.zip'# Read the contents of the ZIP file into a BytesIO objectwith open(zip_file_path, 'rb') as zip_file:
# zip_data = io.BytesIO(zip_file_path.read())
#
# with ZipFile(zip_data) as zip_file:
#     file_names = [file_name for file_name in zip_file.namelist() if file_name.endswith(".zip")]
#     print(file_names)
#
#     #for each file_name, get the bytes    return ???

import zipfile
import io
import gzip

zip_file_path = 'C:\\Users\\coditas\\Downloads\\20230627-parcels-db4fe35a-geo.zip'

# Read the contents of the ZIP file into a BytesIO object
with open(zip_file_path, 'rb') as zip_file:
    zip_data = io.BytesIO(zip_file.read())

with zipfile.ZipFile(zip_data) as zip_file:
    file_names = [file_name for file_name in zip_file.namelist() if file_name.endswith(".zip")]
    print(file_names)

    for file_name in file_names:
        with zip_file.open(file_name) as inner_zip:
            # Read the inner ZIP file's contents into a BytesIO object
            inner_zip_data = io.BytesIO(inner_zip.read())

            # Now you can work with the inner ZIP file's contents
            with zipfile.ZipFile(inner_zip_data) as inner_zip_file:
                inner_file_names = inner_zip_file.namelist()
                for inner_file_name in inner_file_names:
                    with inner_zip_file.open(inner_file_name) as inner_file:
                        # Read the content of the inner file
                        content = inner_file.read()

                        # Gzip the content
                        gzipped_content = io.BytesIO()
                        with gzip.GzipFile(fileobj=gzipped_content, mode='wb') as gz:
                            gz.write(content)

                        # Process the gzipped content here or save it to a file
                        # For example, you can save the gzipped content to a file
                        with open(f'{inner_file_name}.gz', 'wb') as output_file:
                            output_file.write(gzipped_content.getvalue())

                        print(f'Inner file {inner_file_name} gzipped and saved.')
