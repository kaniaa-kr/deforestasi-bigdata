FROM apache/airflow:2.10.5-python3.11

USER root
RUN apt-get update \
 && apt-get install -y --no-install-recommends openjdk-17-jre-headless curl \
 && rm -rf /var/lib/apt/lists/* \
 && ln -s "$(dirname "$(dirname "$(readlink -f "$(which java)")")")" /usr/lib/jvm/java-17
ENV JAVA_HOME=/usr/lib/jvm/java-17

USER airflow
RUN pip install --no-cache-dir \
      "apache-airflow==2.10.5" \
      "pyspark==3.5.5" \
      "apache-sedona==1.9.1" \
      boto3 requests pyarrow pandas h3 python-dotenv

# JAR Spark: Sedona, GeoTools, JDBC PostgreSQL, S3A (Hadoop 3.3.4 = bawaan PySpark 3.5)
RUN JARS=$(python -c "import pyspark,os;print(os.path.join(os.path.dirname(pyspark.__file__),'jars'))") \
 && cd "$JARS" \
 && M=https://repo1.maven.org/maven2 \
 && curl -fsSLO $M/org/apache/sedona/sedona-spark-shaded-3.5_2.12/1.9.1/sedona-spark-shaded-3.5_2.12-1.9.1.jar \
 && curl -fsSLO $M/org/datasyslab/geotools-wrapper/1.9.1-33.5/geotools-wrapper-1.9.1-33.5.jar \
 && curl -fsSLO $M/org/postgresql/postgresql/42.7.4/postgresql-42.7.4.jar \
 && curl -fsSLO $M/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar \
 && curl -fsSLO $M/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar
