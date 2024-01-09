import requests


def upload_files(session_id, file_paths):
    url = f"http://localhost:5000/upload/{session_id}"

    files = [('file', (open(file_path, 'rb')))
             for file_path in file_paths]
    print(files)
    response = requests.post(url, files=files)

    print(response.json())


if __name__ == '__main__':
    # Replace with an actual session ID
    session_id = input("Enter session id: ")
    upload_files(
        session_id, ["sample_input/video.mp4", "sample_input/audio.wav"])
