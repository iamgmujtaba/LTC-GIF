from keras.models import load_model
import numpy as np

import os
import time
import csv
import operator 

from utils.UCFdata import UCFDataSet
from utils.lib_createDir import prepare_walter_dirs
from utils.lib_hls import get_container_csv, download_containers, natural_keys
from utils.lib_hls import get_seg_file, get_vidSeg_timestamp, remove_dublicate_row_csv, download_segments
from utils.lib_thumbnails import extract_thumbnails, process_image
from modules.SGDW import SGDW

from config import parse_opts

ucf_data = UCFDataSet()

config = parse_opts()
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]= config.device

model_path ='./output/033-1.07.hdf5'
model = load_model(model_path, custom_objects={'SGDW': SGDW})

soccer_video_list = ['ABC Video']            
baseket_video_list = []
boxing_video_list = []
baseball_video_list = []
cricket_video_list = []
tennis_video_list = []

####################################################################
def event_recognition(thumbnail_dir, detect_thumb_csv):
    threshold = 0.80
    scenes_data = []
    
    for fileName in os.listdir(thumbnail_dir):
        # Turn the image into an array.
        img_fileName = os.path.join(thumbnail_dir,fileName)
        image_arr = process_image(img_fileName, (config.spatial_size, config.spatial_size, 3))
        image_arr = np.expand_dims(image_arr, axis=0)
          
        # Predict.
        predictions = model.predict([image_arr])
        # Show how much we think it's each one.
        label_predictions = {}
        for i, label in enumerate(ucf_data.classes):
            label_predictions[label] = predictions[0][i]

        sorted_lps = sorted(label_predictions.items(), key=operator.itemgetter(1), reverse=True)
        
        for i, class_prediction in enumerate(sorted_lps):
            i += 1
            if float(class_prediction[1]) >= threshold:
                print("{} {}: {:.2f}%".format(img_fileName, class_prediction[0], class_prediction[1] * 100))
                scenes_data.append([img_fileName, class_prediction[0]])
    
    with open(detect_thumb_csv, 'w') as fout:
        writer = csv.writer(fout)
        writer.writerows(sorted(scenes_data, key=natural_keys))

def process_csv(csv_file, process_thumb_path, select_category):
    count = 0
    video_data = []
    with open(csv_file, 'r') as fin:
        reader = csv.reader(fin)
        for row in reader:
            if select_category == 'Soccer':
                if row[1] == 'SoccerJuggling' or row[1] == 'SoccerPenalty':
                    video_data.append([os.path.basename(row[0])])
                    count += 1
            elif select_category == 'Baseketball':
                if row[1] == 'Basketball' or row[1] == 'BasketballDunk':
                    video_data.append([os.path.basename(row[0])])
                    count += 1
            elif select_category == 'Boxing':
                if row[1] == 'BoxingPunchingBag' or row[1] == 'BoxingSpeedBag' or row[1] == 'Punch':
                    video_data.append([os.path.basename(row[0])])
                    count += 1
            elif select_category == 'Baseball':
                if row[1] == 'BaseballPitch':
                    video_data.append([os.path.basename(row[0])])
                    count += 1
            elif select_category == 'Cricket':
                if row[1] == 'CricketBowling'or row[1] == 'CricketShot':
                    video_data.append([os.path.basename(row[0])])
                    count += 1
            elif select_category == 'Tennis':
                if row[1] == 'TennisSwing':
                    video_data.append([os.path.basename(row[0])])
                    count += 1
            else:
                print('Error: No category selected')

    with open(process_thumb_path, 'w') as fout:
        writer = csv.writer(fout)
        writer.writerows(sorted(video_data, key=natural_keys))
    
    print('Number of detect thumbnails: {}'.format(count))

def generate_GIF(segments_dest, gif_dest):
    files = get_seg_file(segments_dest)
    for segment_no in files:
        print(os.path.join(segments_dest,segment_no))
        segment = os.path.join(segments_dest,segment_no)
        segment_name = segment_no.split(".")[0]
        
        pal_cmd = ("ffmpeg -y -t 5 -i " + segment + " -vf fps=10,scale=320:-1:flags=lanczos,palettegen " + os.path.join(gif_dest, segment_name)+"_palette.png")
        gif_cmd = ("ffmpeg -y -t 5 -i " + segment + " -i "+ os.path.join(gif_dest, segment_name) +"_palette.png " +" -lavfi \"fps=15,scale=320:-1:flags=lanczos[x];[x][1:v]paletteuse\" " + os.path.join(gif_dest, segment_name) +"_first.gif")

        print(pal_cmd)
        print(gif_cmd)

        os.system(pal_cmd)
        os.system(gif_cmd)
    

