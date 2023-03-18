import sys
sys.path.append('/apdcephfs/share_1290939/chenyangqi/video_editing')
from tqdm import tqdm
from glob import glob
import imageio
from PIL import Image
import numpy as np
import cv2
import os
from video_diffusion.common.image_util import save_gif_mp4_folder_type

def test_load_save(video_source):

    # You need to install the program FFMPEG and tell it where it is installed
    # os.environ['IMAGEIO_FFMPEG_EXE'] = '/usr/bin/ffmpeg'

    # video_source = '/apdcephfs/share_1290939/chenyangqi/video_editing/data/wild_video/space_shuttle.mp4'


    reader = imageio.get_reader(video_source)
    fps = reader.get_meta_data()['fps']


    for i, im in enumerate(reader):
        # use :05d to add zero, no space before the 05d
        cv2.imwrite(os.path.join(os.path.dirname(video_source), f"{i:05d}.jpg"), im[:, :, ::-1])

def crop_resize_frame(frame):
    h_f,w_f,c_f = frame.shape
    print(f'{h_f}X{w_f}X{c_f}')
    if h_f > 512:
        crop_frame = frame[h_f-512: h_f , w_f-512:w_f, :]
    else:
        crop_frame = frame
    # crop_frame = cv2.resize(crop_frame, (512, 512),interpolation=cv2.INTER_CUBIC)
    crop_frame = cv2.resize(crop_frame, (256, 256),interpolation=cv2.INTER_CUBIC)
    return crop_frame


def concat_a_folder(video_folder = '/apdcephfs/share_1290939/chenyangqi/video_editing/data/homepage_0316/style/1_surf_ukiyo', 
                    save_folder=None,
                    one_by_one_result=False):
    if save_folder is None:
        save_folder = video_folder
    print(video_folder+'/*.mp4')
    video_path_list = sorted(glob(video_folder+'/*.mp4'))
    # test_load_save()
    print(video_path_list)
    reader_list = [imageio.get_reader(video_source) for video_source in video_path_list ]
    
    image_frame_by_video_mat = []
    for reader in reader_list:
        image_frame_list = []
        for i, im in enumerate(reader):
            # use :05d to add zero, no space before the 05d
            # cv2.imwrite(os.path.join(os.path.dirname(video_source), f"{i:05d}.jpg"), im[:, :, ::-1])
            image_frame_list.append(crop_resize_frame(im))
            if i == 7: break
        if i == 6: image_frame_list.append(crop_resize_frame(im))
            
        image_frame_by_video_mat.append(image_frame_list)
    

    if not one_by_one_result:
        writer_edit_list = []
        
        for index in range(len(image_frame_by_video_mat[0])):
            concat_index = np.concatenate([image_frame_list[index] for image_frame_list in image_frame_by_video_mat], axis=1)
            # cv2.imwrite(f'{index:05d}.png',concat_index[:, :, ::-1])
            # breakpoint()
            print(concat_index.shape)
            writer_edit_list.append(concat_index)
        # writer_edit.close()
        os.makedirs(os.path.dirname(save_folder), exist_ok=True)
        save_gif_mp4_folder_type(writer_edit_list, "%s_concat_result.gif" % (save_folder), save_gif=True)
    else:
        
        
        for target_index in range(1, len(image_frame_by_video_mat)):
            writer_edit_list = []
            for index in range(len(image_frame_by_video_mat[0])):
                concat_index = np.concatenate([image_frame_by_video_mat[0][index], image_frame_by_video_mat[target_index][index]], axis=1)
                # cv2.imwrite(f'{index:05d}.png',concat_index[:, :, ::-1])
                # breakpoint()
                print(concat_index.shape)
                writer_edit_list.append(concat_index)
            # writer_edit.close()
            os.makedirs(os.path.dirname(save_folder), exist_ok=True)
            save_gif_mp4_folder_type(writer_edit_list, f"{save_folder}_{target_index:02d}_concat_result.gif", save_gif=True)
    return writer_edit_list

if __name__ == '__main__':
    style_folder = '/apdcephfs/share_1290939/chenyangqi/video_editing/data/homepage_0316/baseline'
    # folder_list = ['/apdcephfs/share_1290939/chenyangqi/video_editing/data/homepage_0316/style/3_sunflower_vangogh']
    # style_folder = '/apdcephfs/share_1290939/chenyangqi/video_editing/data/homepage_0316/shape'
    # style_folder = '/apdcephfs/share_1290939/chenyangqi/video_editing/data/homepage_0316/attri'
    # style_folder = '/apdcephfs/share_1290939/chenyangqi/video_editing/data/homepage_0316/style'
    # style_folder = '/apdcephfs/share_1290939/chenyangqi/video_editing/data/homepage_0316/shape'
    # folder_list = ['/apdcephfs/share_1290939/chenyangqi/video_editing/data/homepage_0316/attri/16_sq_eat']
    one_by_one_result = True

    folder_list = sorted(glob(style_folder+'/*'))
    for f in folder_list:
        concat_a_folder(f, save_folder=style_folder+'_concat256'+f'/{os.path.basename(f)}', one_by_one_result=one_by_one_result)