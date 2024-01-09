import requests
import zipfile
import io


def download_zip(session_id):
    url = f"http://localhost:5000/download_zip/{session_id}"
    response = requests.get(url)

    with zipfile.ZipFile(io.BytesIO(response.content), 'r') as zip_ref:
        zip_ref.extractall(f'outputs')
    response = requests.delete(
        f"http://localhost:5000/delete_files/{session_id}")
    print(response.json())


if __name__ == '__main__':
    # Replace with the actual session ID used during upload
    session_id = input("Enter session id: ")
    download_zip(session_id)
