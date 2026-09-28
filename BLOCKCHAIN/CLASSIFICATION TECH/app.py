import math
import random
import string
from collections import Counter

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split


st.set_page_config(
    page_title="CipherLens | Classification Techniques",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)


# -----------------------------
# Cipher utilities
# -----------------------------
def normalize(text):
    return "".join(char for char in text.upper() if char in string.ascii_uppercase)


def caesar_encrypt(text, shift):
    result = []
    for char in text.upper():
        if char in string.ascii_uppercase:
            result.append(chr((ord(char) - 65 + shift) % 26 + 65))
        else:
            result.append(char)
    return "".join(result)


def vigenere_encrypt(text, key):
    key = normalize(key) or "KEY"
    result = []
    key_index = 0
    for char in text.upper():
        if char in string.ascii_uppercase:
            shift = ord(key[key_index % len(key)]) - 65
            result.append(chr((ord(char) - 65 + shift) % 26 + 65))
            key_index += 1
        else:
            result.append(char)
    return "".join(result)


def rail_fence_encrypt(text, rails):
    clean = normalize(text)
    if rails <= 1 or rails >= len(clean):
        return clean
    rows = [[] for _ in range(rails)]
    row, direction = 0, 1
    for char in clean:
        rows[row].append(char)
        if row == 0:
            direction = 1
        elif row == rails - 1:
            direction = -1
        row += direction
    return "".join("".join(line) for line in rows)


def columnar_encrypt(text, keyword):
    clean = normalize(text)
    keyword = normalize(keyword) or "ZEBRA"
    width = len(keyword)
    padded = clean + "X" * ((width - len(clean) % width) % width)
    order = sorted(range(width), key=lambda index: (keyword[index], index))
    grid = [padded[index:index + width] for index in range(0, len(padded), width)]
    return "".join("".join(row[index] for row in grid) for index in order)


def rail_fence_decrypt(text, rails):
    clean = normalize(text)
    if rails <= 1 or rails >= len(clean):
        return clean
    pattern = list(range(rails)) + list(range(rails - 2, 0, -1))
    rail_numbers = [pattern[index % len(pattern)] for index in range(len(clean))]
    counts = [rail_numbers.count(rail) for rail in range(rails)]
    rows, cursor = [], 0
    for count in counts:
        rows.append(list(clean[cursor:cursor + count]))
        cursor += count
    return "".join(rows[rail].pop(0) for rail in rail_numbers)


def columnar_decrypt(text, keyword):
    clean = normalize(text)
    keyword = normalize(keyword) or "ZEBRA"
    width = len(keyword)
    row_count = math.ceil(len(clean) / width)
    order = sorted(range(width), key=lambda index: (keyword[index], index))
    rows = [[""] * width for _ in range(row_count)]
    cursor = 0
    for column in order:
        for row in range(row_count):
            if cursor < len(clean):
                rows[row][column] = clean[cursor]
                cursor += 1
    return "".join("".join(row) for row in rows).rstrip("X")


def atbash_encrypt(text):
    return "".join(chr(155 - ord(char)) if char in string.ascii_uppercase else char for char in text.upper())


def monoalphabetic_encrypt(text, key):
    alphabet = string.ascii_uppercase
    mapping = normalize(key)
    if len(mapping) != 26 or len(set(mapping)) != 26:
        mapping = "QWERTYUIOPASDFGHJKLZXCVBNM"
    table = str.maketrans(alphabet, mapping)
    return text.upper().translate(table), mapping


def monoalphabetic_decrypt(text, key):
    alphabet = string.ascii_uppercase
    _, mapping = monoalphabetic_encrypt("", key)
    table = str.maketrans(mapping, alphabet)
    return text.upper().translate(table)


def homophonic_encrypt(text):
    codes = {
        "A": ["11", "41"], "E": ["15", "51"], "I": ["19", "91"], "O": ["20", "02"],
        "T": ["30", "03"], "N": ["31"], "R": ["32"], "S": ["33"], "L": ["34"],
    }
    result = []
    for char in normalize(text):
        if char in codes:
            result.append(codes[char][0])
        else:
            result.append(f"{ord(char) - 55:02d}")
    return " ".join(result)


def homophonic_decrypt(text):
    reverse = {"11": "A", "15": "E", "19": "I", "20": "O", "30": "T", "31": "N", "32": "R", "33": "S", "34": "L"}
    return "".join(reverse.get(token, chr(int(token) + 55) if token.isdigit() and 65 <= int(token) + 55 <= 90 else "?") for token in text.split())


def playfair_encrypt(text, key):
    key = normalize(key) or "MONARCHY"
    sequence = []
    for char in key + string.ascii_uppercase:
        char = "I" if char == "J" else char
        if char not in sequence:
            sequence.append(char)
    square = [sequence[index:index + 5] for index in range(0, 25, 5)]
    positions = {char: (row, column) for row, line in enumerate(square) for column, char in enumerate(line)}
    clean = normalize(text).replace("J", "I")
    pairs, index = [], 0
    while index < len(clean):
        first = clean[index]
        second = clean[index + 1] if index + 1 < len(clean) and clean[index + 1] != first else "X"
        pairs.append((first, second))
        index += 1 if second == "X" and index + 1 < len(clean) and clean[index + 1] == first else 2
    if pairs and len(pairs[-1][1]) == 0:
        pairs[-1] = (pairs[-1][0], "X")
    encrypted = []
    for first, second in pairs:
        row_a, col_a = positions[first]
        row_b, col_b = positions[second]
        if row_a == row_b:
            encrypted.extend([square[row_a][(col_a + 1) % 5], square[row_b][(col_b + 1) % 5]])
        elif col_a == col_b:
            encrypted.extend([square[(row_a + 1) % 5][col_a], square[(row_b + 1) % 5][col_b]])
        else:
            encrypted.extend([square[row_a][col_b], square[row_b][col_a]])
    return "".join(encrypted), [" ".join(line) for line in square]


