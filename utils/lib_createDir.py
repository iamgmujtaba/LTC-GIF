import json as simplejson
import os
import time
import shutil
####################################################################
####################################################################
def print_config(config):
    print('#'*60)
    print('Training configuration:')
    for k,v  in vars(config).items():
        print('  {:>20} {}'.format(k, v))
    print('#'*60)

def write_config(config, json_path):
    with open(json_path, 'w') as f:
        f.write(simplejson.dumps(vars(config), indent=4, sort_keys=True))

def output_subdir(config):
    prefix = time.strftime("%Y_%m_%d_%H%M")
    subdir = "{}_{}_{}".format(prefix, config.dataset, config.model)
    return os.path.join(config.save_dir, subdir)

def prepare_output_dirs(config):
    # Set output directories
    config.save_dir = output_subdir(config)
    config.checkpoint_dir = os.path.join(config.save_dir, 'checkpoints')
    config.log_dir = os.path.join(config.save_dir, 'logs')

    # And create them
    if os.path.exists(config.save_dir):
        # Only occurs when experiment started the same minute
        shutil.rmtree(config.save_dir)

    os.mkdir(config.save_dir)
    os.mkdir(config.checkpoint_dir)
    os.mkdir(config.log_dir)
    return config

####################################################################
####################################################################
# create directory for hls server files to download
def prepare_walter_dirs(vid_server_dir, video_title):
    prefix = time.strftime("%Y_%m_%d")
    subdir = "{}_{}".format(prefix, video_title)
    main_video_dir = os.path.join(vid_server_dir, subdir)

    if os.path.exists(main_video_dir):
        # Only occurs when experiment started the same minute
        shutil.rmtree(main_video_dir)

    vid_container_dir = os.path.join(main_video_dir, 'containers')
    vid_thumbnail_dir = os.path.join(main_video_dir, 'thumbnails')
    vid_segment_dir = os.path.join(main_video_dir, 'segments')
    
    os.mkdir(main_video_dir)
    os.mkdir(vid_container_dir)
    os.mkdir(vid_thumbnail_dir)
    os.mkdir(vid_segment_dir)

    return main_video_dir, vid_container_dir, vid_thumbnail_dir, vid_segment_dir