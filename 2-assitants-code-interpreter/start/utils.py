import os


def save_file(data_bytes, file_name):
    """Saves a file to the OpenAI API."""
    # Ensure the `files` directory exists
    if not os.path.exists("files"):
        os.makedirs("files")

    # Write the byte data to the file
    with open(f"files/{file_name}", "wb") as file:
        file.write(data_bytes)

    print(f"File {file_name} has been saved in the 'files' directory.")


def retrieve_annotations(annotation):
    """Retrieves the annotations from a message."""
    file_name = annotation.text.split("/")[-1]
    file_id = annotation.file_path.file_id

    try:
        image_data = client.files.content(file_id=file_id)
        print(file_name)
        file_data = image_data.read()
        print(file_data)
        return file_data, file_name
    except Exception as e:
        print(e)
        return None, None
