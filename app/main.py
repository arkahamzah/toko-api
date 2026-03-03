from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import engine, get_db
from app.models import Produk, Order, Base
from app.cache import get_cache, set_cache, delete_cache
import json

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Toko API")

# Schema
class ProdukRequest(BaseModel):
    nama: str
    harga: int
    stok: int = 0

class OrderRequest(BaseModel):
    nama_pembeli: str
    jumlah: int
    produk_id: int

# PRODUK
@app.get("/produk")
def list_produk(db: Session = Depends(get_db)):
    cached = get_cache("produk:all")
    if cached:
        return {"source": "cache", "data": json.loads(cached)}
    produk = db.query(Produk).all()
    data = [{"id": p.id, "nama": p.nama, "harga": p.harga, "stok": p.stok} for p in produk]
    set_cache("produk:all", json.dumps(data), expire=60)
    return {"source": "database", "data": data}

@app.post("/produk")
def tambah_produk(data: ProdukRequest, db: Session = Depends(get_db)):
    produk = Produk(nama=data.nama, harga=data.harga, stok=data.stok)
    db.add(produk)
    db.commit()
    db.refresh(produk)
    delete_cache("produk:all")
    return {"id": produk.id, "nama": produk.nama, "harga": produk.harga}

@app.delete("/produk/{produk_id}")
def hapus_produk(produk_id: int, db: Session = Depends(get_db)):
    produk = db.query(Produk).filter(Produk.id == produk_id).first()
    if not produk:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan!")
    db.delete(produk)
    db.commit()
    delete_cache("produk:all")
    return {"pesan": "Produk berhasil dihapus!"}

# ORDER
@app.post("/order")
def buat_order(data: OrderRequest, db: Session = Depends(get_db)):
    produk = db.query(Produk).filter(Produk.id == data.produk_id).first()
    if not produk:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan!")
    if produk.stok < data.jumlah:
        raise HTTPException(status_code=400, detail="Stok tidak cukup!")
    produk.stok -= data.jumlah
    order = Order(nama_pembeli=data.nama_pembeli, jumlah=data.jumlah, produk_id=data.produk_id)
    db.add(order)
    db.commit()
    db.refresh(order)
    return {
        "id": order.id,
        "nama_pembeli": order.nama_pembeli,
        "produk": produk.nama,
        "jumlah": order.jumlah,
        "total": produk.harga * order.jumlah
    }
