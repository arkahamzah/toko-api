from celery import Celery
import time
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "tasks",
    broker=REDIS_URL,
    backend=REDIS_URL
)

@celery_app.task
def kirim_email(email: str, pesan: str):
    print(f"Mengirim email ke {email}...")
    time.sleep(3)
    print(f"Email terkirim ke {email}: {pesan}")
    return {"status": "terkirim", "email": email}

@celery_app.task
def proses_order(order_id: int):
    print(f"Memproses order #{order_id}...")
    time.sleep(2)
    print(f"Order #{order_id} selesai diproses!")
    return {"status": "selesai", "order_id": order_id}