def main(select_category):
    count = 1
    local_walter_dir = './TestResults/'

    if select_category == 'Soccer':
        video_list = soccer_video_list
    elif select_category == 'Baseketball':
        video_list = baseket_video_list
    elif select_category == 'Boxing':
        video_list = boxing_video_list
    elif select_category == 'Baseball':
        video_list = baseball_video_list
    elif select_category == 'Cricket':
        video_list = cricket_video_list
    elif select_category == 'Tennis':
        video_list = tennis_video_list
    else:
        print('Error 404: No category found')


    for selected_video in video_list:
        print('-'*80)
        print('{}: {}'.format(count, selected_video))
        count += 1

        #Create director for movie
        main_video_dir, vid_container_dir, vid_thumbnail_dir, vid_segment_dir = prepare_walter_dirs(local_walter_dir, selected_video)

        containers_csv_url = os.path.join(config.walter_ip, selected_video, 'container_list.csv')   
        containers_url = os.path.join(config.walter_ip,selected_video,'thumbnails/')
        seg_movie_url = os.path.join(config.walter_ip, selected_video, 'segments')

        print(containers_csv_url)
        print(containers_url)
        
        detect_thumb_csv = os.path.join(main_video_dir, 'detect_thumbs.csv')
        process_thumb_csv = os.path.join(main_video_dir, select_category+'_thumbs.csv')
        segmnets_csv = os.path.join(main_video_dir, select_category+'_segment.csv')

        gif_video_path = os.path.join(main_video_dir, 'gif')

        text_file = open(os.path.join(main_video_dir,'process.txt'), "w")
        text_file.write(main_video_dir)
        text_file.write('\n')

        #--------------------------------------------------
        start1 = time.time()
        get_container_csv(containers_csv_url, main_video_dir)
        download_containers(containers_url, main_video_dir, vid_container_dir)
        end1 = time.time()
        text_file.write('Download TCs seconds: ' + str(round(end1 - start1, 2)) + '----- mintues: ' + str(round (end1 - start1, 2)/60) )
        text_file.write('\n')
        # ==================================================
        

        # ==================================================
        start2 = time.time()
        extract_thumbnails(vid_container_dir, vid_thumbnail_dir)
        end2 = time.time()
        text_file.write('Extract thumbnail seconds: ' + str(round(end2 - start2, 2)) + '----- mintues: ' + str(round (end2 - start2, 2)/60) )
        text_file.write('\n')
        # ==================================================


        # ==================================================
        start3 = time.time()
        event_recognition(vid_thumbnail_dir, detect_thumb_csv)
        end3 = time.time()
        text_file.write('Event recognize seconds: ' + str(round(end3 - start3, 2)) + '----- mintues: ' + str(round (end3 - start3, 2)/60) )
        text_file.write('\n')
        # ==================================================

        try:
            os.makedirs(gif_video_path)
        except OSError:
            pass

        # ==================================================
        start4 = time.time()        
        process_csv(detect_thumb_csv, process_thumb_csv, select_category)
        get_vidSeg_timestamp(segmnets_csv, process_thumb_csv)
        remove_dublicate_row_csv(segmnets_csv)
        download_segments(seg_movie_url, segmnets_csv, vid_segment_dir)
        end4 = time.time()
        # ==================================================

        # ==================================================
        start5 = time.time()
        generate_GIF(vid_segment_dir, gif_video_path)
        end5 = time.time()
        # ==================================================

        text_file.write('Get timestamp: seconds: ' + str(round(end4 - start4, 2)) + '----- mintues: ' + str(round (end4 - start4, 2)/60))
        text_file.write('\n')
        text_file.write('Generate GIF sec: ' + str(round(end5 - start5, 2)) + ' mint: ' + str(round (end5 - start5, 2)/60))
        text_file.write('\n')
        text_file.close()

        
if __name__ == "__main__":
    main(select_category = config.category)
