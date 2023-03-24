FROM python:3.11
ADD Freemuxlet_Pooling.py .
ENV TZ=America/Los_Angeles
RUN ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && dpkg-reconfigure -f noninteractive tzdata
# do not try to install python core libraries
RUN pip3 install pandas openpyxl
CMD [ "python", "./Freemuxlet_Pooling.py" ]

# use cd to change to python file containing directory to build
# to build: docker build -t freemuxlet-pooling .
# to run: docker run -i -t -v /Path/to/reference_files.xlsx:/mnt/mydata freemuxlet-pooling
# docker build --platform linux/amd64 -t freemuxlet-pooling-intel . ##will build for intel compatibility

# to push to a public repository:
    #docker tag freemuxlet-pooling astarzinski/freemuxlet-pooling
    #docker push astarzinski/freemuxlet-pooling