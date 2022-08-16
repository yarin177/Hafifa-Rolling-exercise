from azure.storage.blob import BlobClient
from given_functions import is_frame_tagged, generate_metadata
import cv2
from flask import Flask
from flask import request
import os
from DBHandler import DBHandler
from flasgger import swag_from

connection_string = "DefaultEndpointsProtocol=https;AccountName=hafifaos;AccountKey=GYFMpijXyEmd3IIRPw0DnjH3EhNeUFkSHxtK1i7kiaNdX4vWvf9ijhtE9xGpTZmvPERUygc4N1Elccdf143qWg==;EndpointSuffix=core.windows.net"
app = Flask(__name__)
db = DBHandler()

@app.route('/uploadvideo', methods = ['POST'])
@swag_from('requests.yml')
def upload_video():
    """
    This function takes a video path, split it to frames,
    generates metadata for each frame, updating it in Postgres DB,
    and uploads all the media to Azure storage blob.

    Args:
        video_path(str): A local path for a vide file

    Returns:
        status(str): Sucess/Error
    """

    # Edge cases handling
    content = request.json
    if 'video_path' not in content:
        return "Error: 'video_path' key was not provided", 400

    video_path = content['video_path']
    if not os.path.isfile(video_path):
        return f"Error: file '{video_path}' is not found", 400

    metadatas = []
    frames = get_frames(video_path)
    print('Generating Metadata..')
    head, tail = os.path.split(video_path)
    video_folder_name = tail.split('.')[0]

    for frame in frames:
        metadatas.append((generate_metadata(frame), is_frame_tagged(frame)))

    view_name = tail.split('_')[0]
    os_video_path = f'videos/{video_folder_name}.mp4'
    frame_count = len(frames)
    folder_frame_path = f"frames/{video_folder_name}"

    #Upload to DB
    db.add_video(os_video_path, view_name, frame_count)
    metas_to_frames = db.add_metadatas(metadatas)
    db.add_frames(metas_to_frames,folder_frame_path,os_video_path)

    return 'Success'
    #print('Uploading Frames..')
    #upload_frames(frames, video_folder)
    #print('Uploading Video..')
    #upload_video(video_path)

def get_frames(video_path):
    frames = []
    vidcap = cv2.VideoCapture(video_path)
    success,image = vidcap.read()

    while success:
        frames.append(image)  
        success,image = vidcap.read()

    return frames

def upload_frames(frames: list, video_folder: str):
    blob_folder_name = f'frames/{video_folder}'

    for count, frame in enumerate(frames):
        # convert image to bytes
        is_success, im_buf_arr = cv2.imencode(".png", frame)
        byte_im = im_buf_arr.tobytes()
        # upload frame to the container
        blob = BlobClient.from_connection_string(conn_str=connection_string, container_name="yarin-hafifa", blob_name=f"{blob_folder_name}/{count}.png")
        blob.upload_blob(byte_im)

def upload_video(video_path):
    blob_folder_name = 'videos'
    blob = BlobClient.from_connection_string(conn_str=connection_string, container_name="yarin-hafifa", blob_name=f"{blob_folder_name}/{video_path}")

    with open(video_path, "rb") as data:
        blob.upload_blob(data)


if __name__ == '__main__':
    app.run()