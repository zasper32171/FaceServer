sudo apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub

wget http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_10.1.168-1_amd64.deb
sudo apt-get install -y ./cuda-repo-ubuntu1604_10.1.168-1_amd64.deb
sudo apt-get update && sudo apt-get install -y cuda-10-0
rm ./cuda-repo-ubuntu1604_10.1.168-1_amd64.deb

wget http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1604/x86_64/nvidia-machine-learning-repo-ubuntu1604_1.0.0-1_amd64.deb
sudo apt-get install -y ./nvidia-machine-learning-repo-ubuntu1604_1.0.0-1_amd64.deb
sudo apt-get update && sudo apt-get install -y libcudnn7=7.4.1.5-1+cuda10.0 libcudnn7-dev=7.4.1.5-1+cuda10.0
rm ./nvidia-machine-learning-repo-ubuntu1604_1.0.0-1_amd64.deb

sudo apt-get install -y nvinfer-runtime-trt-repo-ubuntu1604-5.0.2-ga-cuda10.0
sudo apt-get update && sudo apt-get install -y libnvinfer-dev=5.0.2-1+cuda10.0 libnvinfer5=5.0.2-1+cuda10.0

sudo sed -i 's/PATH="\/usr\/local\/sbin:\/usr\/local\/bin:\/usr\/sbin:\/usr\/bin:\/sbin:\/bin:\/usr\/games:\/usr\/local\/games"/PATH="\/usr\/local\/sbin:\/usr\/local\/bin:\/usr\/sbin:\/usr\/bin:\/sbin:\/bin:\/usr\/games:\/usr\/local\/games:\/usr\/local\/cuda\/bin"/g' /etc/environment

