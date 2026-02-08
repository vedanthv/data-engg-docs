from airflow.sdk import dag, task
from datetime import datetime

@dag(
    dag_id="simple_etl_taskflow_example",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False
)
def simple_etl():

    # -------------------------
    # EXTRACT
    # -------------------------
    @task
    def extract():
        # Dummy source data (like API or file)
        sales_data = [
            {"order_id": 1, "amount": 100},
            {"order_id": 2, "amount": 200},
            {"order_id": 3, "amount": 150},
        ]
        print("Extracted data:", sales_data)
        return sales_data   # returned value goes to XCom automatically


    # -------------------------
    # TRANSFORM
    # -------------------------
    @task
    def transform(data):
        # Example transformation
        total_sales = sum(order["amount"] for order in data)

        result = {
            "total_sales": total_sales,
            "record_count": len(data)
        }

        print("Transformed result:", result)
        return result   # pass to next task


    # -------------------------
    # LOAD
    # -------------------------
    @task
    def load(summary):
        # Dummy load step (normally DB insert or S3 upload)
        print("Loading data...")
        print(f"Total Sales: {summary['total_sales']}")
        print(f"Record Count: {summary['record_count']}")


    # -------------------------
    # PIPELINE FLOW
    # -------------------------
    extracted_data = extract()
    transformed_data = transform(extracted_data)
    load(transformed_data)


simple_etl()
