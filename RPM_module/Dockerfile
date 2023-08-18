From centos:7

#copy require files over
COPY rpm_download.py /root/rpm_download.py
COPY input.txt /root/input.txt

WORKDIR /root
#update image
RUN yum -y update && yum install -y python3

