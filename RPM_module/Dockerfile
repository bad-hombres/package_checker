From centos:7

WORKDIR /root

#update image and isntall python3
RUN yum -y update && yum install -y python3


#run the download script
ENTRYPOINT ["python3", "./rpm_download.py"]