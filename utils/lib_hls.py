import os
import csv
import re
from urllib.request import urlopen
import requests


####################################################################
####################################################################
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)',str(text)) ]

####################################################################
####################################################################
# download csv from walter for specifc movie
def get_container_csv(movie_url, dest_path):
    file_name = movie_url.split('/')[-1]

    u = urlopen(movie_url)
    f = open(os.path.join(dest_path,file_name), 'wb')
    resp = requests.get(movie_url)
    
    file_size = int(resp.headers['content-length'])

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)

####################################################################
# download container images from walter fro the specific movie
def containers_to_download(cont_list_csv, movie_path):
    with open(os.path.join(movie_path,cont_list_csv)) as csvfile:
        readCSV = csv.reader(csvfile)
        for row in readCSV:
            row_count = sum(1 for row in readCSV)
            print("Images to download: %s"%(row_count+1))

def download_containers(movie_thumb_url,movie_path, thumb_dest_dir):
    cont_list_csv = 'container_list.csv'
    containers_to_download(cont_list_csv, movie_path)

    with open(os.path.join(movie_path,cont_list_csv)) as csvfile:
        readCSV = csv.reader(csvfile)
        for row in readCSV:
            try:
                t_url = movie_thumb_url+str(row).strip('[]').strip("'")
                file_name = t_url.split('/')[-1]

                u = urlopen(t_url)
                f = open(os.path.join(thumb_dest_dir,file_name), 'wb')
                resp = requests.get(t_url)
                
                file_size = int(resp.headers['content-length'])
            
                file_size_dl = 0
                block_sz = 8192
                while True:
                    buffer = u.read(block_sz)
                    if not buffer:
                        break

                    file_size_dl += len(buffer)
                    f.write(buffer)
                    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
                    status = status + chr(8)*(len(status)+1)
                f.close()
            except:
                pass
    print("Download complted: ", thumb_dest_dir)

####################################################################
def get_vidSeg_timestamp(segment_csv, detect_thumbs_csv):
    with open(segment_csv, 'w') as f2:
        with open(detect_thumbs_csv) as f:
            reader = csv.reader(f)
            for rows in reader:
                            
                fileName = " ".join(rows)
                tempName = fileName.split("_")
                frameNumber = int(tempName[1])*25+int (tempName[2].split(".")[0])

                segment_no = int(frameNumber/10)
                segment_name = "out"+ '{:02}'.format(segment_no)+".ts"
                
                f2.write(str(segment_name)+"\n")


def download_segments(movie_url, segment_csv, segments_dest):
    f = open(segment_csv, "r+")
    reader = csv.reader(f)
    pre_line = next(reader)
    x = 10
    while(True) and x >0:
        try:
            cur_line = next(reader)
            if pre_line != cur_line:
                
                segment_name = str(pre_line).strip('[]').strip("'")
                #print("downloading segment: ",segment_name)

                seg_url = os.path.join(movie_url, segment_name)
                # movie_url + segment_name
                print('downloading segment: ', seg_url)
                
                u = urlopen(seg_url)
                f = open(os.path.join(segments_dest,segment_name), 'wb')
                resp = requests.get(seg_url)

                file_size = int(resp.headers['content-length'])
                #print ("Downloading: %s Bytes: %s" % (segment_name, file_size))
                
                file_size_dl = 0
                block_sz = 8192
                while True:
                    buffer = u.read(block_sz)
                    if not buffer:
                        break

                    file_size_dl += len(buffer)
                    f.write(buffer)
                    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
                    status = status + chr(8)*(len(status)+1)
            pre_line = cur_line
            x -=1
        except :
            break

def remove_dublicate_row_csv (csv_file):
    count = 0
    with open(csv_file, 'r') as fin:
        lines = fin.readlines()
        lines = [line.strip() for line in lines]
        lines = list(set(lines))
        # lines = sorted(lines)
        lines.sort(key=natural_keys)
        with open(csv_file, 'w') as fout:
            for line in lines:
                fout.write(line + '\n')
                count += 1

    print('Number of detect segments: {}'.format(count))


def get_seg_file(seg_path):
    return [f for f in os.listdir(seg_path) if os.path.isfile(os.path.join(seg_path, f)) and f.endswith('.ts')]
