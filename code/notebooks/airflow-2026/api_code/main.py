from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta, date
import random
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets


security = HTTPBasic()

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "manish")

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username


app = FastAPI()

# ------------ REQUEST BODY MODEL ------------

class FilterRequest(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    limit: Optional[int] = 50


# ------------ UTILITY FUNCTIONS ------------

devices = ["mobile", "desktop", "tablet"]
browsers = ["Chrome", "Firefox", "Safari", "Edge"]
referrers = ["google", "direct", "social", "email_campaign", "ad"]
payment_methods = ["card", "upi", "netbanking", "cod"]

def random_date(start, end):
    """Return random datetime between two full dates."""
    start_dt = datetime.combine(start, datetime.min.time())
    end_dt = datetime.combine(end, datetime.max.time())

    delta = end_dt - start_dt
    random_seconds = random.randint(0, int(delta.total_seconds()))

    return start_dt + timedelta(seconds=random_seconds)



def generate_login_data(start_date, end_date, limit):
    login_users = []

    for i in range(limit):
        user_id = f"user_{random.randint(10000, 99999)}"
        login_users.append({
            "user_id": user_id,
            "login_time": random_date(start_date, end_date),
            "device": random.choice(devices),
            "browser": random.choice(browsers),
            "referrer": random.choice(referrers),
            "session_duration": random.randint(30, 600),
            "geo_location": random.choice(["US", "IN", "UK", "CA", "DE"]),
            "is_new_user": random.choice([True, False])
        })

    return login_users


def generate_product_page_data(login_users):
    product_users = []

    for user in login_users:
        # 80% users visit product page
        if random.random() < 0.80:
            product_users.append({
                "user_id": user["user_id"],
                "view_time": user["login_time"] + timedelta(minutes=random.randint(1, 10)),
                "product_id": random.randint(1000, 9999),
                "time_on_page": random.randint(5, 180),
                "scroll_depth_percent": random.randint(10, 100),
                "clicked_recommendations": random.randint(0, 5),
                "added_to_wishlist": random.choice([True, False]),
                "added_to_cart": random.random() < 0.60  # 60% add to cart
            })
    return product_users


def generate_checkout_data(product_users):
    checkout_users = []

    for user in product_users:
        if user["added_to_cart"]:
            checkout_users.append({
                "user_id": user["user_id"],
                "checkout_time": user["view_time"] + timedelta(minutes=random.randint(5, 15)),
                "items_in_cart": random.randint(1, 4),
                "total_value": round(random.uniform(20, 500), 2),
                "payment_method": random.choice(payment_methods),
                "coupon_used": random.choice([True, False]),
                "abandoned_cart": False
            })

    return checkout_users


# ------------ ENDPOINTS ------------

@app.post("/getAll")
def get_all_data(filters: FilterRequest, user: str = Depends(authenticate)):
    start_date = filters.start_date or date.today()
    end_date = filters.end_date or date.today()
    limit = filters.limit or 50

    login = generate_login_data(start_date, end_date, limit)
    product = generate_product_page_data(login)
    checkout = generate_checkout_data(product)

    return {
        "login_users": login,
        "product_page_users": product,
        "checkout_users": checkout
    }


@app.post("/loginUsers")
def get_login_users(filters: FilterRequest, user: str = Depends(authenticate)):
    start_date = filters.start_date or date.today()
    end_date = filters.end_date or date.today()
    limit = filters.limit or 50

    return generate_login_data(start_date, end_date, limit)


@app.post("/productUsers")
def get_product_users(filters: FilterRequest, user: str = Depends(authenticate)):
    start_date = filters.start_date or date.today()
    end_date = filters.end_date or date.today()
    limit = filters.limit or 50

    login = generate_login_data(start_date, end_date, limit)
    return generate_product_page_data(login)


@app.post("/checkoutUsers")
def get_checkout_users(filters: FilterRequest, user: str = Depends(authenticate)):
    start_date = filters.start_date or date.today()
    end_date = filters.end_date or date.today()
    limit = filters.limit or 50

    login = generate_login_data(start_date, end_date, limit)
    product = generate_product_page_data(login)
    return generate_checkout_data(product)
