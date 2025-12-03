from flask import Flask, request, render_template_string
import hashlib

app = Flask(__name__)

# MD5 hash of actual flag: flag{multi_shift_caesar_is_fun}
FLAG_HASH = "9bf0e0d947df2f6edf004d32f5cefdba"

# Final ciphertext after Caesar → XOR("k3y") → Base64
# (This should match your current design; adjust if you change the flag or layers)
CIPHERTEXT = "AlwdAUgLEUIABWwKA1UVEmwVAV0bAVImAkkaNEMcB1AeCU4="

# -------------------------- PAGE 1 --------------------------
PAGE_INTRO = r"""
<!doctype html>
<html>
<head>
<title>The Three-Layer Cipher – Prelude</title>
<style>
body { background:#111; color:#eee; font-family:sans-serif; text-align:center; padding-top:80px; }
.card { background:#1c1c1c; padding:30px 40px; display:inline-block; border-radius:10px;
        box-shadow:0 0 15px #000; max-width:650px; }
button { background:#ff9800; padding:10px 20px; border-radius:6px; border:none; cursor:pointer; margin-top:20px; }
</style>
</head>
<body>
<div class="card">
    <h2>The Three-Layer Cipher</h2>
    <p>You discovered a mysterious encrypted artifact.</p>
    <p>The scribbles mention <i>"layers upon layers upon layers…"</i></p>

    

    <p><i>"No single transformation stands alone."</i></p>

    <form action="/clues">
        <button type="submit">Continue →</button>
    </form>
</div>
</body>
</html>
"""

# -------------------------- PAGE 2 --------------------------
PAGE_CLUES = r"""
<!doctype html>
<html>
<head>
<title>Clue Chamber</title>
<style>
body { background:#111; color:#eee; font-family:sans-serif; text-align:center; padding-top:60px; }
.card { background:#1c1c1c; padding:30px 40px; border-radius:10px; display:inline-block;
        box-shadow:0 0 15px #000; max-width:650px; }
button { background:#03a9f4; padding:10px 20px; border:none; border-radius:6px; cursor:pointer; margin-top:20px; }
.hint { color:#bbb; margin-top:10px; }
</style>
</head>
<body>

<!-- REAL HINT: Final order = Base64 decode → XOR with 'k3y' → reverse per-word Caesar shifts -->
<!-- XOR key = "k3y" -->

<div class="card">
    <h2>Clue Chamber</h2>

    <p class="hint">Clue #1: "The final layer is readable by all machines."</p>
    <p class="hint">Clue #2: "Before that lies a reversible byte dance with a simple partner."</p>
    <p class="hint"><b>Clue #3: "And at the core, ancient shifts guide each word differently."</b></p>

    <form action="/challenge">
        <button type="submit">Proceed to Cipher →</button>
    </form>
</div>

</body>
</html>
"""

# -------------------------- PAGE 3 --------------------------
PAGE_CHALLENGE = r"""
<!doctype html>
<html>
<head>
<title>Layered Crypto Challenge</title>
<style>
body { background:#111; color:#eee; font-family:sans-serif; text-align:center; padding-top:70px; }
.card { background:#1c1c1c; padding:30px 40px; border-radius:10px; display:inline-block; 
        box-shadow:0 0 15px #000; max-width:700px; }
code { background:#222; padding:10px; border-radius:6px; display:block; margin-top:10px; 
       font-size:0.9rem; word-break:break-all; }
button { background:#4caf50; padding:10px 20px; border:none; border-radius:6px; cursor:pointer; margin-top:20px; }
input { width:90%; padding:10px; margin-top:15px; border-radius:6px; border:1px solid #444; 
        background:#111; color:#eee; }
.msg.ok { color:#4caf50; font-weight:bolder; margin-top:10px; }
.msg.err { color:#e91e63; font-weight:bolder; margin-top:10px; }
</style>
</head>
<body>
<div class="card">
    <h2>The Final Cipher</h2>
    <!-- XOR key = "k3y" -->

    <code>{{ ciphertext }}</code>

    <p><i>"Three guardians protect this secret. Unmask them in reverse order."</i></p>

    <form method="POST">
        <input type="text" name="flag" placeholder="flag{...}">
        <button type="submit">Submit Flag</button>
    </form>

    {% if message %}
        <div class="msg {{ css_class }}">{{ message }}</div>
    {% endif %}
</div>
</body>
</html>
"""

# -------------------------- ROUTES --------------------------
@app.route("/")
def intro():
    return render_template_string(PAGE_INTRO)

@app.route("/clues")
def clues():
    return render_template_string(PAGE_CLUES)

@app.route("/challenge", methods=["GET", "POST"])
def challenge():
    message = ""
    css_class = ""

    if request.method == "POST":
        guess = request.form.get("flag", "").strip()
        guess_hash = hashlib.md5(guess.encode()).hexdigest()

        if guess_hash == FLAG_HASH:
            message = "🎉 Correct! You have removed all three layers."
            css_class = "ok"
        else:
            message = "❌ Incorrect. Think in reverse: Base64 → XOR → Caesar."
            css_class = "err"

    return render_template_string(
        PAGE_CHALLENGE,
        ciphertext=CIPHERTEXT,
        message=message,
        css_class=css_class
    )

# Vercel requires the app to be exported
handler = app
