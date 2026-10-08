import os
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "report_assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

def get_font(size, bold=False):
    font_names = [
        "arialbd.ttf" if bold else "arial.ttf",
        "segui_bd.ttf" if bold else "segoeui.ttf",
        "calibrib.ttf" if bold else "calibri.ttf"
    ]
    for fn in font_names:
        try:
            return ImageFont.truetype(f"C:/Windows/Fonts/{fn}", size)
        except Exception:
            pass
    return ImageFont.load_default()

# ─────────────────────────────────────────────────────────────
# 1. Atmiya University Seal / Emblem (Clean Black & White / Grayscale)
# ─────────────────────────────────────────────────────────────
def generate_atmiya_logo():
    w, h = 400, 400
    img = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(img)

    # Concentric circles
    d.ellipse([10, 10, 390, 390], outline="#000000", width=6)
    d.ellipse([24, 24, 376, 376], outline="#000000", width=2)
    d.ellipse([40, 40, 360, 360], outline="#000000", width=2)
    d.ellipse([80, 80, 320, 320], outline="#000000", width=3, fill="#f8f9fa")

    # Star / Hexagram
    d.polygon([(200, 95), (300, 270), (100, 270)], outline="#000000", width=3)
    d.polygon([(200, 305), (300, 130), (100, 130)], outline="#000000", width=3)

    # Central Lotus symbol
    d.ellipse([160, 160, 240, 240], fill="#ffffff", outline="#000000", width=2)
    d.ellipse([175, 175, 225, 225], fill="#000000")

    # Text curves simulated
    f_title = get_font(22, bold=True)
    d.text((200, 52), "ATMIYA UNIVERSITY", fill="#000000", font=f_title, anchor="mm")
    f_sub = get_font(18, bold=True)
    d.text((200, 345), "॥ सुहृदं सर्वभूतानाम् ॥", fill="#000000", font=f_sub, anchor="mm")

    path = os.path.join(ASSETS_DIR, "atmiya_logo.png")
    img.save(path)
    print("Generated atmiya_logo.png (B&W)")

