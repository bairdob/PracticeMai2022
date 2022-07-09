FROM centos/python-36-centos7:latest
#RUN yum -y install epel-release; \
#    yum -y install python3; yum clean all;

COPY . /PracticeMai2022
WORKDIR /PracticeMai2022 
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 5000/tcp
CMD ["python3", "app.py"]

