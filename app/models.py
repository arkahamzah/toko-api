from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Produk(Base):
    __tablename__ = "produk"
    id = Column(Integer, primary_key=True)
    nama = Column(String, nullable=False)
    harga = Column(Integer, nullable=False)
    stok = Column(Integer, default=0)
    orders = relationship("Order", back_populates="produk")

class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    nama_pembeli = Column(String, nullable=False)
    jumlah = Column(Integer, nullable=False)
    produk_id = Column(Integer, ForeignKey("produk.id"))
    produk = relationship("Produk", back_populates="orders")