# ─────────────────────────────────────────────────────────────
# 2. System Architecture (Figure 5.1) - Simple, Readable Black & White
# ─────────────────────────────────────────────────────────────
def generate_architecture_diagram():
    w, h = 1200, 800
    img = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(img)
    f_title = get_font(18, bold=True)
    f_box = get_font(15, bold=True)
    f_sub = get_font(13)

    # Top: User Layer
    d.rounded_rectangle([200, 30, 1000, 110], radius=10, outline="#000000", width=2, fill="#ffffff")
    d.text((600, 55), "USERS & TRADING CLIENTS", fill="#000000", font=f_title, anchor="mm")
    d.text((600, 85), "Web Browser / Mobile Device (Retail Investors & Students)", fill="#000000", font=f_sub, anchor="mm")

    # Arrow Down
    d.line([(600, 110), (600, 160)], fill="#000000", width=2)
    d.polygon([(594, 150), (606, 150), (600, 160)], fill="#000000")
    d.text((615, 135), "HTTPS / WSS", fill="#000000", font=f_sub)

    # Presentation Layer
    d.rounded_rectangle([150, 160, 1050, 260], radius=10, outline="#000000", width=2, fill="#f8f9fa")
    d.text((600, 190), "FRONTEND PRESENTATION LAYER (React 18 & Vite)", fill="#000000", font=f_title, anchor="mm")
    d.text((600, 225), "Tailwind CSS UI  |  Redux Toolkit State  |  Chart.js Visualizations  |  Socket.io Client", fill="#000000", font=f_sub, anchor="mm")

    # Arrow Down
    d.line([(600, 260), (600, 310)], fill="#000000", width=2)
    d.polygon([(594, 300), (606, 300), (600, 310)], fill="#000000")
    d.text((615, 285), "REST API Requests & WebSocket Events", fill="#000000", font=f_sub)

    # Backend Layer
    d.rounded_rectangle([80, 310, 1120, 560], radius=10, outline="#000000", width=2, fill="#ffffff")
    d.rectangle([80, 310, 1120, 350], fill="#eeeeee", outline="#000000", width=2)
    d.text((600, 330), "BACKEND SERVER & ENGINE CONTROLLERS (Node.js & Express)", fill="#000000", font=f_title, anchor="mm")

    # Core backend modules
    modules = [
        ("Auth & Security", "JWT Authentication,\nBcrypt Hashing & Guards"),
        ("Real-Time Ticker", "Finnhub Polling &\nSocket.io Broadcasting"),
        ("Virtual Trading", "Buy/Sell Execution,\nCash Balance & PnL"),
        ("ML Predictor", "OLS 2nd-Degree Model,\nR² & MAE Projections"),
        ("Explainable AI", "Google Gemini LLM &\nGrounded Neural Fallback"),
        ("Community Forum", "Social Trading Posts,\nComments & Live Feeds")
    ]
    box_w, box_h = 150, 130
    start_x, start_y = 110, 380
    gap = 20
    for i, (m_title, m_desc) in enumerate(modules):
        bx = start_x + i * (box_w + gap)
        d.rounded_rectangle([bx, start_y, bx + box_w, start_y + box_h], radius=6, outline="#000000", width=2, fill="#ffffff")
        d.rectangle([bx, start_y, bx + box_w, start_y + 32], fill="#f0f0f0", outline="#000000", width=1)
        d.text((bx + box_w//2, start_y + 16), m_title, fill="#000000", font=get_font(13, bold=True), anchor="mm")
        d.text((bx + box_w//2, start_y + 75), m_desc, fill="#000000", font=get_font(11), anchor="mm")

    # Arrows Down to DB and External APIs
    d.line([(380, 560), (380, 620)], fill="#000000", width=2)
    d.polygon([(374, 610), (386, 610), (380, 620)], fill="#000000")

    d.line([(820, 560), (820, 620)], fill="#000000", width=2)
    d.polygon([(814, 610), (826, 610), (820, 620)], fill="#000000")

    # Bottom Left: Database
    d.rounded_rectangle([120, 620, 640, 760], radius=10, outline="#000000", width=2, fill="#f8f9fa")
    d.text((380, 645), "DATA PERSISTENCE LAYER (MongoDB)", fill="#000000", font=f_box, anchor="mm")
    d.text((380, 680), "Mongoose ODM: Users | Portfolios | Trades | Posts | Watchlists", fill="#000000", font=f_sub, anchor="mm")
    d.text((380, 715), "In-Memory Price & Prediction Cache (TTL Expirations)", fill="#000000", font=f_sub, anchor="mm")

    # Bottom Right: External APIs
    d.rounded_rectangle([680, 620, 1080, 760], radius=10, outline="#000000", width=2, fill="#f8f9fa")
    d.text((880, 645), "EXTERNAL SERVICES & AI APIS", fill="#000000", font=f_box, anchor="mm")
    d.text((880, 680), "• Finnhub API (Live Stock Quotes & Search)", fill="#000000", font=f_sub, anchor="mm")
    d.text((880, 705), "• Yahoo Finance (30-Day Historical OHLCV)", fill="#000000", font=f_sub, anchor="mm")
    d.text((880, 730), "• Google Gemini 1.5 Flash (XAI LLM Service)", fill="#000000", font=f_sub, anchor="mm")

    path = os.path.join(ASSETS_DIR, "figure_5_1_architecture.png")
    img.save(path)
    print("Generated figure_5_1_architecture.png (B&W)")

# ─────────────────────────────────────────────────────────────
# 3. Class Diagram (Figure 5.2) - Simple, Readable Black & White
# ─────────────────────────────────────────────────────────────
def generate_class_diagram():
    w, h = 1200, 750
    img = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(img)
    f_bold = get_font(13, bold=True)
    f_body = get_font(11)

    def draw_class(x, y, w_box, h_box, name, attrs, methods):
        # Outer box
        d.rectangle([x, y, x + w_box, y + h_box], outline="#000000", width=2, fill="#ffffff")
        # Header compartment
        d.rectangle([x, y, x + w_box, y + 28], fill="#eeeeee", outline="#000000", width=1)
        d.text((x + w_box//2, y + 14), name, fill="#000000", font=f_bold, anchor="mm")
        
        # Attributes compartment
        d.text((x + 8, y + 36), "\n".join(attrs), fill="#000000", font=f_body)
        mid_y = y + 34 + len(attrs)*16
        d.line([(x, mid_y), (x + w_box, mid_y)], fill="#000000", width=1)
        
        # Methods compartment
        d.text((x + 8, mid_y + 6), "\n".join(methods), fill="#000000", font=f_body)

    # User
    draw_class(40, 50, 250, 220, "User", 
               ["- _id: ObjectId", "- name: String", "- email: String", "- password: String (Hash)", "- portfolioBalance: Float", "- createdAt: Date"],
               ["+ register(): Promise", "+ login(): JWT", "+ comparePassword(): Bool", "+ updateProfile(): Void"])

    # Portfolio
    draw_class(360, 50, 250, 220, "Portfolio",
               ["- _id: ObjectId", "- userId: ObjectId", "- cashBalance: Float", "- totalInvested: Float", "- totalCurrentValue: Float", "- holdings: Array<Holding>"],
               ["+ calculatePnL(): Float", "+ executeBuy(): Bool", "+ executeSell(): Bool", "+ getSummary(): Object"])

    # Trade
    draw_class(680, 50, 250, 220, "Trade",
               ["- _id: ObjectId", "- userId: ObjectId", "- symbol: String", "- type: 'BUY' | 'SELL'", "- quantity: Integer", "- price: Float", "- totalAmount: Float"],
               ["+ recordTrade(): Void", "+ getTradeHistory(): Array", "+ validateBalance(): Bool"])

    # StockQuote
    draw_class(40, 360, 250, 230, "StockQuote",
               ["- symbol: String", "- companyName: String", "- currentPrice: Float", "- openPrice: Float", "- highPrice: Float", "- lowPrice: Float", "- changePercent: Float"],
               ["+ fetchQuote(): Object", "+ streamPriceSocket(): Void", "+ cacheBaseline(): Void"])

    # PredictionEngine (ML)
    draw_class(360, 360, 260, 240, "PredictionEngine (OLS ML)",
               ["- symbol: String", "- sampleCandles: Array", "- degree: 2", "- betaCoefficients: [b0,b1,b2]", "- r2Metric: Float", "- maeMetric: Float", "- trend: 'Bullish'|'Bearish'"],
               ["+ trainRegression(): Void", "+ solveCramersRule(): Array", "+ forecastNext5Days(): Array", "+ computeUncertaintyCone(): Obj"])

    # GenAIThesis (XAI)
    draw_class(680, 360, 260, 240, "GenAIThesis (XAI Layer)",
               ["- symbol: String", "- mlTrend: String", "- targetPrice: Float", "- summary: String", "- bullCase: Array<String>", "- bearCase: Array<String>", "- actionableVerdict: String"],
               ["+ callGeminiFlash(): JSON", "+ generateGroundedLocal(): Obj", "+ synthesizeThesis(): Memo", "+ cacheThesis(): Void"])

    # CommunityPost
    draw_class(980, 200, 190, 200, "CommunityPost",
               ["- _id: ObjectId", "- userId: ObjectId", "- authorName: String", "- content: String", "- likes: Array<Id>", "- comments: Array"],
               ["+ createPost(): Void", "+ addLike(): Void", "+ addComment(): Void"])

    # Association lines with clear text
    d.line([(290, 130), (360, 130)], fill="#000000", width=2)
    d.text((325, 115), "1..1 owns", fill="#000000", font=get_font(11, bold=True), anchor="mm")

    d.line([(610, 130), (680, 130)], fill="#000000", width=2)
    d.text((645, 115), "1..* has", fill="#000000", font=get_font(11, bold=True), anchor="mm")

    d.line([(165, 270), (165, 360)], fill="#000000", width=2)
    d.text((195, 315), "tracks", fill="#000000", font=get_font(11, bold=True), anchor="mm")

    d.line([(290, 480), (360, 480)], fill="#000000", width=2)
    d.text((325, 465), "feeds data", fill="#000000", font=get_font(11, bold=True), anchor="mm")

    d.line([(620, 480), (680, 480)], fill="#000000", width=2)
    d.text((650, 465), "explains", fill="#000000", font=get_font(11, bold=True), anchor="mm")

    d.line([(610, 180), (980, 260)], fill="#000000", width=1)
    d.text((800, 210), "interacts", fill="#000000", font=get_font(11, bold=True), anchor="mm")

    path = os.path.join(ASSETS_DIR, "figure_5_2_class.png")
    img.save(path)
    print("Generated figure_5_2_class.png (B&W)")

# ─────────────────────────────────────────────────────────────
# 4. Use Case Diagram (Figure 5.3) - Simple, Readable Black & White
# ─────────────────────────────────────────────────────────────
def generate_usecase_diagram():
    w, h = 1200, 750
    img = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(img)
    f_actor = get_font(14, bold=True)
    f_uc = get_font(12, bold=True)

    # Boundary Box
    d.rectangle([280, 30, 940, 720], outline="#000000", width=2, fill="#ffffff")
    d.text((610, 60), "StockSphere Virtual Trading System", fill="#000000", font=get_font(16, bold=True), anchor="mm")

    # Left Actor: Virtual Trader
    def draw_actor(x, y, name):
        d.ellipse([x - 20, y - 20, x + 20, y + 20], outline="#000000", width=2, fill="#ffffff")
        d.line([(x, y + 20), (x, y + 70)], fill="#000000", width=2)
        d.line([(x - 30, y + 40), (x + 30, y + 40)], fill="#000000", width=2)
        d.line([(x, y + 70), (x - 25, y + 120)], fill="#000000", width=2)
        d.line([(x, y + 70), (x + 25, y + 120)], fill="#000000", width=2)
        d.text((x, y + 140), name, fill="#000000", font=f_actor, anchor="mm")

    draw_actor(130, 270, "Virtual Trader\n(User)")
    draw_actor(1070, 360, "External AI &\nMarket APIs")

    use_cases = [
        ("Register & Login (JWT Auth)", 115),
        ("View Live Market Tickers", 180),
        ("Search Stocks & Interactive Charts", 245),
        ("Execute Virtual Buy / Sell Orders", 310),
        ("Manage Portfolio & Track PnL", 375),
        ("Run 2nd-Degree Polynomial ML Forecast", 440),
        ("Generate GenAI Investment Thesis (XAI)", 505),
        ("Manage Personalized Watchlist", 570),
        ("Post & Interact in Community Forum", 635)
    ]

    for uc_title, y_pos in use_cases:
        d.ellipse([420, y_pos - 22, 800, y_pos + 22], outline="#000000", width=2, fill="#ffffff")
        d.text((610, y_pos), uc_title, fill="#000000", font=f_uc, anchor="mm")

        # Lines from Trader
        d.line([(165, 310), (420, y_pos)], fill="#000000", width=1)

    # Lines to External Services
    d.line([(800, 180), (1030, 390)], fill="#000000", width=1)
    d.line([(800, 440), (1030, 390)], fill="#000000", width=1)
    d.line([(800, 505), (1030, 390)], fill="#000000", width=1)

    path = os.path.join(ASSETS_DIR, "figure_5_3_usecase.png")
    img.save(path)
    print("Generated figure_5_3_usecase.png (B&W)")

# ─────────────────────────────────────────────────────────────
# 5. Activity Diagram (Figure 5.4) - Simple, Readable Black & White
# ─────────────────────────────────────────────────────────────
def generate_activity_diagram():
    w, h = 1200, 650
    img = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(img)
    f_step = get_font(12, bold=True)
    f_sub = get_font(10)

    # Start Node (Solid black circle)
    d.ellipse([40, 280, 80, 320], fill="#000000")

    nodes = [
        ("User Login", "JWT Auth", 120),
        ("Search Stock", "e.g. AAPL, TSLA", 250),
        ("View Live Chart", "Price History", 380),
        ("Run ML Forecast", "OLS Regression", 510),
        ("Generate Thesis", "GenAI Bull/Bear", 640),
        ("Submit Order", "Buy/Sell Qty", 770),
    ]

    for title, desc, x in nodes:
        d.rounded_rectangle([x, 260, x + 105, 340], radius=8, outline="#000000", width=2, fill="#ffffff")
        d.text((x + 52, 285), title, fill="#000000", font=f_step, anchor="mm")
        d.text((x + 52, 315), desc, fill="#000000", font=f_sub, anchor="mm")

        # Arrow forward
        prev_x = 80 if x == 120 else (x - 25)
        d.line([(prev_x, 300), (x, 300)], fill="#000000", width=2)
        d.polygon([(x, 300), (x - 7, 295), (x - 7, 305)], fill="#000000")

    # Arrow to Decision Diamond
    d.line([(875, 300), (920, 300)], fill="#000000", width=2)
    d.polygon([(920, 300), (913, 295), (913, 305)], fill="#000000")

    # Decision Diamond: Balance Check
    d.polygon([(920, 300), (960, 260), (1000, 300), (960, 340)], outline="#000000", width=2, fill="#ffffff")
    d.text((960, 300), "Valid?", fill="#000000", font=get_font(11, bold=True), anchor="mm")

    # Yes branch -> Execution box
    d.line([(1000, 300), (1040, 300)], fill="#000000", width=2)
    d.polygon([(1040, 300), (1033, 295), (1033, 305)], fill="#000000")
    d.text((1018, 288), "Yes", fill="#000000", font=get_font(10, bold=True), anchor="mm")

    d.rounded_rectangle([1040, 260, 1145, 340], radius=8, outline="#000000", width=2, fill="#ffffff")
    d.text((1092, 285), "Execute Trade", fill="#000000", font=f_step, anchor="mm")
    d.text((1092, 315), "Update Portfolio", fill="#000000", font=f_sub, anchor="mm")

    # Arrow from Execution to Final End Node
    d.line([(1092, 340), (1092, 420)], fill="#000000", width=2)
    d.polygon([(1092, 420), (1087, 413), (1097, 413)], fill="#000000")

    # No branch (Rejected)
    d.line([(960, 340), (960, 420)], fill="#000000", width=2)
    d.polygon([(960, 420), (955, 413), (965, 413)], fill="#000000")
    d.text((975, 370), "No", fill="#000000", font=get_font(10, bold=True))

    d.rounded_rectangle([910, 420, 1010, 480], radius=6, outline="#000000", width=2, fill="#ffffff")
    d.text((960, 442), "Order Rejected", fill="#000000", font=get_font(11, bold=True), anchor="mm")
    d.text((960, 462), "Low Balance", fill="#000000", font=f_sub, anchor="mm")

    # End Node (Bullseye)
    d.ellipse([1072, 420, 1112, 460], outline="#000000", width=2, fill="#ffffff")
    d.ellipse([1080, 428, 1104, 452], fill="#000000")
    d.text((1092, 475), "Completed", fill="#000000", font=get_font(11, bold=True), anchor="mm")

    path = os.path.join(ASSETS_DIR, "figure_5_4_activity.png")
    img.save(path)
    print("Generated figure_5_4_activity.png (B&W)")

# ─────────────────────────────────────────────────────────────
# 6. DFD Level 0 (Figure 5.5) - Simple, Readable Black & White
# ─────────────────────────────────────────────────────────────
def generate_dfd_diagram():
    w, h = 1200, 700
    img = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(img)
    f_box = get_font(13, bold=True)
    f_line = get_font(11)

    # Central Process Circle
    d.ellipse([430, 220, 770, 460], outline="#000000", width=3, fill="#ffffff")
    d.text((600, 320), "0.0 StockSphere System", fill="#000000", font=get_font(16, bold=True), anchor="mm")
    d.text((600, 355), "Virtual Stock Trading &\nAI Market Forecasting Platform", fill="#000000", font=get_font(13), anchor="mm")

    # Entities (Rectangles)
    # User / Trader
    d.rectangle([50, 280, 220, 400], outline="#000000", width=2, fill="#ffffff")
    d.text((135, 340), "Virtual Trader\n(User)", fill="#000000", font=f_box, anchor="mm")

    # Finnhub API
    d.rectangle([980, 80, 1150, 180], outline="#000000", width=2, fill="#ffffff")
    d.text((1065, 130), "Finnhub API\n(Live Quotes)", fill="#000000", font=f_box, anchor="mm")

    # Yahoo Finance API
    d.rectangle([980, 270, 1150, 370], outline="#000000", width=2, fill="#ffffff")
    d.text((1065, 320), "Yahoo Finance API\n(30-Day Candles)", fill="#000000", font=f_box, anchor="mm")

    # Google Gemini AI
    d.rectangle([980, 460, 1150, 560], outline="#000000", width=2, fill="#ffffff")
    d.text((1065, 510), "Google Gemini AI\n(XAI LLM API)", fill="#000000", font=f_box, anchor="mm")

    # Data stores (Parallel open lines at bottom)
    stores = [
        ("D1: Users & Auth", 300, 580),
        ("D2: Portfolios & Holdings", 510, 580),
        ("D3: Trades History", 720, 580),
        ("D4: Watchlists & Community", 930, 580)
    ]
    for s_name, sx, sy in stores:
        d.line([(sx, sy), (sx + 180, sy)], fill="#000000", width=2)
        d.line([(sx, sy + 38), (sx + 180, sy + 38)], fill="#000000")
        d.text((sx + 90, sy + 19), s_name, fill="#000000", font=get_font(11, bold=True), anchor="mm")

    # Arrows between User and System
    d.line([(220, 320), (430, 320)], fill="#000000", width=2)
    d.polygon([(430, 320), (423, 315), (423, 325)], fill="#000000")
    d.text((325, 305), "Orders, Symbol Searches", fill="#000000", font=f_line, anchor="mm")

    d.line([(430, 370), (220, 370)], fill="#000000", width=2)
    d.polygon([(220, 370), (227, 365), (227, 375)], fill="#000000")
    d.text((325, 385), "Live Tickers, PnL, AI Memos", fill="#000000", font=f_line, anchor="mm")

    # Arrows to External Services
    d.line([(730, 260), (980, 150)], fill="#000000", width=2)
    d.polygon([(980, 150), (972, 146), (975, 156)], fill="#000000")
    d.text((850, 190), "Price Quotes", fill="#000000", font=f_line, anchor="mm")

    d.line([(770, 340), (980, 320)], fill="#000000", width=2)
    d.polygon([(980, 320), (972, 316), (974, 326)], fill="#000000")
    d.text((875, 315), "Candle Data", fill="#000000", font=f_line, anchor="mm")

    d.line([(730, 420), (980, 490)], fill="#000000", width=2)
    d.polygon([(980, 490), (974, 483), (972, 493)], fill="#000000")
    d.text((855, 445), "ML Metrics -> AI Thesis", fill="#000000", font=f_line, anchor="mm")

    # Arrows to Data Stores
    d.line([(600, 460), (600, 580)], fill="#000000", width=2)
    d.polygon([(600, 580), (595, 573), (605, 573)], fill="#000000")
    d.text((615, 520), "CRUD Queries", fill="#000000", font=f_line)

    path = os.path.join(ASSETS_DIR, "figure_5_5_dfd.png")
    img.save(path)
    print("Generated figure_5_5_dfd.png (B&W)")

# ─────────────────────────────────────────────────────────────
# 7. State Diagram (Figure 5.6) - Simple, Readable Black & White
# ─────────────────────────────────────────────────────────────
def generate_state_diagram():
    w, h = 1200, 550
    img = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(img)
    f_state = get_font(13, bold=True)
    f_sub = get_font(10)
    f_lbl = get_font(11, bold=True)

    # Initial State (Solid black dot)
    d.ellipse([50, 200, 90, 240], fill="#000000")

    states = [
        ("Trade Initiated", "User enters symbol & qty", 150),
        ("Validating Funds", "Check cash & share limits", 380),
        ("Execution Engine", "Match price & compute total", 610),
        ("Position Active", "Holdings & balance updated", 840),
    ]

    for title, desc, x in states:
        d.rounded_rectangle([x, 180, x + 160, 260], radius=8, outline="#000000", width=2, fill="#ffffff")
        d.text((x + 80, 205), title, fill="#000000", font=f_state, anchor="mm")
        d.text((x + 80, 235), desc, fill="#000000", font=f_sub, anchor="mm")

    # Connect forward states
    d.line([(90, 220), (150, 220)], fill="#000000", width=2)
    d.polygon([(150, 220), (143, 215), (143, 225)], fill="#000000")

    d.line([(310, 220), (380, 220)], fill="#000000", width=2)
    d.polygon([(380, 220), (373, 215), (373, 225)], fill="#000000")
    d.text((345, 205), "Submit", fill="#000000", font=get_font(10))

    d.line([(540, 220), (610, 220)], fill="#000000", width=2)
    d.polygon([(610, 220), (603, 215), (603, 225)], fill="#000000")
    d.text((575, 205), "Valid", fill="#000000", font=get_font(10, bold=True))

    d.line([(770, 220), (840, 220)], fill="#000000", width=2)
    d.polygon([(840, 220), (833, 215), (833, 225)], fill="#000000")
    d.text((805, 205), "Success", fill="#000000", font=get_font(10))

    # Rejection State (Under Validating Funds)
    d.rounded_rectangle([380, 360, 540, 440], radius=8, outline="#000000", width=2, fill="#ffffff")
    d.text((460, 385), "Order Rejected", fill="#000000", font=f_state, anchor="mm")
    d.text((460, 415), "Insufficient Cash", fill="#000000", font=f_sub, anchor="mm")

    d.line([(460, 260), (460, 360)], fill="#000000", width=2)
    d.polygon([(460, 360), (455, 353), (465, 353)], fill="#000000")
    d.text((525, 310), "Invalid / Low Funds", fill="#000000", font=f_lbl, anchor="mm")

    # Final State from Active
    d.ellipse([1070, 200, 1110, 240], outline="#000000", width=2, fill="#ffffff")
    d.ellipse([1078, 208, 1102, 232], fill="#000000")
    d.line([(1000, 220), (1070, 220)], fill="#000000", width=2)
    d.polygon([(1070, 220), (1063, 215), (1063, 225)], fill="#000000")
    d.text((1035, 205), "Closed", fill="#000000", font=get_font(10))

    path = os.path.join(ASSETS_DIR, "figure_5_6_state.png")
    img.save(path)
    print("Generated figure_5_6_state.png (B&W)")

# ─────────────────────────────────────────────────────────────
# 8. Entity Relationship Diagram (Figure 5.7) - Simple, Readable Black & White
# ─────────────────────────────────────────────────────────────
def generate_er_diagram():
    w, h = 1200, 750
    img = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(img)
    f_tbl = get_font(13, bold=True)
    f_fld = get_font(11)

    def draw_entity(x, y, title, fields):
        w_box, h_box = 210, 30 + len(fields)*22
        d.rectangle([x, y, x + w_box, y + h_box], outline="#000000", width=2, fill="#ffffff")
        d.rectangle([x, y, x + w_box, y + 26], fill="#eeeeee", outline="#000000", width=1)
        d.text((x + w_box//2, y + 13), title, fill="#000000", font=f_tbl, anchor="mm")
        for i, (pk, fn) in enumerate(fields):
            d.text((x + 8, y + 36 + i*22), f"{pk:2}  {fn}", fill="#000000", font=f_fld)

    # USER
    draw_entity(70, 80, "USER", [
        ("PK", "_id (ObjectId)"),
        ("  ", "name (String)"),
        ("  ", "email (String, Unique)"),
        ("  ", "password (String, Hashed)"),
        ("  ", "portfolioBalance (Float)"),
        ("  ", "createdAt (Date)")
    ])

    # PORTFOLIO
    draw_entity(480, 80, "PORTFOLIO", [
        ("PK", "_id (ObjectId)"),
        ("FK", "userId (Ref: User)"),
        ("  ", "cashBalance (Float)"),
        ("  ", "totalInvested (Float)"),
        ("  ", "updatedAt (Date)")
    ])

    # HOLDING (Subdocument)
    draw_entity(890, 80, "HOLDING", [
        ("PK", "_id (ObjectId)"),
        ("FK", "portfolioId (Ref: Portfolio)"),
        ("  ", "symbol (String)"),
        ("  ", "quantity (Integer)"),
        ("  ", "averageBuyPrice (Float)"),
        ("  ", "totalCost (Float)")
    ])

    # TRADE
    draw_entity(480, 380, "TRADE", [
        ("PK", "_id (ObjectId)"),
        ("FK", "userId (Ref: User)"),
        ("  ", "symbol (String)"),
        ("  ", "type ('BUY' | 'SELL')"),
        ("  ", "quantity (Integer)"),
        ("  ", "executedPrice (Float)"),
        ("  ", "totalAmount (Float)"),
        ("  ", "executedAt (Date)")
    ])

    # WATCHLIST
    draw_entity(70, 380, "WATCHLIST", [
        ("PK", "_id (ObjectId)"),
        ("FK", "userId (Ref: User)"),
        ("  ", "symbol (String)"),
        ("  ", "addedAt (Date)")
    ])

    # COMMUNITY POST
    draw_entity(890, 380, "POST", [
        ("PK", "_id (ObjectId)"),
        ("FK", "userId (Ref: User)"),
        ("  ", "authorName (String)"),
        ("  ", "content (String)"),
        ("  ", "likesCount (Integer)"),
        ("  ", "createdAt (Date)")
    ])

    # Relationship connection lines
    d.line([(280, 150), (480, 150)], fill="#000000", width=2)
    d.text((380, 135), "1 : 1 owns", fill="#000000", font=get_font(11, bold=True), anchor="mm")

    d.line([(690, 150), (890, 150)], fill="#000000", width=2)
    d.text((790, 135), "1 : N contains", fill="#000000", font=get_font(11, bold=True), anchor="mm")

    d.line([(175, 240), (175, 380)], fill="#000000", width=2)
    d.text((215, 310), "1 : N keeps", fill="#000000", font=get_font(11, bold=True), anchor="mm")

    d.line([(585, 220), (585, 380)], fill="#000000", width=2)
    d.text((630, 300), "1 : N records", fill="#000000", font=get_font(11, bold=True), anchor="mm")

    path = os.path.join(ASSETS_DIR, "figure_5_7_er.png")
    img.save(path)
    print("Generated figure_5_7_er.png (B&W)")

# ─────────────────────────────────────────────────────────────
# 9. Sequence Diagram (Figure 5.8) - Simple, Readable Black & White
# ─────────────────────────────────────────────────────────────
def generate_sequence_diagram():
    w, h = 1200, 750
    img = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(img)
    f_lifeline = get_font(13, bold=True)
    f_msg = get_font(11)

    lifelines = [
        ("Trader (Browser)", 140),
        ("React Client", 370),
        ("Express REST API", 600),
        ("Yahoo & ML Model", 830),
        ("Gemini AI / DB", 1060)
    ]

    for name, x in lifelines:
        d.rectangle([x - 75, 40, x + 75, 80], outline="#000000", width=2, fill="#ffffff")
        d.text((x, 60), name, fill="#000000", font=f_lifeline, anchor="mm")
        # Dashed lifeline
        for ly in range(80, 710, 12):
            d.line([(x, ly), (x, ly + 6)], fill="#666666", width=1)

    steps = [
        (120, 140, 370, "1. Click 'AI Predictor' (AAPL)", False),
        (170, 370, 600, "2. GET /api/stocks/predict/AAPL", False),
        (220, 600, 830, "3. Fetch 30-Day Candles & Train OLS Model", False),
        (280, 830, 600, "4. Return R²=88%, MAE=$3.04, Trend=Bullish", True),
        (340, 600, 370, "5. Render Forecast Curve & Confidence Band", True),
        (400, 140, 370, "6. Click 'Generate AI Thesis'", False),
        (450, 370, 600, "7. GET /api/stocks/thesis/AAPL", False),
        (510, 600, 1060, "8. Pass ML Metrics to Gemini LLM / Neural Engine", False),
        (570, 1060, 600, "9. Return Structured Bull/Bear Thesis Memo", True),
        (620, 600, 370, "10. Render Executive Summary & Catalysts", True),
        (660, 370, 140, "11. Display Actionable Virtual Trading Guidance", True)
    ]

    for y, x1, x2, msg, is_return in steps:
        d.line([(x1, y), (x2, y)], fill="#000000", width=2)
        if x2 > x1:
            d.polygon([(x2, y), (x2 - 8, y - 5), (x2 - 8, y + 5)], fill="#000000")
        else:
            d.polygon([(x2, y), (x2 + 8, y - 5), (x2 + 8, y + 5)], fill="#000000")
        d.text(((x1 + x2)//2, y - 10), msg, fill="#000000", font=f_msg, anchor="mm")

    path = os.path.join(ASSETS_DIR, "figure_5_8_sequence.png")
    img.save(path)
    print("Generated figure_5_8_sequence.png (B&W)")

if __name__ == "__main__":
    generate_atmiya_logo()
    generate_architecture_diagram()
    generate_class_diagram()
    generate_usecase_diagram()
    generate_activity_diagram()
    generate_dfd_diagram()
    generate_state_diagram()
    generate_er_diagram()
    generate_sequence_diagram()
    print("All 9 diagrams generated successfully in clean, simple Black & White format in report_assets/!")