def playfair_decrypt(text, key):
    encrypted, square_text = playfair_encrypt("", key)
    square = [line.split() for line in square_text]
    positions = {char: (row, column) for row, line in enumerate(square) for column, char in enumerate(line)}
    clean = normalize(text).replace("J", "I")
    decrypted = []
    for index in range(0, len(clean), 2):
        first, second = clean[index:index + 2]
        if len(second) != 1:
            break
        row_a, col_a = positions[first]
        row_b, col_b = positions[second]
        if row_a == row_b:
            decrypted.extend([square[row_a][(col_a - 1) % 5], square[row_b][(col_b - 1) % 5]])
        elif col_a == col_b:
            decrypted.extend([square[(row_a - 1) % 5][col_a], square[(row_b - 1) % 5][col_b]])
        else:
            decrypted.extend([square[row_a][col_b], square[row_b][col_a]])
    return "".join(decrypted).rstrip("X"), square_text


def double_transposition_encrypt(text, keyword):
    first = columnar_encrypt(text, keyword)
    return columnar_encrypt(first, keyword), first


def double_transposition_decrypt(text, keyword):
    first = columnar_decrypt(text, keyword)
    return columnar_decrypt(first, keyword), first


def alphabet_table(mapping=None, position_note="Characters keep their own identity"):
    alphabet = list(string.ascii_uppercase)
    if mapping is None:
        mapping = alphabet
    return pd.DataFrame({
        "Plain A-Z": alphabet,
        "Position": list(range(1, 27)),
        "Cipher / result": mapping,
        "What to notice": [position_note] * 26,
    })


PLAIN_TEXTS = [
    "MEET ME AFTER CLASS",
    "THE NETWORK NEEDS PROTECTION",
    "SEND THE FILE BEFORE NOON",
    "CRYPTOGRAPHY BUILDS TRUST",
    "ALICE SENDS A MESSAGE TO BOB",
    "LEARN THE KEY THEN READ THE TEXT",
    "KEEP YOUR PASSWORD PRIVATE",
    "SECURE SYSTEMS VERIFY EVERY MESSAGE",
    "THE EXAM STARTS AT TEN",
    "DATA SHOULD BE PROTECTED IN TRANSIT",
    "A GOOD KEY MAKES A CIPHER HARDER TO GUESS",
    "PRACTICE MAKES CRYPTOGRAPHY CLEAR",
]


def feature_names():
    return [
        "length", "unique_ratio", "entropy", "index_coincidence",
        "common_bigram_rate", "repeat_rate", "vowel_ratio", "letter_balance",
    ]


def extract_features(text):
    clean = normalize(text)
    if not clean:
        return np.zeros(len(feature_names()))
    counts = Counter(clean)
    length = len(clean)
    probabilities = [count / length for count in counts.values()]
    entropy = -sum(probability * math.log2(probability) for probability in probabilities)
    coincidence = sum(count * (count - 1) for count in counts.values()) / max(length * (length - 1), 1)
    common_bigrams = {"TH", "HE", "IN", "ER", "AN", "RE", "ON", "AT", "EN", "ND"}
    bigrams = [clean[index:index + 2] for index in range(length - 1)]
    common_bigram_rate = sum(pair in common_bigrams for pair in bigrams) / max(len(bigrams), 1)
    repeat_rate = 1 - len(set(bigrams)) / max(len(bigrams), 1)
    vowel_ratio = sum(char in "AEIOU" for char in clean) / length
    expected = np.array([0.082, 0.015, 0.028, 0.043, 0.127, 0.022, 0.02, 0.061, 0.07, 0.0015,
                         0.0077, 0.04, 0.024, 0.067, 0.075, 0.019, 0.001, 0.06, 0.063, 0.091,
                         0.028, 0.01, 0.024, 0.0024, 0.02, 0.0007])
    observed = np.array([counts.get(chr(65 + index), 0) / length for index in range(26)])
    letter_balance = float(np.mean(np.abs(observed - expected)))
    return np.array([length, len(counts) / 26, entropy, coincidence, common_bigram_rate,
                     repeat_rate, vowel_ratio, letter_balance])


def build_dataset(seed=7):
    randomizer = random.Random(seed)
    rows = []
    for plaintext in PLAIN_TEXTS:
        for _ in range(18):
            caesar = caesar_encrypt(plaintext, randomizer.randint(1, 25))
            atbash = atbash_encrypt(plaintext)
            monoalphabetic, _ = monoalphabetic_encrypt(plaintext, "QWERTYUIOPASDFGHJKLZXCVBNM")
            homophonic = homophonic_encrypt(plaintext)
            playfair, _ = playfair_encrypt(plaintext, "MONARCHY")
            vigenere = vigenere_encrypt(plaintext, randomizer.choice(["KEY", "LEMON", "CIPHER", "CODE"]))
            rail = rail_fence_encrypt(plaintext, randomizer.choice([2, 3, 4]))
            columnar = columnar_encrypt(plaintext, randomizer.choice(["ZEBRA", "CIPHER", "TRAIN"]))
            double_transposition, _ = double_transposition_encrypt(plaintext, "ZEBRA")
            combined = columnar_encrypt(caesar, "ZEBRA")
            rows.extend([
                {"text": caesar, "label": "Substitution", "technique": "Caesar"},
                {"text": atbash, "label": "Substitution", "technique": "Atbash"},
                {"text": monoalphabetic, "label": "Substitution", "technique": "Monoalphabetic"},
                {"text": homophonic, "label": "Substitution", "technique": "Homophonic"},
                {"text": playfair, "label": "Substitution", "technique": "Playfair"},
                {"text": vigenere, "label": "Substitution", "technique": "Vigenere"},
                {"text": rail, "label": "Transposition", "technique": "Rail Fence"},
                {"text": columnar, "label": "Transposition", "technique": "Columnar"},
                {"text": double_transposition, "label": "Transposition", "technique": "Double Transposition"},
                {"text": combined, "label": "Substitution", "technique": "Combined substitution + transposition"},
            ])
    frame = pd.DataFrame(rows)
    features = np.vstack(frame["text"].map(extract_features))
    return frame, features


