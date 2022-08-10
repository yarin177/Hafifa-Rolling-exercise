from azure.storage.blob import BlobClient
from given_functions import is_frame_tagged, generate_metadata
import cv2

connection_string = "DefaultEndpointsProtocol=https;AccountName=hafifaos;AccountKey=GYFMpijXyEmd3IIRPw0DnjH3EhNeUFkSHxtK1i7kiaNdX4vWvf9ijhtE9xGpTZmvPERUygc4N1Elccdf143qWg==;EndpointSuffix=core.windows.net"

def get_frames(video_path):
    frames = []
    vidcap = cv2.VideoCapture(video_path)
    success,image = vidcap.read()

    while success:
        frames.append(image)  
        success,image = vidcap.read()

    return frames

def upload_frames(frames: list):
    blob_folder_name = 'frames'

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