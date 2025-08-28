import os
import json
from sqlalchemy import create_engine, text
from .models import BrandData
from dotenv import load_dotenv

load_dotenv()

# *************************** DATABASE CONFIGURATION ******
# Replace with your actual MySQL credentials.

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("No DATABASE_URL found in environment variables.")


try:
    engine = create_engine(DATABASE_URL)

    with engine.connect() as connection:
        print("Successfully connected to the MySQL database.")
except Exception as e:
    print(f"Error connecting to the database: {e}")
    engine = None
# *******************************************************************

def saveBrandData(brand_data: BrandData, website_url: str):
    if not engine:
        print("Database engine not initialized. Cannot save data.")
        return

    sql = text("""
        INSERT INTO brands (
            website_url, product_catalog, social_handles, contact_details,
            privacy_policy_url, privacy_policy_content,
            refund_policy_url, refund_policy_content,
            about_us_url, about_us_content,
            contact_us_url, contact_us_content,
            faqs_url, faqs_content,
            blogs_url, blogs_content,
            track_order_url, track_order_content
        ) VALUES (
            :website_url, :product_catalog, :social_handles, :contact_details,
            :privacy_policy_url, :privacy_policy_content,
            :refund_policy_url, :refund_policy_content,
            :about_us_url, :about_us_content,
            :contact_us_url, :contact_us_content,
            :faqs_url, :faqs_content,
            :blogs_url, :blogs_content,
            :track_order_url, :track_order_content
        )
        ON DUPLICATE KEY UPDATE
            scraped_at = CURRENT_TIMESTAMP,
            product_catalog = VALUES(product_catalog),
            social_handles = VALUES(social_handles),
            contact_details = VALUES(contact_details),
            privacy_policy_url = VALUES(privacy_policy_url),
            privacy_policy_content = VALUES(privacy_policy_content),
            refund_policy_url = VALUES(refund_policy_url),
            refund_policy_content = VALUES(refund_policy_content),
            about_us_url = VALUES(about_us_url),
            about_us_content = VALUES(about_us_content),
            contact_us_url = VALUES(contact_us_url),
            contact_us_content = VALUES(contact_us_content),
            faqs_url = VALUES(faqs_url),
            faqs_content = VALUES(faqs_content),
            blogs_url = VALUES(blogs_url),
            blogs_content = VALUES(blogs_content),
            track_order_url = VALUES(track_order_url),
            track_order_content = VALUES(track_order_content);
    """)

    #fix for http pydantic class to json
    socialHandles = {
        platform : str(url) for platform,url in brand_data.social_handles.items() if url
    }

    params = {
        "website_url": website_url,

        "product_catalog": json.dumps([p.model_dump() for p in brand_data.product_catalog]),
        "social_handles": json.dumps(socialHandles),
        "contact_details": brand_data.contact_details.model_dump_json() if brand_data.contact_details else None,
        
        "privacy_policy_url": str(brand_data.privacy_policy.url) if brand_data.privacy_policy else None,
        "privacy_policy_content": brand_data.privacy_policy.content if brand_data.privacy_policy else None,
        "refund_policy_url": str(brand_data.refund_policy.url) if brand_data.refund_policy else None,
        "refund_policy_content": brand_data.refund_policy.content if brand_data.refund_policy else None,
        "about_us_url": str(brand_data.about_us.url) if brand_data.about_us else None,
        "about_us_content": brand_data.about_us.content if brand_data.about_us else None,
        "contact_us_url": str(brand_data.contact_us.url) if brand_data.contact_us else None,
        "contact_us_content": brand_data.contact_us.content if brand_data.contact_us else None,
        "faqs_url": str(brand_data.faqs.url) if brand_data.faqs else None,
        "faqs_content": brand_data.faqs.content if brand_data.faqs else None,
        "blogs_url": str(brand_data.blogs.url) if brand_data.blogs else None,
        "blogs_content": brand_data.blogs.content if brand_data.blogs else None,
        "track_order_url": str(brand_data.track_order.url) if brand_data.track_order else None,
        "track_order_content": brand_data.track_order.content if brand_data.track_order else None,
    }

    try:
        with engine.connect() as connection:
            connection.execute(sql, params)
            connection.commit()
            print(f"Successfully saved data for {website_url} to the database.")
    except Exception as e:
        print(f"Failed to save data for {website_url}. Error: {e}")