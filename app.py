from flask import Flask, session, redirect, request
import sqlite3

app = Flask(__name__)
app.secret_key = "shoppy_secret_key"

# ================= DATABASE =================
def get_db():
    conn = sqlite3.connect("shop.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price INTEGER,
            image TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS stock (
            product_id INTEGER PRIMARY KEY,
            qty INTEGER
        )
    """)

    if c.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 0:
        for p in PRODUCTS:
            c.execute(
                "INSERT INTO products (id,name,price,image) VALUES (?,?,?,?)",
                (p["id"], p["name"], p["price"], p["image"])
            )
            c.execute(
                "INSERT OR IGNORE INTO stock VALUES (?,?)",
                (p["id"], 10)
            )

    conn.commit()
    conn.close()

# ================= ADMIN =================
USERS = {
    "Razak": {"password": "123", "role": "admin"}
}

# ================= PRODUK =================
PRODUCTS = [
   {"id": 1, "name": "Laptop ASUS", "price": 8500000, "image": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8"},
    {"id": 2, "name": "Laptop Lenovo", "price": 7800000, "image": "https://laptopmedia.com/wp-content/uploads/2024/09/04_IdeaPad_Slim_5_13_10_Cloud_Grey_Hero_Rear_Facing_Right.jpeg"},
    {"id": 3, "name": "Laptop Acer", "price": 7200000, "image": "https://laptopmedia.com/wp-content/uploads/2020/10/2-34-e1603717432898.jpg"},
    {"id": 4, "name": "Laptop HP", "price": 8000000, "image": "https://c1.neweggimages.com/ProductImageCompressAll1280/34-269-132-V04.jpg"},
    {"id": 5, "name": "Laptop MSI", "price": 12500000, "image": "https://m.media-amazon.com/images/I/81-3FfpcwML._AC_.jpg"},

    {"id": 6, "name": "Mouse USB", "price": 120000, "image": "https://images.unsplash.com/photo-1527814050087-3793815479db"},
    {"id": 7, "name": "Mouse Gaming", "price": 250000, "image": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7"},
    {"id": 8, "name": "Keyboard Office", "price": 180000, "image": "https://www.keyboardco.com/product-images/portuguese_keyboard_black_usb_large.jpg"},
    {"id": 9, "name": "Keyboard Gaming RGB", "price": 450000, "image": "https://images.unsplash.com/photo-1603481546579-65d935ba9cdd"},
    {"id": 10, "name": "Mouse Pad Gaming", "price": 75000, "image": "https://m.media-amazon.com/images/I/71iMelPup4L.jpg"},

    {"id": 11, "name": "Headset Gaming", "price": 350000, "image": "https://images.unsplash.com/photo-1585298723682-7115561c51b7"},
    {"id": 12, "name": "Earphone Wireless", "price": 280000, "image": "https://www.store4u.pk/wp-content/uploads/2022/10/M1999909.jpg"},
    {"id": 13, "name": "Speaker Bluetooth", "price": 300000, "image": "https://m.media-amazon.com/images/I/81uJyMRONOL.jpg"},
    {"id": 14, "name": "Soundbar Mini", "price": 650000, "image": "https://m.media-amazon.com/images/I/61hoRvQb9DL._AC_SL1500_.jpg"},
    {"id": 15, "name": "Microphone USB", "price": 420000, "image": "https://i5.walmartimages.com/asr/c2b32e2c-a366-45c4-a2b1-f897551404c8.52c24c1a3833459da692b86ad0a4c518.jpeg"},

    {"id": 16, "name": "Smartphone Android", "price": 3200000, "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9"},
    {"id": 17, "name": "Smartphone Gaming", "price": 5500000, "image": "https://fijitraders.com/wp-content/uploads/2021/09/ASUS-ROG-Phone-5-2021-5G-Dual-SIM-Smartphone-16GB256GB-Phantom-Black-1.jpg"},
    {"id": 18, "name": "Tablet Android", "price": 4100000, "image": "https://image.made-in-china.com/2f0j00zhRgbrOCbjqP/Newest-Teclast-P20HD-Tablet-Android-10-Tablets-PC-4G-LTE-10-1-Octa-Core-Tabletas.jpg"},
    {"id": 19, "name": "Smartwatch", "price": 1250000, "image": "https://i.pinimg.com/originals/ee/5d/99/ee5d998ec7a5f833d7ad0785ee8505f1.jpg"},
    {"id": 20, "name": "Smart Band", "price": 450000, "image": "https://images.unsplash.com/photo-1617043786394-f977fa12eddf"},

    {"id": 21, "name": "Flashdisk 32GB", "price": 60000, "image": "https://tse3.mm.bing.net/th/id/OIP.AOoBqBuVVu4OWkoqbClKNgHaHa?cb=defcachec2&rs=1&pid=ImgDetMain&o=7&rm=3"},
    {"id": 22, "name": "Flashdisk 64GB", "price": 90000, "image": "https://down-id.img.susercontent.com/file/id-11134207-7r98o-lqn11jj16pa701"},
    {"id": 23, "name": "SSD 256GB", "price": 550000, "image": "https://a-static.mlcdn.com.br/800x560/hd-ssd-256-gb-m-2-sata-macrovip-gold-nvme-mvgld-256gb/olistplus/opm3zc70gyu25l1x/0cb4241209fe7bc3df86b0f9f1516188.jpeg"},
    {"id": 24, "name": "SSD 512GB", "price": 950000, "image": "https://simmtronics.co.in/wp-content/uploads/2022/12/512GB-M.2-Sata-Solid-State-Drive-%E2%80%93-SSD-S950P-2-1.webp"},
    {"id": 25, "name": "Harddisk External 1TB", "price": 850000, "image": "https://cf.shopee.co.id/file/957e9e8bdd00f1261841e35c44494fc9"},

    {"id": 26, "name": "Monitor 22 Inch", "price": 1850000, "image": "https://down-id.img.susercontent.com/file/id-11134207-7r98s-ly0jc3y61sbw5a"},
    {"id": 27, "name": "Monitor 24 Inch", "price": 2100000, "image": "https://m.media-amazon.com/images/I/71IC5qsZKpL._AC_SL1000_.jpg"},
    {"id": 28, "name": "Printer Inkjet", "price": 1750000, "image": "https://i1.adis.ws/i/canon/3771C006AA_PIXMA-TS3350-BLACK_01"},
    {"id": 29, "name": "Scanner Dokumen", "price": 1650000, "image": "https://static.inkstation.com.au/images/epson_scanner_ff680w.jpg"},
    {"id": 30, "name": "Webcam HD", "price": 320000, "image": "https://www.popsci.com/uploads/2021/10/15/Elgato-Facecam-Edit.jpg"},

    {"id": 31, "name": "Router WiFi", "price": 380000, "image": "https://png.pngtree.com/background/20240507/original/pngtree-d-render-of-white-background-with-modern-wifi-router-featuring-glowing-picture-image_8834877.jpg"},
    {"id": 32, "name": "Modem 4G", "price": 450000, "image": "https://lzd-img-global.slatic.net/g/p/47cd59ba2e6ab970ee630a7237f72111.png_720x720q80.png"},
    {"id": 33, "name": "Kabel HDMI", "price": 60000, "image": "https://upload.jaknot.com/2023/01/images/products/dd56fe/original/fsu-kabel-hdmi-gold-plated-high-speed-od73mm-1080p-135-meter-shh11.jpg"},
    {"id": 34, "name": "Kabel LAN", "price": 40000, "image": "https://id-test-11.slatic.net/p/0fa536ab80e4a2cfaffb544f0be9fbda.jpg"},
    {"id": 35, "name": "USB Hub", "price": 85000, "image": "https://lzd-img-global.slatic.net/g/p/2d66c4d9b787395a622762a8fe32873b.jpg_720x720q80.jpg"},

    {"id": 36, "name": "Cooling Pad Laptop", "price": 180000, "image": "https://images-na.ssl-images-amazon.com/images/I/71xim6bGiYL.jpg"},
    {"id": 37, "name": "Charger Laptop Universal", "price": 250000, "image": "https://i5.walmartimages.com/seo/96W-Universal-Laptop-Charger-Adjustable-Voltage-for-Multiple-Laptops-Safe_16fbcaaa-c95a-4d19-b78a-a78c4ceb14ef.119bbf5cb854e0e7474c38c4845f7fe9.jpeg"},
    {"id": 38, "name": "Power Bank 10000mAh", "price": 180000, "image": "https://tse2.mm.bing.net/th/id/OIP.OHLkz9IfSr08pBeT5bFi8AHaHa?cb=defcachec2&rs=1&pid=ImgDetMain&o=7&rm=3"},
    {"id": 39, "name": "Power Bank 20000mAh", "price": 250000, "image": "https://cf.shopee.ph/file/2758509ac4e2b8fec7d1ccdafa78497f"},
    {"id": 40, "name": "Tripod Kamera", "price": 220000, "image": "https://static.jakmall.id/2022/12/images/products/1411d1/detail/heonyirry-tripod-profesional-untuk-kamera-digital-3110.jpg"},

    {"id": 41, "name": "Kamera Digital", "price": 4200000, "image": "https://www.bhphotovideo.com/images/images2500x2500/nikon_13302_d7100_dslr_camera_with_1005009.jpg"},
    {"id": 42, "name": "Action Camera", "price": 3100000, "image": "https://images.unsplash.com/photo-1519183071298-a2962eadcdb2"},
    {"id": 43, "name": "Drone Mini", "price": 4500000, "image": "https://m.media-amazon.com/images/I/715mtPQP4IL._AC_SL1500_.jpg"},
    {"id": 44, "name": "Memory Card 64GB", "price": 120000, "image": "https://m.media-amazon.com/images/I/71UIgvXR6nL._AC_.jpg"},
    {"id": 45, "name": "Memory Card 128GB", "price": 220000, "image": "https://m.media-amazon.com/images/I/71TRuPdTPEL._AC_.jpg"},

    {"id": 46, "name": "Game Controller", "price": 380000, "image": "https://cdn.whatgadget.net/wp-content/uploads/2023/09/23152641/168838.jpg"},
    {"id": 47, "name": "VR Headset", "price": 6500000, "image": "https://img.freepik.com/premium-photo/virtual-reality-experience-branding-showcase-incorporate-logo-into-vr-headset-designs-virtual-environments-promotional-materials_1029473-130595.jpg"},
    {"id": 48, "name": "Projector Mini", "price": 2800000, "image": "https://m.media-amazon.com/images/I/710FDCXgN8L._AC_.jpg"},
    {"id": 49, "name": "UPS 1200VA", "price": 1750000, "image": "https://img.mbizmarket.co.id/products/thumbs/800x800/2022/10/05/5707f13ea4c64650a54c2390d7099083.jpg"},
    {"id": 50, "name": "Stop Kontak Surge Protector", "price": 150000, "image": "https://down-id.img.susercontent.com/file/id-11134201-7rasi-m1nrfyvc9g0v5e"},
]

# ================= TEMPLATE =================
def base_html(content):
    return f"""
<!DOCTYPE html>
<html>
<head>
<title>Shoppy</title>
<style>
body {{ font-family: Arial; background:#f4f6f8; margin:0; }}
header {{ background:#ee4d2d; color:white; padding:15px; display:flex; justify-content:space-between; align-items:center; }}
nav a {{ color:white; margin-left:15px; text-decoration:none; }}
.container {{ padding:20px; }}
.products {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:20px; }}
.card {{ background:white; padding:15px; border-radius:8px; text-align:center; }}
.card img {{ width:100%; height:150px; object-fit:cover; }}
.btn {{ background:#ee4d2d; color:white; padding:6px 10px; border-radius:5px; text-decoration:none; margin:2px; }}
.gray {{ background:gray; }}
</style>
</head>
<body>{content}</body>
</html>
"""

# ================= AUTH =================
@app.route("/")
def index():
    return redirect("/login")

@app.route("/login", methods=["GET","POST"])
def login():
    msg=""
    if request.method=="POST":
        u,p=request.form["username"],request.form["password"]

        if u in USERS and USERS[u]["password"]==p:
            session["user"]=u
            session["role"]="admin"
            session["cart"]={}
            return redirect("/shop")

        c=get_db().cursor()
        if c.execute("SELECT * FROM users WHERE username=? AND password=?",(u,p)).fetchone():
            session["user"]=u
            session["role"]="user"
            session["cart"]={}
            return redirect("/shop")

        msg="Login gagal"

    return base_html(f"""
    <form method=POST class=card style="width:300px;margin:auto">
    <h3>Login</h3>
    <input name=username required><br><br>
    <input type=password name=password required><br><br>
    <button class=btn>Login</button>
    <p style="color:red">{msg}</p>
    <a href="/register">Daftar</a>
    </form>
    """)

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method=="POST":
        u,p=request.form["username"],request.form["password"]
        c=get_db().cursor()
        if not c.execute("SELECT * FROM users WHERE username=?",(u,)).fetchone():
            c.execute("INSERT INTO users VALUES (?,?)",(u,p))
            c.connection.commit()
            return redirect("/login")

    return base_html("""
    <form method=POST class=card style="width:300px;margin:auto">
    <h3>Register</h3>
    <input name=username required><br><br>
    <input type=password name=password required><br><br>
    <button class=btn>Daftar</button>
    </form>
    """)

# ================= SHOP =================
@app.route("/shop")
def shop():
    if "user" not in session:
        return redirect("/login")

    keyword = request.args.get("q", "").strip()
    c = get_db().cursor()

    # ===== SEARCH LOGIC =====
    if keyword:
        products = c.execute(
            "SELECT * FROM products WHERE name LIKE ?",
            (f"%{keyword}%",)
        ).fetchall()
    else:
        products = c.execute("SELECT * FROM products").fetchall()

    # ===== PRODUCT CARD =====
    cards = ""
    for p in products:
        stock = c.execute(
            "SELECT qty FROM stock WHERE product_id=?",
            (p["id"],)
        ).fetchone()["qty"]

        btn = "<span class='btn gray'>Habis</span>" if stock <= 0 else \
              f"<a class='btn' href='/add/{p['id']}'>Tambah</a>"

        cards += f"""
        <div class="card">
            <img src="{p['image']}">
            <h4>{p['name']}</h4>
            <p>Rp {p['price']:,}</p>
            <p>Stok: {stock}</p>
            {btn}
        </div>
        """

    if not cards:
        cards = "<h3>❌ Produk tidak ditemukan</h3>"

    # ===== ADMIN MENU =====
    admin_menu = """
        <a href="/admin/stock">📦 Stok</a>
        <a href="/admin/add-product">➕ Produk</a>
    """ if session["role"] == "admin" else ""

    # ===== FINAL HTML =====
    return base_html(f"""
    <header>
        <h3>Shoppy</h3>

        <form method="GET" action="/shop" style="display:flex; gap:5px;">
            <input type="text" name="q" placeholder="Cari produk..."
                   value="{keyword}"
                   style="padding:6px;border-radius:5px;border:none;">
            <button class="btn">Cari</button>
        </form>

        <nav>
            {admin_menu}
            <a href="/cart">🛒 {sum(session["cart"].values())}</a>
            <a href="/logout">Logout</a>
        </nav>
    </header>

    <div class="container">
        <div class="products">
            {cards}
        </div>
    </div>
    """)

# ================= ADD TO CART =================
@app.route("/add/<int:id>")
def add(id):
    c = get_db().cursor()
    stock = c.execute("SELECT qty FROM stock WHERE product_id=?",(id,)).fetchone()

    if stock and stock["qty"]>0:
        cart = session.get("cart", {})
        cart[str(id)] = cart.get(str(id),0) + 1
        session["cart"] = cart   # 🔥 FIX

        c.execute("UPDATE stock SET qty=qty-1 WHERE product_id=?",(id,))
        c.connection.commit()

    return redirect("/shop")

# ================= CART =================
@app.route("/cart")
def cart():
    c=get_db().cursor()
    rows=""
    total=0

    for pid,qty in session.get("cart",{}).items():
        p=c.execute("SELECT * FROM products WHERE id=?",(pid,)).fetchone()
        subtotal=p["price"]*qty
        total+=subtotal

        rows+=f"""
        <tr>
            <td>{p['name']}</td>
            <td>{qty}</td>
            <td>Rp {subtotal:,}</td>
            <td>
                <a class=btn href="/cart/plus/{pid}">➕</a>
                <a class="btn gray" href="/cart/min/{pid}">➖</a>
            </td>
        </tr>
        """

    if not rows:
        rows="<tr><td colspan=4>Keranjang kosong</td></tr>"

    return base_html(f"""
    <div class=container>
    <h2>Keranjang</h2>
    <table border=1 cellpadding=10 width=100%>
        <tr><th>Produk</th><th>Qty</th><th>Subtotal</th><th>Aksi</th></tr>
        {rows}
    </table>
    <h3>Total: Rp {total:,}</h3>
    <a class=btn href="/shop">⬅ Belanja</a>
    <a class="btn gray" href="/checkout">Checkout</a>
    </div>
    """)

# ================= ADMIN STOCK =================
@app.route("/admin/stock")
def admin_stock():
    if session.get("role")!="admin":
        return "Admin only"

    c=get_db().cursor()
    rows=""
    for p in c.execute("SELECT * FROM products").fetchall():
        qty=c.execute("SELECT qty FROM stock WHERE product_id=?",(p["id"],)).fetchone()["qty"]
        rows+=f"""
        <tr>
            <td>{p['name']}</td>
            <td>{qty}</td>
            <td>
                <a class=btn href="/admin/stock/plus/{p['id']}">➕</a>
                <a class=btn gray href="/admin/stock/minus/{p['id']}">➖</a>
            </td>
        </tr>
        """

    return base_html(f"""
    <div class=container>
    <h2>Manajemen Stok</h2>
    <table border=1 cellpadding=10>
    <tr><th>Produk</th><th>Stok</th><th>Aksi</th></tr>
    {rows}
    </table>
    <br>
    <a class=btn href="/shop">🔄 Kembali ke Belanja</a>
    </div>
    """)

@app.route("/admin/stock/plus/<int:id>")
def stock_plus(id):
    c=get_db().cursor()
    c.execute("UPDATE stock SET qty=qty+1 WHERE product_id=?",(id,))
    c.connection.commit()
    return redirect("/admin/stock")

@app.route("/admin/stock/minus/<int:id>")
def stock_minus(id):
    c=get_db().cursor()
    c.execute("UPDATE stock SET qty=CASE WHEN qty>0 THEN qty-1 ELSE 0 END WHERE product_id=?",(id,))
    c.connection.commit()
    return redirect("/admin/stock")

# ================= ADMIN ADD PRODUCT =================
@app.route("/admin/add-product", methods=["GET","POST"])
def add_product():
    if session.get("role")!="admin":
        return "Admin only"

    if request.method=="POST":
        c=get_db().cursor()
        c.execute("INSERT INTO products (name,price,image) VALUES (?,?,?)",
                  (request.form["name"],int(request.form["price"]),request.form["image"]))
        pid=c.lastrowid
        c.execute("INSERT INTO stock VALUES (?,?)",(pid,int(request.form["qty"])))
        c.connection.commit()
        return redirect("/shop")

    return base_html("""
    <div class=container>
    <h2>Tambah Produk</h2>
    <form method=POST class=card style="max-width:400px">
        <input name=name placeholder="Nama Produk" required><br><br>
        <input name=price type=number placeholder="Harga" required><br><br>
        <input name=image placeholder="URL Gambar" required><br><br>
        <input name=qty type=number placeholder="Stok Awal" required><br><br>
        <button class=btn>Simpan</button>
    </form>
    </div>
    """)

# ================= PLUS QTY (FIX) =================
@app.route("/cart/plus/<int:id>")
def cart_plus(id):
    c=get_db().cursor()
    stock=c.execute("SELECT qty FROM stock WHERE product_id=?",(id,)).fetchone()

    if stock and stock["qty"]>0:
        cart = session.get("cart", {})
        cart[str(id)] = cart.get(str(id),0) + 1
        session["cart"] = cart   # 🔥 FIX

        c.execute("UPDATE stock SET qty=qty-1 WHERE product_id=?",(id,))
        c.connection.commit()

    return redirect("/cart")

# ================= MIN QTY (FIX) =================
@app.route("/cart/min/<int:id>")
def cart_min(id):
    cart = session.get("cart", {})

    if str(id) in cart:
        cart[str(id)] -= 1
        if cart[str(id)] <= 0:
            del cart[str(id)]

        session["cart"] = cart   # 🔥 FIX

        c=get_db().cursor()
        c.execute("UPDATE stock SET qty=qty+1 WHERE product_id=?",(id,))
        c.connection.commit()

    return redirect("/cart")

# ================= CHECKOUT (FIX) =================
@app.route("/checkout")
def checkout():
    if not session.get("cart"):
        return redirect("/shop")

    session["cart"] = {}

    return base_html("""
    <div class=container style="text-align:center">
        <h2>✅ Checkout Berhasil</h2>
        <a class=btn href="/shop">Belanja Lagi</a>
    </div>
    """)



@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ================= RUN =================
if __name__=="__main__":
    init_db()
    app.run(debug=True)
