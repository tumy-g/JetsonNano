# How to install Mediapipe on jetson nano

# Environment
Ubuntu 18.04 Bionic Beaver 

version:Jetpack 4.6.4  

Date 2023-12-30  

# prepare
## Start fan-control
```
sudo jetson_clocks --fan
```
## Stop fan-control
```
echo 0 | sudo tee /sys/devices/pwm-fan/target_pwm
```

# Increase swap for more swap ram
```
git clone https://github.com/JetsonHacksNano/installSwapfile.git  
cd installSwapfile

./installSwapfile.sh
```

# Setup - pre install include Python and pip
```
sudo apt update
sudo apt-get update
sudo apt-get install python3-pip
sudo pip3 install -U pip testresources setuptools==49.6.0
```

# python libraries for Tensorflow
```
sudo apt-get install libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran
```

# Install more Python libraries
```
sudo pip3 install -U --no-deps numpy==1.19.4 future==0.18.2 mock==3.0.5 keras_preprocessing==1.1.2 keras_applications==1.0.8 gast==0.4.0 protobuf pybind11 cython pkgconfig
```

# Install h5py
```
mkdir ~/data
sudo docker run -it --rm --runtime nvidia -v $HOME/data/:/data/ nvcr.io/nvidia/l4t-base:r32.7.1 /bin/bash
```

```
apt-get update
apt-get install -y python3-pip pkg-config
apt-get install -y libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran
pip3 install -U pip testresources setuptools
ln -s /usr/include/locale.h /usr/include/xlocale.h
pip3 install --verbose 'protobuf<4' 'Cython<3'
pip3 install numpy==1.19.4 pkgconfig==1.5.5
apt-get install -y git
git clone https://github.com/h5py/h5py.git
cd h5py
git checkout 3.1.0
git config user.email "you@example.com"
git config user.name "Your Name"
git cherry-pick 3bf862daa4ebeb2eeaf3a0491e05f5415c1818e4
H5PY_SETUP_REQUIRES=0 pip3 install . --no-deps --no-build-isolation
H5PY_SETUP_REQUIRES=0 python3 setup.py bdist_wheel
cp dist/h5py-3.1.0-cp36-cp36m-linux_aarch64.whl /data/
exit

ls -l ~/data/h5py-3.1.0-cp36-cp36m-linux_aarch64.whl

pip3 install  --no-deps ~.data/h5py ~(please push tab key)
```

# Setting nvidia bootloader
```
cd ~
sudo mv /var/lib/dpkg/info/ /var/lib/dpkg/backup/
sudo mkdir /var/lib/dpkg/info/
sudo apt update
sudo apt -f install
sudo mv /var/lib/dpkg/info/* /var/lib/dpkg/backup/
sudo rm -rf /var/lib/dpkg/info
sudo mv /var/lib/dpkg/backup/ /var/lib/dpkg/info/
sudo apt install nvidia-l4t-bootloader

sudo apt update
sudo apt dist-upgrade
```

# Install opencv
```
sudo apt-get install python3-opencv
```

```
sudo sudo apt-get purge *libopencv*
sudo apt-get update
sudo apt-get install -y build-essential cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
sudo apt-get install -y libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
sudo apt-get install -y python2.7-dev python3.6-dev python-dev python-numpy python3-numpy
sudo apt-get install -y libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libdc1394-22-dev
sudo apt-get install -y libv4l-dev v4l-utils qv4l2 v4l2ucp
sudo apt-get install -y curl

mkdir workspace
cd workspace
curl -L https://github.com/opencv/opencv/archive/4.5.0.zip -o opencv-4.5.0.zip
curl -L https://github.com/opencv/opencv_contrib/archive/4.5.0.zip -o opencv_contrib-4.5.0.zip
unzip opencv-4.5.0.zip
unzip opencv_contrib-4.5.0.zip
cd opencv-4.5.0/

mkdir release
cd release/
cmake -D WITH_CUDA=ON -D WITH_CUDNN=ON -D CUDA_ARCH_BIN="5.3,6.2,7.2" -D CUDA_ARCH_PTX="" -D OPENCV_GENERATE_PKGCONFIG=ON -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-4.5.0/modules -D WITH_GSTREAMER=ON -D WITH_LIBV4L=ON -D BUILD_opencv_python2=ON -D BUILD_opencv_python3=ON -D BUILD_TESTS=OFF -D BUILD_PERF_TESTS=OFF -D BUILD_EXAMPLES=OFF -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local ..
make -j$(nproc)
sudo make install

echo "** Install opencv-"4.5.0" successfully"
```

# Install media pipe from the source code
```
git clone https://github.com/google/mediapipe.git
cd mediapipe
```

# Install more libraries for the media pipe setup
```
sudo apt-get install -y libopencv-core-dev  libopencv-highgui-dev libopencv-calib3d-dev libopencv-features2d-dev libopencv-imgproc-dev libopencv-video-dev
```

# set permissions for the setup script file 
```
sudo chmod 744 setup_opencv.sh
```

# run installation from source code : about 30 minutes
```
./setup_opencv.sh
```

# Last step
```
git clone https://github.com/PINTO0309/mediapipe-bin
cd mediapipe-bin

sudo apt install curl
./v0.8.5/download.sh
unzip v0.8.5.zip -d v0.8.5


## It will take =2,30 hours to build opencv-contrib on jetson nano, so wait you
sudo pip3 install numpy-1.19.4-cp36-none-manylinux2014_aarch64.whl
sudo pip3 install mediapipe-0.8.5_cuda102-cp36-none-linux_aarch64.whl

pip3 install dataclasses
```