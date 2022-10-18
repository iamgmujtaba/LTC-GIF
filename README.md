# Client-driven Lightweight Method to Generate Artistic Media for Feature-length Sports Videos

This repository contains the original implementation of the paper __[Client-driven Lightweight Method to Generate Artistic Media for Feature-length Sports Videos](https://drive.google.com/file/d/13A1sZuLfhKVT6R1nHHiaBhIpOqacDfCf/view)__, presented in the proceedings of the 19th International Conference on Signal Processing and Multimedia Applications (SIGMAP) 2022, Lisbon, Portugal.

## Abstract
This paper proposes a lightweight methodology to attract users and increase views of videos through personalized artistic media i.e., static thumbnails and animated Graphics Interchange Format (GIF) images. The proposed method analyzes lightweight thumbnail containers (LTC) using computational resources of the client device to recognize personalized events from feature-length sports videos. In addition, instead of processing the entire video, small video segments are used in order to generate artistic media. This makes our approach more computationally efficient compared to existing methods that use the entire video data. Further, the proposed method retrieves and uses thumbnail containers and video segments, which reduces the required transmission bandwidth as well as the amount of locally stored data that are used during artistic media generation. After conducting experiments on the NVIDIA Jetson TX2, the computational complexity of our method was 3.78 times lower than that of the state-of-the-art method. To the best of our knowledge, this is the first technique that uses LTC to generate artistic media while providing lightweight and high-performance services on resource-constrained devices.

## Prerequisite
- Linux or macOS
- Python 3.6
- CPU or NVIDIA GPU + CUDA CuDNN

## Getting Started
### Installation
- Clone this repo:
```bash
git clone https://github.com/iamgmujtaba/aristic-media
cd aristic-media
```
- To create conda environment and install cuda toolkit, run the following command:
```bash
conda create -n armedia cudatoolkit=10.0 cudnn=7.6.0 python=3.6 -y
conda activate armedia
```
- Install [TensorFlow](https://www.tensorflow.org/) and Keras and other dependencies
  - For pip users, please type the command 
```bash
pip install -r requirements.txt
```

## Preparing the data
1. Create train and test folders
```bash
cd data && mkdir train && mkdir test
```

2. Download the dataset from UCF into the data folder:
```bash
wget wget https://www.crcv.ucf.edu/data/UCF101/UCF101.rar --no-check-certificate
```

3. Extract UCF101.rar file in the data folder
```bash
unrar e UCF101.rar
```

4.  Run the scripts in the data folder to move the videos to the appropriate folders
```bash
python 1_move_files_ucf101.py 
```

5. Run the scripts in the data folder to extract video frames in the train/test folders and make the CSV file. The CSV file will be used in the rest of the code references
```bash
python 2_extract_files_ucf101.py
```

- Note: You need FFmpeg installed to extract frames from videos. 

## Train and evaluate
To train the model, run the following command.

```bash
python train.py --dataset_path /path/to/UCF101 --model_name xception --batch_size 32 --epochs 100 --learning_rate 0.001 --num_classes 101 --save_model_path /path/to/save/model
```
Check [config.py](config.py) for the list of all the parameters.

- In order to evaluate the proposed method, you have to configure [hls-server](https://github.com/iamgmujtaba/hls-server).
- Use [vid2tc](https://github.com/iamgmujtaba/vid2tc) to generate thumbnail contaienrs from videos. For more inforamtion, please refer to the __[paper](https://drive.google.com/file/d/13A1sZuLfhKVT6R1nHHiaBhIpOqacDfCf/view)__.
- Download the pretrained model from [google drive](https://drive.google.com/file/d/1zYHrkIu0GL5xRG0BNYsRtKvejgFPOjRs/view?usp=sharing).
- Place the pretrained model in the [output](output) folder.
- Run the following command to test the proposed method.

```bash
python test.py --genre wt 
```

## Experimental Results

https://user-images.githubusercontent.com/33286377/192426341-42e9caaf-bc57-41e0-9f27-c0703836d6f1.mp4




## Citation
If you use this code for your research, please cite our paper.
```
@inproceedings{mujtabasigmap2022,
    title={Client-driven Lightweight Method to Generate Artistic Media for Feature-length Sports Videos},
    author={Mujtaba, Ghulam and Choi, Jaehyuk and Ryu, Eun-Seok},
    booktitle={19th International Conference on Signal Processing and Multimedia Applications (SIGMAP)},
    pages={102-111},
    year={2022},
    address = {Lisbon, Portugal},
    month = {}}
```

The following paper are also related to this reserach, please cite the articles if you use the code.
```
@article{mujtaba2022,
  title={LTC-SUM: Lightweight Client-driven Personalized Video Summarization Framework Using 2D CNN},
  author={Mujtaba, Ghulam and Malik, Adeel and Ryu, Eun-Seok},
  journal={IEEE Access},
  year={2022},
  publisher={IEEE},
  doi={10.1109/ACCESS.2022.3209275}}

@article{mujtaba2020client,
  title={Client-driven personalized trailer framework using thumbnail containers},
  author={Mujtaba, Ghulam and Ryu, Eun-Seok},
  journal={IEEE Access},
  volume={8},
  pages={60417--60427},
  year={2020},
  publisher={IEEE}
}

@article{mujtaba2021,
  title={Client-driven animated GIF generation framework using an acoustic feature},
  author={Mujtaba, Ghulam and Lee, Sangsoon and Kim, Jaehyoun and Ryu, Eun-Seok},
  journal={Multimedia Tools and Applications},
  year={2021},
  publisher={Springer}}

@inproceedings{mujtaba2021human,
  title={Human character-oriented animated gif generation framework},
  author={Mujtaba, Ghulam and Ryu, Eun-Seok},
  booktitle={2021 Mohammad Ali Jinnah University International Conference on Computing (MAJICC)},
  pages={1--6},
  year={2021},
  organization={IEEE}
}
```
