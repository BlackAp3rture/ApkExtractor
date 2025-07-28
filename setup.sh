#!/bin/sh
#test
# Upgrade PIP
pip install --upgrade pip
pip2 install --upgrade pip

# Install requirements
pip install -r requirements
pip2 install -r requirements

brew install libusb

# Download and build apktool
wget https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.2.3.jar
mv apktool_2.2.3.jar apktool.jar
chmod +x apktool.jar

# Download and unzip dex2jar
wget https://bitbucket.org/pxb1988/dex2jar/downloads/dex2jar-2.0.zip
unzip dex2jar-2.0.zip
rm dex2jar-2.0.zip
chmod +x dex2jar-2.0/*
