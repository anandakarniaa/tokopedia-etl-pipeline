import os
import psycopg


def save_postgres(df):

    conn = psycopg.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "tokopedia_db"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres")
    )

    try:

        with conn.cursor() as cur:

            # Clear existing data
            cur.execute(
                "TRUNCATE TABLE products RESTART IDENTITY CASCADE"
            )

            print(
                f"📊 DataFrame yang akan masuk PostgreSQL: {len(df)} rows"
            )

            for index, (_, row) in enumerate(
                df.iterrows(),
                start=1
            ):

                print(
                    f"Processing row {index}/{len(df)}"
                )

                cur.execute(
                    """
                    INSERT INTO products (
                        product_name,
                        price,
                        seller,
                        city,
                        sold,
                        rating,
                        revenue,
                        price_category,
                        popular_product
                    )
                    VALUES (
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s
                    )
                    """,
                    (
                        row["Product Name"],
                        row["Price"],
                        row["Seller"],
                        row["City"],
                        row["Sold"],
                        row["Rating"],
                        row["Revenue"],
                        row["Price_Category"],
                        row["Popular_Product"]
                    )
                )

        conn.commit()

        print(
            "✅ Data successfully loaded to PostgreSQL"
        )

    except Exception as e:

        conn.rollback()

        print(
            f"❌ PostgreSQL loading failed: {e}"
        )

        raise

    finally:

        conn.close()