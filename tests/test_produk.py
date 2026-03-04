def test_list_produk(client):
    response = client.get("/produk")
    assert response.status_code == 200

def test_tambah_produk(client):
    response = client.post("/produk", json={
        "nama": "Kopi", "harga": 50000, "stok": 100
    })
    assert response.status_code == 200
    assert response.json()["nama"] == "Kopi"

def test_buat_order_sukses(client):
    produk = client.post("/produk", json={
        "nama": "Teh", "harga": 30000, "stok": 10
    }).json()
    response = client.post("/order", json={
        "nama_pembeli": "Arka",
        "email": "arka@email.com",
        "jumlah": 2,
        "produk_id": produk["id"]
    })
    assert response.status_code == 200
    assert response.json()["total"] == 60000

def test_stok_tidak_cukup(client):
    produk = client.post("/produk", json={
        "nama": "Susu", "harga": 20000, "stok": 1
    }).json()
    response = client.post("/order", json={
        "nama_pembeli": "Budi",
        "email": "budi@email.com",
        "jumlah": 99,
        "produk_id": produk["id"]
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Stok tidak cukup!"

def test_hapus_produk_tidak_ada(client):
    response = client.delete("/produk/9999")
    assert response.status_code == 404
