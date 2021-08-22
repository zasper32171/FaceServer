#!/bin/bash

set -e

./nvinstall.sh
source /etc/environment

mkdir temp
TEMP_DIR="`realpath temp`"

# update python modules

sudo apt-get update
sudo apt-get -y install python3-pip python3-tk
sudo -H pip3 install --upgrade pip setuptools
sudo -H pip3 install psutil

# install OpenCV-Python

sudo apt-get -y install libopencv-dev
sudo -H pip3 install opencv-python-headless opencv-contrib-python-headless

# Compile Darknet

cd $TEMP_DIR && git clone https://github.com/pjreddie/darknet && cd darknet
sed -i 's/GPU=0/GPU=1/g' Makefile
sed -i 's/CUDNN=0/CUDNN=1/g' Makefile
sed -i 's/OPENCV=0/OPENCV=1/g' Makefile
sed -i 's/OPENMP=0/OPENMP=1/g' Makefile
sed -i '10s/$/\ \\/' Makefile
sed -i '11i\ \ \ \ \ \ -gencode arch=compute_61,code=[sm_61,compute_61] \\' Makefile
sed -i '12i\ \ \ \ \ \ -gencode arch=compute_70,code=[sm_70,compute_70]' Makefile
make -j4
cp $TEMP_DIR/darknet/libdarknet.so $TEMP_DIR/../lib/darknet

# FaceNet

sudo -H pip3 install tensorflow-gpu==1.14.0 numpy==1.16.2 scikit-learn==0.18.0 scipy==0.16.1

# OpenFace

sudo add-apt-repository -y ppa:janisozaur/cmake-update
sudo apt-get update && sudo apt-get -y install cmake

sudo -H pip3 install dlib==19.17.0

cd $TEMP_DIR && git clone https://github.com/nagadomi/distro ./torch --recursive && cd torch
sed -i '15s/.*/PREFIX=\/usr\/local/' install.sh
bash install-deps && sudo sh -c 'echo 'no' | TORCH_NVCC_FLAGS="-D__CUDA_NO_HALF_OPERATORS__" ./install.sh'

sudo sh -c 'luarocks install nn && luarocks install dpnn && luarocks install image && luarocks install optim && luarocks install csvigo && luarocks install torchx && luarocks install tds'
cd extra/cutorch && sudo sh -c 'TORCH_NVCC_FLAGS="-D__CUDA_NO_HALF_OPERATORS__" luarocks make rocks/cutorch-scm-1.rockspec'
sudo luarocks install cunn

cd $TEMP_DIR && git clone https://github.com/soumith/cudnn.torch.git -b R7 && cd cudnn.torch
sudo luarocks make cudnn-scm-1.rockspec

sudo -H sh -c "TORCH_INSTALL=/usr/local pip3 install lutorpy==1.3.7"

# cleanup

cd $TEMP_DIR/..
sudo rm -rf $TEMP_DIR

