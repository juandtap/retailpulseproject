FROM apache/spark:4.1.3-scala2.13-java17-python3-ubuntu

USER root

ADD https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.4.2/hadoop-aws-3.4.2.jar \
    /opt/spark/jars/hadoop-aws-3.4.2.jar

ADD https://repo1.maven.org/maven2/software/amazon/awssdk/bundle/2.29.52/bundle-2.29.52.jar \
    /opt/spark/jars/bundle-2.29.52.jar

RUN chmod 644 \
    /opt/spark/jars/hadoop-aws-3.4.2.jar \
    /opt/spark/jars/bundle-2.29.52.jar

# Python requirements
COPY services/spark-processor/requirements.txt /tmp/requirements.txt

RUN pip install \
    --no-cache-dir \
    -r /tmp/requirements.txt


USER spark