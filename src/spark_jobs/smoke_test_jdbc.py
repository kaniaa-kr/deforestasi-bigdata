import os
from sedona.spark import SedonaContext

sedona = SedonaContext.create(
    SedonaContext.builder().appName("smoke-jdbc").master("local[2]").getOrCreate())

url = (f"jdbc:postgresql://{os.environ['SUPABASE_DB_HOST']}:{os.environ['SUPABASE_DB_PORT']}"
       f"/{os.environ['SUPABASE_DB_NAME']}?sslmode=require")
df = (sedona.read.format("jdbc")
      .option("url", url)
      .option("driver", "org.postgresql.Driver")
      .option("user", os.environ["SUPABASE_READER_USER"])
      .option("password", os.environ["SUPABASE_READER_PASSWORD"])
      .option("dbtable", "(SELECT extensions.postgis_version() AS v) t")
      .load())
df.show(truncate=False)
print("SMOKE JDBC OK")