@st.cache_resource
def train_model():
    frame, features = build_dataset()
    x_train, x_test, y_train, y_test = train_test_split(
        features, frame["label"], test_size=0.25, random_state=42, stratify=frame["label"]
    )
    model = RandomForestClassifier(n_estimators=180, max_depth=8, random_state=42)
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    return model, frame, accuracy_score(y_test, predictions), confusion_matrix(
        y_test, predictions, labels=["Substitution", "Transposition"]
    )


@st.cache_resource
def train_technique_model():
    frame, features = build_dataset()
    x_train, x_test, y_train, y_test = train_test_split(
        features, frame["technique"], test_size=0.25, random_state=42, stratify=frame["technique"]
    )
    model = RandomForestClassifier(n_estimators=220, max_depth=10, random_state=42)
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    return model, accuracy_score(y_test, predictions)


# -----------------------------
# Visual language
# -----------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    :root { --ink:#102a43; --muted:#627d98; --teal:#007c83; --mint:#d9f0eb; --gold:#f4b942; --paper:#f7fafc; }
    .stApp { background: radial-gradient(circle at 85% 4%, #e9f7f3 0, #f7fafc 35%, #ffffff 80%); color:var(--ink); }
    html, body, [class*="css"] { font-family:'Space Grotesk', sans-serif; font-weight:500; }
    h1, h2, h3, h4 { color:var(--ink); letter-spacing:0; font-weight:700; }
    h1 { font-size: clamp(2.2rem, 5vw, 4.6rem); line-height:1.02; text-shadow:0 2px 0 rgba(255,255,255,.7); }
    h2 { font-size:2.15rem; line-height:1.1; }
    h3 { font-size:1.25rem; }
    h4 { font-size:1.05rem; }
    p, li, label, [data-testid="stCaptionContainer"] { color:#334e68; font-weight:500; }
    strong, b { color:var(--ink); font-weight:700; }
    .eyebrow { color:var(--teal); font-family:'DM Mono', monospace; font-size:.78rem; font-weight:700; letter-spacing:.14em; text-transform:uppercase; }
    .hero { padding:2.5rem 0 1.25rem; border-bottom:1px solid #d9e2ec; }
    .hero p { color:var(--muted); max-width:760px; font-size:1.05rem; }
    .panel { background:rgba(255,255,255,.85); border:1px solid #d9e2ec; border-radius:8px; padding:1.25rem; height:100%; box-shadow:0 8px 30px rgba(16,42,67,.05); }
    .metric { font-family:'DM Mono', monospace; color:var(--teal); font-size:1.9rem; font-weight:700; }
    .label { color:var(--teal); text-transform:uppercase; font-size:.74rem; font-weight:700; letter-spacing:.1em; }
    .flow { display:flex; align-items:center; justify-content:center; gap:.5rem; flex-wrap:wrap; margin:1rem 0; }
    .flow span { background:#e9f7f3; border:2px solid #82cfc3; padding:.7rem 1rem; border-radius:5px; font-family:'DM Mono', monospace; color:var(--ink); font-weight:700; }
    .flow b { color:#c27b00; font-size:1.35rem; font-weight:700; }
    .callout { border-left:5px solid var(--gold); background:#fff8e6; padding:.9rem 1.1rem; margin:.8rem 0; color:#334e68; font-weight:500; }
    .code-line { font-family:'DM Mono', monospace; background:#102a43; color:#d9f0eb; padding:1rem; border-radius:5px; overflow:auto; font-weight:700; font-size:1.05rem; }
    div[data-testid="stButton"] button { border:2px solid var(--teal); border-radius:5px; font-weight:700; letter-spacing:.01em; }
    div[data-testid="stButton"] button[kind="primary"] { background:var(--teal); color:#ffffff; box-shadow:0 4px 0 #005b60; }
    div[data-testid="stButton"] button:hover { border-color:#c27b00; color:#102a43; transform:translateY(-1px); }
    div[data-baseweb="tab"] { font-weight:700; color:var(--ink); }
    div[data-baseweb="tab-highlight"] { background-color:var(--teal); height:4px; }
    [data-testid="stMetricValue"] { font-weight:700; color:var(--teal); }
    [data-testid="stWidgetLabel"] p { font-weight:700; color:var(--ink); }
    [data-testid="stSidebar"] { background:#102a43; }
    [data-testid="stSidebar"] * { color:#f7fafc; font-weight:600; }
    [data-testid="stSidebar"] .stRadio label, [data-testid="stSidebar"] .stSelectbox label { color:#d9f0eb; font-weight:700; }
    </style>
    """,
    unsafe_allow_html=True,
)


model, dataset, validation_accuracy, matrix = train_model()
technique_model, technique_accuracy = train_technique_model()

with st.sidebar:
    st.markdown("### CIPHERLENS")
    st.caption("CLASSICAL CRYPTOGRAPHY LAB")
    st.markdown("---")
    view = st.radio("Navigate", ["Overview", "Learn the concepts", "Classify a cipher", "Model lab"])
    st.markdown("---")
    st.caption("PANTECH SOLUTIONS")


if view == "Overview":
    st.markdown('<div class="hero"><div class="eyebrow">ML PROJECT / CLASSIFICATION TECHNIQUES</div><h1>Read the shape of a cipher.</h1><p>An interactive classroom lab for learning how machine learning can classify classical encryption families: substitution replaces characters; transposition rearranges them.</p></div>', unsafe_allow_html=True)
    st.write("")
    left, right = st.columns([1.4, 1])
    with left:
        st.markdown("#### The learning loop")
        st.markdown('<div class="flow"><span>PLAINTEXT</span><b>→</b><span>CLASSICAL CIPHER</span><b>→</b><span>FEATURES</span><b>→</b><span>ML PREDICTION</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="callout"><strong>Important:</strong> This is an educational classifier trained on synthetic examples. It demonstrates an ML workflow; it is not a dependable cryptanalysis tool for unknown real-world ciphertext.</div>', unsafe_allow_html=True)
        st.markdown("#### What this project demonstrates")
        st.write("- Feature engineering from ciphertext statistics")
        st.write("- A Random Forest classification model")
        st.write("- Confidence scores and validation results")
        st.write("- Why classical ciphers are useful for learning, but weak for modern security")
    with right:
        st.markdown('<div class="panel"><div class="label">TRAINING SET</div><div class="metric">%d samples</div><p>Balanced synthetic examples from Caesar, Vigenere, Rail Fence, and Columnar Transposition ciphers.</p><div class="label">VALIDATION ACCURACY</div><div class="metric">%.1f%%</div><p>Held-out examples from the generated dataset.</p></div>' % (len(dataset), validation_accuracy * 100), unsafe_allow_html=True)

elif view == "Learn the concepts":
    st.markdown('<div class="eyebrow">START HERE / BEGINNER MODE</div><h2>Classical encryption, from the beginning</h2>', unsafe_allow_html=True)
    st.write("First understand the message journey. Then learn the two big ways classical ciphers change a message.")
    intro, tab1, tab2, tab3 = st.tabs(["1. Basics", "2. Substitution", "3. Transposition", "4. Practice"])
    with intro:
        st.markdown("#### The five words you need")
        st.dataframe(pd.DataFrame([
            ["Plaintext", "The original readable message", "HELLO"],
            ["Key", "A secret number or word that controls the rule", "3 or LEMON"],
            ["Encryption", "Changing plaintext into a secret-looking message", "HELLO → KHOOR"],
            ["Ciphertext", "The changed message sent to someone", "KHOOR"],
            ["Decryption", "Using the key to get the original message back", "KHOOR → HELLO"],
        ], columns=["Word", "Easy meaning", "Example"]), use_container_width=True, hide_index=True)
        st.markdown("#### The complete message journey")
        st.markdown('<div class="flow"><span>1. PLAINTEXT<br><small>HELLO</small></span><b>→</b><span>2. ENCRYPT<br><small>use key 3</small></span><b>→</b><span>3. CIPHERTEXT<br><small>KHOOR</small></span></div>', unsafe_allow_html=True)
        st.markdown('<div class="flow"><span>1. CIPHERTEXT<br><small>KHOOR</small></span><b>→</b><span>2. DECRYPT<br><small>reverse key 3</small></span><b>→</b><span>3. PLAINTEXT<br><small>HELLO</small></span></div>', unsafe_allow_html=True)
        st.markdown("#### The only difference to remember")
        st.markdown('<div class="panel"><h3>SUBSTITUTION = REPLACE</h3><p>Letters are changed into other letters or codes. The positions usually stay in the same order.</p><div class="flow"><span>H</span><b>→</b><span>replace</span><b>→</b><span>K</span></div><h3>TRANSPOSITION = REARRANGE</h3><p>The same letters are kept, but their positions are moved.</p><div class="flow"><span>H E L L O</span><b>→</b><span>rearrange</span><b>→</b><span>L O H E L</span></div></div>', unsafe_allow_html=True)
        st.info("Learning tip: Always ask two questions: Did the letters change? If yes, it is substitution. Did only the order change? If yes, it is transposition.")
    with tab1:
        st.markdown("#### Substitution means REPLACE")
        st.write("Take one letter from the original message and replace it with another letter or code. Do this from left to right. The message order stays the same.")
        st.markdown("**Three simple steps**")
        st.write("1. Read one plaintext letter.")
        st.write("2. Look at the key or mapping.")
        st.write("3. Write the replacement letter or code.")
        st.markdown('<div class="flow"><span>H</span><b>→</b><span>RULE: +3</span><b>→</b><span>K</span></div>', unsafe_allow_html=True)
        st.markdown("**Complete A-Z reference: Caesar key 3**")
        st.dataframe(alphabet_table(list("DEFGHIJKLMNOPQRSTUVWXYZABC"), "Letter is replaced; position stays the same"), use_container_width=True, hide_index=True)
        st.markdown("**Substitution techniques, one by one**")
        st.dataframe(pd.DataFrame([
            ["Caesar", "Replace each letter with a fixed shift", "Key = number", "HELLO → KHOOR"],
            ["Atbash", "Mirror the alphabet", "No key", "A → Z, H → S"],
            ["Monoalphabetic", "Use one scrambled A-Z mapping", "26-letter permutation", "A always maps to the same letter"],
            ["Homophonic", "Give one letter several possible codes", "Code table", "A may be 11 or 41"],
            ["Playfair", "Replace pairs using a 5×5 key square", "Keyword", "Encrypts digraphs, not single letters"],
            ["Vigenere", "Use changing Caesar shifts", "Repeated keyword", "ATTACK + LEMON → LXFOPV"],
        ], columns=["Technique", "Simple explanation", "Key", "Example / answer"]), use_container_width=True, hide_index=True)
        st.markdown("**Substitution diagrams: input → rule → answer**")
        substitution_diagrams = [
            ("1. Caesar", "HELLO", "Shift every letter +3", "KHOOR", "Each letter moves three places forward: H → K."),
            ("2. Atbash", "HELLO", "Mirror A-Z: A↔Z, B↔Y", "SVOOL", "The alphabet is reversed: H → S and E → V."),
            ("3. Monoalphabetic", "HELLO", "Use fixed map A-Z → QWERTY...", "ITSSV", "Every letter always uses the same scrambled replacement."),
            ("4. Homophonic", "MEET", "Use numeric code table", "22 15 15 30", "A letter is represented by a code; some letters can have multiple codes."),
            ("5. Playfair", "INSTRUMENTS", "Encrypt two letters at a time", "GATLMZCLRQXA", "Pairs use a 5×5 key square, so the rule works on digraphs."),
            ("6. Vigenere", "ATTACK", "Repeat key LEMON and add shifts", "LXFOPV", "The key changes the Caesar shift at each position."),
        ]
        substitution_steps = {
            "1. Caesar": "A B C D E ... X Y Z\n+3:  D E F G H ... A B C\nHELLO: H E L L O → K H O O R",
            "2. Atbash": "A B C ... H ... S ... Z\nZ Y X ... S ... H ... A\nHELLO → SVOOL",
            "3. Monoalphabetic": "PLAIN:  A B C D E ... H ... L ... O\nCIPHER: Q W E R T ... I ... S ... V\nHELLO → ITSSV",
            "4. Homophonic": "M → 22\nE → 15\nE → 15\nT → 30\nMEET → 22 15 15 30",
            "5. Playfair": "IN | ST | RU | ME | NT | SX\n  ↓ pair rule using key square\nGA | TL | MZ | CL | RQ | XA\nINSTRUMENTS → GATLMZCLRQXA",
            "6. Vigenere": "PLAIN: A T T A C K\nKEY:   L E M O N L\nADD:   0+11, 19+4, 19+12 ...\nANSWER: L X F O P V",
        }
        substitution_decryption = {
            "1. Caesar": "TO DECRYPT: move every letter back 3\nK H O O R → H E L L O\nANSWER: KHOOR becomes HELLO",
            "2. Atbash": "TO DECRYPT: mirror the alphabet again\nS V O O L → H E L L O\nANSWER: the same mirror rule reverses the change",
            "3. Monoalphabetic": "TO DECRYPT: use the reverse map\nI T S S V → H E L L O\nANSWER: look up cipher letters in the bottom row",
            "4. Homophonic": "TO DECRYPT: split the codes and look them up\n22 15 15 30 → M E E T\nANSWER: the code table returns the original letters",
            "5. Playfair": "TO DECRYPT: process pairs and reverse each square rule\nGA | TL | MZ | CL | RQ | XA → INSTRUMENTS\nANSWER: the key square recovers the original pairs",
            "6. Vigenere": "TO DECRYPT: repeat LEMON and subtract its shifts\nL X F O P V → A T T A C K\nANSWER: subtraction reverses the addition",
        }
        for title, sample_input, rule, answer, explanation in substitution_diagrams:
            st.markdown(f"**{title}**")
            st.markdown(f'<div class="flow"><span>INPUT: {sample_input}</span><b>→</b><span>RULE: {rule}</span><b>→</b><span>ANSWER: {answer}</span></div>', unsafe_allow_html=True)
            st.code(substitution_steps[title])
            st.caption(explanation)
            st.markdown(f"**Decrypt / get the original back:** {substitution_decryption[title]}")
        st.markdown("**Caesar example**")
        st.code("HELLO  +  key 3  →  KHOOR")
        st.info("Vigenere extends this idea by using a repeated keyword, so the shift can change at every position.")
    with tab2:
        st.markdown("#### Transposition means REARRANGE")
        st.write("Do not change the letters. Move them to new positions using a path or key. The same letters are still present, but the order is different.")
        st.markdown("**Three simple steps**")
        st.write("1. Write the original letters.")
        st.write("2. Move them using the key.")
        st.write("3. Read them in the new order.")
        st.markdown('<div class="flow"><span>H E L L O</span><b>→</b><span>POSITION RULE</span><b>→</b><span>L O H E L</span></div>', unsafe_allow_html=True)
        st.markdown("**Complete A-Z reference: positions are preserved, order changes**")
        st.dataframe(alphabet_table(position_note="Letter is unchanged; only its position is rearranged"), use_container_width=True, hide_index=True)
        st.markdown("**Transposition techniques, one by one**")
        st.dataframe(pd.DataFrame([
            ["Rail Fence", "Write letters in a zig-zag, read rows", "Number of rails", "HELLO → HOELL"],
            ["Columnar", "Write rows, read columns by keyword order", "Keyword", "ZEBRA numbers columns"],
            ["Double Transposition", "Apply columnar rearrangement twice", "One or two keywords", "Second pass rearranges the intermediate text"],
            ["Combined", "Substitute letters, then rearrange positions", "Both keys", "Character values and positions both change"],
        ], columns=["Technique", "Simple explanation", "Key", "Example / answer"]), use_container_width=True, hide_index=True)
        st.markdown("**Transposition diagrams: input → position rule → answer**")
        transposition_diagrams = [
            ("1. Rail Fence", "HELLO", "Write in a 3-rail zig-zag, read rows", "HOELL", "The letters stay H, E, L, L, O; only their order changes."),
            ("2. Columnar", "MEETME", "Write under ZEBRA, read columns 1,2,3,4,5", "MXEXEXTXME", "The keyword decides which column is read first; X fills empty cells."),
            ("3. Double Transposition", "MEETME", "Columnar rearrange twice with ZEBRA", "MXEXEXTXME → EEEXXTXMMX", "The first rearrangement is rearranged again for a stronger historical cipher."),
            ("4. Combined", "HELLO", "Caesar +3, then Columnar ZEBRA", "KHOOR → ROHOK", "First Caesar changes the letters; Columnar then changes their positions."),
        ]
        transposition_steps = {
            "1. Rail Fence": "STEP 1 - WRITE DOWN THE ZIG-ZAG\nRAIL 1: H . . . O\nRAIL 2: . E . L .\nRAIL 3: . . L . .\nPATH:    H → E → L → L → O\n\nSTEP 2 - READ EACH ROW\nRAIL 1 + RAIL 2 + RAIL 3 = HO + EL + L = HOELL",
            "2. Columnar": "KEY:      Z  E  B  R  A\nNUMBER:   5  3  2  4  1\n\nGRID:     M  E  E  T  M\n          E  X  X  X  X\n\nREAD 1,2,3,4,5: MX | EX | EX | TX | ME\nANSWER: MXEXEXTXME",
            "3. Double Transposition": "FIRST PASS:  MEETME → MXEXEXTXME\nSECOND PASS: MXEXEXTXME → EEEXXTXMMX\nThe second pass rearranges the first answer again.",
            "4. Combined": "STEP 1 - SUBSTITUTE: HELLO + 3 → KHOOR\nSTEP 2 - REARRANGE: KHOOR under ZEBRA\nREAD COLUMNS → ROHOK\nBoth letters and positions have changed.",
        }
        transposition_decryption = {
            "1. Rail Fence": "TO DECRYPT: mark the zig-zag spaces, fill rows with HOELL, then follow the path\nHOELL → H E L L O\nANSWER: HOELL becomes HELLO",
            "2. Columnar": "TO DECRYPT: fill columns in keyword order 1,2,3,4,5, then read rows\nMXEXEXTXME → MEETME\nANSWER: remove X padding at the end if it was added",
            "3. Double Transposition": "TO DECRYPT: undo the second pass, then undo the first pass\nEEEXXTXMMX → MXEXEXTXME → MEETME\nANSWER: two reverse passes recover the original",
            "4. Combined": "TO DECRYPT: undo Columnar first, then move Caesar letters back 3\nROHOK → KHOOR → HELLO\nANSWER: reverse operations in the opposite order",
        }
        for title, sample_input, rule, answer, explanation in transposition_diagrams:
            st.markdown(f"**{title}**")
            st.markdown(f'<div class="flow"><span>INPUT: {sample_input}</span><b>→</b><span>POSITION RULE: {rule}</span><b>→</b><span>ANSWER: {answer}</span></div>', unsafe_allow_html=True)
            st.code(transposition_steps[title])
            st.caption(explanation)
            st.markdown(f"**Decrypt / get the original back:** {transposition_decryption[title]}")
        st.markdown("**Rail Fence example: 3 rails**")
        st.code("W . . . E . . . C . . . E\n. E . R . D . S . O . V . R\n. . A . . . I . . . E . . .")
        st.info("Rail Fence follows a zig-zag path. Columnar Transposition writes into columns, then reads columns in keyword order.")
    with tab3:
        st.markdown("#### Generate and understand an example")
        technique = st.selectbox("Technique", [
            "Caesar (substitution)", "Atbash (substitution)", "Monoalphabetic (substitution)",
            "Homophonic (substitution)", "Playfair (digraph substitution)", "Vigenere (polyalphabetic)",
            "Rail Fence (transposition)", "Columnar (transposition)", "Double Transposition",
            "Combined: substitution then transposition",
        ])
        plaintext = st.text_input("Plaintext", "MEET ME AFTER CLASS")
        key_defaults = {
            "Caesar (substitution)": "3", "Atbash (substitution)": "none",
            "Monoalphabetic (substitution)": "QWERTYUIOPASDFGHJKLZXCVBNM",
            "Homophonic (substitution)": "fixed teaching table", "Playfair (digraph substitution)": "MONARCHY",
            "Vigenere (polyalphabetic)": "LEMON", "Rail Fence (transposition)": "3",
            "Columnar (transposition)": "ZEBRA", "Double Transposition": "ZEBRA",
            "Combined: substitution then transposition": "3 / ZEBRA",
        }
        key = st.text_input("Key / setting", key_defaults[technique])
        clean = normalize(plaintext)
        explanation = ""
        detail = ""
        display_mapping = list(string.ascii_uppercase)
        table_note = "Letter is unchanged; this technique uses a different rule"
        if technique == "Caesar (substitution)":
            shift = int(key) if key.isdigit() else 3
            result = caesar_encrypt(plaintext, shift)
            display_mapping = list(caesar_encrypt(string.ascii_uppercase, shift))
            table_note = f"Replace using shift {shift}"
            explanation = f"Each letter moves {shift} positions forward. Example: H → {caesar_encrypt('H', shift)}. Spaces stay unchanged."
            detail = "Formula: C = (P + K) mod 26"
        elif technique == "Atbash (substitution)":
            result = atbash_encrypt(plaintext)
            display_mapping = list(atbash_encrypt(string.ascii_uppercase))
            table_note = "Replace using the mirrored alphabet"
            explanation = "The alphabet is mirrored: A ↔ Z, B ↔ Y, C ↔ X. Example: H → S."
            detail = "This is a fixed keyless substitution. Applying it twice returns the original text."
        elif technique == "Monoalphabetic (substitution)":
            result, mapping = monoalphabetic_encrypt(plaintext, key)
            display_mapping = list(mapping)
            table_note = "Replace using the fixed scrambled alphabet"
            explanation = f"Every plaintext letter uses one fixed scrambled mapping. Example: A → {mapping[0]}, B → {mapping[1]}."
            detail = f"Mapping used: {string.ascii_uppercase} → {mapping}"
        elif technique == "Homophonic (substitution)":
            result = homophonic_encrypt(plaintext)
            display_mapping = [homophonic_encrypt(letter) for letter in string.ascii_uppercase]
            table_note = "One letter can have one of several numeric codes"
            explanation = "A plaintext letter can have more than one code, reducing visible frequency patterns. This demo uses a fixed numeric teaching table."
            detail = "Example codes: A → 11, E → 15, I → 19, O → 20, T → 30."
        elif technique == "Playfair (digraph substitution)":
            result, square = playfair_encrypt(plaintext, key)
            display_mapping = ["PAIR RULE"] * 26
            table_note = "Letters are processed in pairs using the key square"
            explanation = "Letters are encrypted in pairs using a 5×5 key square. Same row shifts right, same column shifts down, otherwise take the rectangle corners."
            detail = "Key square:\n" + "\n".join(square)
        elif technique == "Vigenere (polyalphabetic)":
            result = vigenere_encrypt(plaintext, key)
            first_key = (normalize(key) or "KEY")[0]
            display_mapping = list(caesar_encrypt(string.ascii_uppercase, ord(first_key) - 65))
            table_note = f"First shift uses key letter {first_key}; shifts change as the keyword repeats"
            repeated_key = (normalize(key) or "KEY") * ((len(clean) // len(normalize(key) or "KEY")) + 1)
            explanation = f"The keyword repeats under the plaintext: {repeated_key[:len(clean)]}. Each key letter supplies a different Caesar shift."
            detail = "Formula: Cᵢ = (Pᵢ + Kᵢ) mod 26"
        elif technique == "Rail Fence (transposition)":
            rails = int(key) if key.isdigit() else 3
            result = rail_fence_encrypt(plaintext, rails)
            table_note = f"A-Z letters stay unchanged; positions follow a {rails}-rail zig-zag"
            explanation = f"The letters are written along a zig-zag of {rails} rails, then read row by row. No letters are replaced."
            detail = "Character values stay the same; only their positions change."
        elif technique == "Columnar (transposition)":
            result = columnar_encrypt(plaintext, key)
            table_note = "A-Z letters stay unchanged; positions follow keyword column order"
            order = sorted(range(len(normalize(key) or "ZEBRA")), key=lambda index: ((normalize(key) or "ZEBRA")[index], index))
            explanation = f"The text fills a grid under {normalize(key) or 'ZEBRA'}, then columns are read alphabetically in order {[index + 1 for index in order]}. X is padding when needed."
            detail = "Character values stay the same; the keyword controls column order."
        elif technique == "Double Transposition":
            result, intermediate = double_transposition_encrypt(plaintext, key)
            table_note = "A-Z letters stay unchanged; positions are rearranged twice"
            explanation = "Columnar transposition is applied twice with the same keyword: first pass creates an intermediate text, second pass rearranges it again."
            detail = f"Intermediate text: {intermediate}"
        else:
            substituted = caesar_encrypt(plaintext, int(key.split("/")[0].strip()) if key.split("/")[0].strip().isdigit() else 3)
            column_key = key.split("/")[-1].strip() or "ZEBRA"
            result = columnar_encrypt(substituted, column_key)
            display_mapping = list(caesar_encrypt(string.ascii_uppercase, 3))
            table_note = "First replace with Caesar +3, then rearrange positions by columns"
            explanation = f"First Caesar substitution changes characters; then Columnar Transposition rearranges positions using {column_key}."
            detail = f"Intermediate substitution: {substituted}"
        st.markdown('<div class="code-line">%s → %s</div>' % (clean, result), unsafe_allow_html=True)
        st.markdown("#### How this answer was produced")
        st.write(explanation)
        st.code(detail)
        st.markdown("#### A-Z table used for this answer")
        st.caption("Read the table as Plain A-Z → Cipher / result. For transposition, the letters remain the same and the order is controlled by the key.")
        st.dataframe(alphabet_table(display_mapping, table_note), use_container_width=True, hide_index=True)

elif view == "Classify a cipher":
    st.markdown('<div class="eyebrow">PREDICTION WORKBENCH</div><h2>Classify or recover a cipher</h2>', unsafe_allow_html=True)
    st.write("Choose classification to identify the cipher family, or choose decryption when you know the technique and key and want to recover the original message.")
    operation = st.radio("Task", ["Classify cipher family", "Convert ciphertext to original text"], horizontal=True)
    if operation == "Convert ciphertext to original text":
        decrypt_technique = st.selectbox("Known technique", ["Caesar", "Atbash", "Monoalphabetic", "Homophonic", "Playfair", "Vigenere", "Rail Fence", "Columnar", "Double Transposition"])
        decrypt_defaults = {"Caesar": "3", "Atbash": "none", "Monoalphabetic": "QWERTYUIOPASDFGHJKLZXCVBNM", "Homophonic": "fixed teaching table", "Playfair": "MONARCHY", "Vigenere": "LEMON", "Rail Fence": "3", "Columnar": "ZEBRA", "Double Transposition": "ZEBRA"}
        ciphertext = st.text_area("Ciphertext", "KHOOR", height=100)
        decrypt_key = st.text_input("Key / setting", decrypt_defaults[decrypt_technique])
        if st.button("Recover original text", type="primary"):
            if decrypt_technique == "Caesar":
                shift = int(decrypt_key) if decrypt_key.isdigit() else 3
                original = caesar_encrypt(ciphertext, -shift)
                explanation = f"Reverse the Caesar shift by {shift}: K → H. The ciphertext becomes the original plaintext."
            elif decrypt_technique == "Atbash":
                original = atbash_encrypt(ciphertext)
                explanation = "Apply the mirrored alphabet again: S → H. Atbash decrypts by using the same operation as encryption."
            elif decrypt_technique == "Monoalphabetic":
                original = monoalphabetic_decrypt(ciphertext, decrypt_key)
                explanation = "Look up each ciphertext letter in the reverse mapping. For the default key, Q → A and W → B."
            elif decrypt_technique == "Homophonic":
                original = homophonic_decrypt(ciphertext)
                explanation = "Split the numeric ciphertext into tokens and look up each token in the reverse teaching table."
            elif decrypt_technique == "Playfair":
                original, square = playfair_decrypt(ciphertext, decrypt_key)
                explanation = "Read ciphertext in pairs and reverse the Playfair rule: left for same-row pairs, up for same-column pairs, and rectangle corners otherwise. A final X may be padding."
            elif decrypt_technique == "Vigenere":
                key_text = normalize(decrypt_key) or "KEY"
                original = vigenere_encrypt(ciphertext, "".join(chr(65 - (ord(char) - 65) % 26) for char in key_text))
                # Explicit reverse arithmetic keeps the explanation aligned with the result.
                original = "".join(chr((ord(char) - 65 - (ord(key_text[index % len(key_text)]) - 65)) % 26 + 65) if char in string.ascii_uppercase else char for index, char in enumerate(ciphertext.upper()))
                explanation = f"Repeat the keyword {key_text} under the ciphertext and subtract each key shift: L means subtract 11, E means subtract 4, and so on."
            elif decrypt_technique == "Rail Fence":
                rails = int(decrypt_key) if decrypt_key.isdigit() else 3
                original = rail_fence_decrypt(ciphertext, rails)
                explanation = f"Mark the {rails}-rail zig-zag positions, place ciphertext letters row by row, then read along the zig-zag path."
            elif decrypt_technique == "Columnar":
                original = columnar_decrypt(ciphertext, decrypt_key)
                explanation = f"Number the columns alphabetically using {normalize(decrypt_key) or 'ZEBRA'}, place ciphertext down those columns, then read across the restored rows. Trailing X is removed as padding."
            else:
                original, intermediate = double_transposition_decrypt(ciphertext, decrypt_key)
                explanation = f"Undo the second columnar rearrangement, producing {intermediate}; then undo the first rearrangement to recover the plaintext."
            st.success(f"Original text: {original}")
            st.markdown("#### How the original was recovered")
            st.write(explanation)
        st.markdown('<div class="callout"><strong>Important:</strong> Decryption needs the correct technique and key. Classification alone can suggest a family, but it cannot reliably recover plaintext without those details.</div>', unsafe_allow_html=True)
    else:
        st.write("Paste a ciphertext or choose a known example. The ML model predicts both the broad family and the specific classical technique.")
        sample_mode = st.radio("Input", ["Use an example", "Paste ciphertext"], horizontal=True)
        if sample_mode == "Use an example":
            example = st.selectbox("Example", [
                "Caesar / KHOOR", "Atbash / SVOOL", "Monoalphabetic / ITTOV",
                "Homophonic / 15 30 11 30", "Playfair / GATLMZCLRQXA", "Vigenere / LXFOPVEFRNHR",
                "Rail Fence / WECRLTEERDSOEEFEAOCAIVDEN", "Columnar / EVLNEACDTKESEAQROFOJDEECWIREE",
                "Double Transposition / LNRXE...", "Combined substitution + transposition / ...",
            ])
            sample = example.split(" / ", 1)[1]
        else:
            sample = st.text_area("Ciphertext", "KHOOR ZRUOG", height=100)
        if st.button("Run classification", type="primary"):
            cleaned = normalize(sample)
            if len(cleaned) < 4:
                st.warning("Enter at least four alphabetic characters so the feature extraction is meaningful.")
            else:
                features = extract_features(cleaned).reshape(1, -1)
                prediction = model.predict(features)[0]
                probabilities = model.predict_proba(features)[0]
                technique_prediction = technique_model.predict(features)[0]
                technique_probabilities = technique_model.predict_proba(features)[0]
                confidence = max(probabilities)
                technique_confidence = max(technique_probabilities)
                a, b, c, d = st.columns(4)
                with a:
                    st.metric("Predicted family", prediction)
                with b:
                    st.metric("Model confidence", f"{confidence:.1%}")
                with c:
                    st.metric("Letters analyzed", len(cleaned))
                with d:
                    st.metric("Predicted technique", technique_prediction)
                st.progress(float(confidence))
                st.caption(f"Family confidence: {confidence:.1%}  •  Technique confidence: {technique_confidence:.1%}")
                chart = pd.DataFrame({"Family": model.classes_, "Probability": probabilities}).set_index("Family")
                st.bar_chart(chart)
                technique_chart = pd.DataFrame({"Technique": technique_model.classes_, "Probability": technique_probabilities}).set_index("Technique")
                st.markdown("#### All technique probabilities")
                st.bar_chart(technique_chart)
                st.markdown("#### Features seen by the model")
                st.dataframe(pd.DataFrame([features[0]], columns=feature_names()).T.rename(columns={0: "value"}), use_container_width=True)
                st.markdown('<div class="callout"><strong>Interpret carefully:</strong> A prediction is a pattern-based estimate. Short texts, unknown languages, padding, and unseen cipher designs can make the result unreliable.</div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="eyebrow">MODEL LAB</div><h2>How the classifier works</h2>', unsafe_allow_html=True)
    st.write("The app generates labeled training examples, converts each ciphertext into numeric features, trains a Random Forest, and evaluates it on held-out data.")
    steps = st.columns(4)
    for column, number, title, body in zip(steps, ["01", "02", "03", "04"], ["Generate", "Extract", "Learn", "Evaluate"], ["Create Caesar, Vigenere, Rail Fence, and Columnar examples.", "Measure entropy, repeats, frequency balance, and n-grams.", "Fit a Random Forest to the feature vectors.", "Test on samples the model did not see during training."]):
        with column:
            st.markdown(f'<div class="panel"><div class="eyebrow">{number}</div><h3>{title}</h3><p>{body}</p></div>', unsafe_allow_html=True)
    st.write("")
    left, right = st.columns([1.2, 1])
    with left:
        st.markdown("#### Feature importance")
        importance = pd.DataFrame({"Feature": feature_names(), "Importance": model.feature_importances_}).sort_values("Importance", ascending=True).set_index("Feature")
        st.bar_chart(importance)
    with right:
        st.markdown("#### Held-out confusion matrix")
        st.caption("Rows are actual labels; columns are predicted labels.")
        st.dataframe(pd.DataFrame(matrix, index=["Actual substitution", "Actual transposition"], columns=["Predicted substitution", "Predicted transposition"]), use_container_width=True)
        st.metric("Validation accuracy", f"{validation_accuracy:.1%}")
    st.markdown("#### Dataset preview")
    st.dataframe(dataset.head(8), use_container_width=True, hide_index=True)
    st.caption("The generated dataset is intentionally small and synthetic so students can inspect it. Accuracy here should not be interpreted as real-world security performance.")

st.markdown("---")
st.caption("PANTECH SOLUTIONS  •  CLASSICAL ENCRYPTION TECHNIQUES  •  EDUCATIONAL ML DEMONSTRATION")
