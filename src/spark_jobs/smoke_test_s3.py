import os
from sedona.spark import SedonaContext

b = (SedonaContext.builder().appName("smoke-s3").master("local[2]")
     .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
     .config("spark.hadoop.fs.s3a.endpoint", os.environ["S3_ENDPOINT"])
     .config("spark.hadoop.fs.s3a.access.key", os.environ["S3_ACCESS_KEY"])
     .config("spark.hadoop.fs.s3a.secret.key", os.environ["S3_SECRET_KEY"])
     .config("spark.hadoop.fs.s3a.path.style.access", "true")
     .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
     .config("spark.hadoop.fs.s3a.aws.credentials.provider",
             "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider")
     .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem"))
sedona = SedonaContext.create(b.getOrCreate())

# 1) Sedona berfungsi
sedona.sql("""SELECT ST_Intersects(
  ST_GeomFromWKT('POLYGON((0 0,0 2,2 2,2 0,0 0))'), ST_Point(1.0, 1.0)) AS ok""").show()

# 2) Tulis lalu baca Parquet lewat s3a://
path = f"s3a://{os.environ['S3_BUCKET']}/ref/smoke_test"
sedona.range(1000).write.mode("overwrite").parquet(path)
print("ROWS READ BACK:", sedona.read.parquet(path).count())
print("SMOKE S3 OK")
