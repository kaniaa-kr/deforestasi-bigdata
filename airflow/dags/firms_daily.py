from datetime import datetime, timedelta

from airflow.decorators import dag, task

default_args = {
    "owner": "kania",
    "retries": 3,
    "retry_delay": timedelta(minutes=10),
    "retry_exponential_backoff": True,
    "max_retry_delay": timedelta(hours=1),
}


@dag(
    dag_id="firms_daily",
    start_date=datetime(2026, 11, 1),
    schedule="0 3 * * *",          # 03:00 UTC = 10:00 WIB
    catchup=False,
    max_active_runs=1,
    default_args=default_args,
    params={"lookback_days": 1},
    tags=["firms", "ingest"],
)
def firms_daily():
    @task
    def plan_days(ds=None, params=None):
        from datetime import date
        lb = int(params.get("lookback_days", 1))
        d = date.fromisoformat(ds)
        return [(d - timedelta(days=i)).isoformat() for i in range(lb, -1, -1)]

    @task
    def check_availability(days):
        from ingestion import firms
        firms.check_availability(max(days))
        return days

    @task
    def fetch_day(day):
        from ingestion import firms
        return firms.fetch_day(day)

    @task
    def build_silver(info):
        from ingestion import firms
        return firms.build_silver(info["day"])

    @task
    def report(results):
        for r in results:
            print(r)
        total = sum(r["silver_rows"] for r in results)
        print(f"TOTAL silver run ini: {total} baris")

    days = plan_days()
    ok = check_availability(days)
    raw = fetch_day.expand(day=ok)
    silver = build_silver.expand(info=raw)
    report(silver)


firms_daily()
