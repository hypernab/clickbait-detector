import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# ── Load data ─────────────────────────────────────────────────────────────────
frames = []

try:
    df = pd.read_csv("clickbait.csv")
    frames.append(df)
    print(f"✅ Loaded {len(df)} fresh headlines")
except:
    print("⚠️  clickbait.csv not found, using Kaggle only")

try:
    kaggle_df = pd.read_csv("clickbait_data.csv")
    frames.append(kaggle_df)
    print(f"✅ Loaded {len(kaggle_df)} Kaggle headlines")
except:
    print("❌ clickbait_data.csv not found - can't continue")
    exit()

# ── Merge and clean ───────────────────────────────────────────────────────────
master = pd.concat(frames, ignore_index=True)
master = master.drop_duplicates(subset=["headline"])
master = master.dropna(subset=["headline", "clickbait"])  # fixes the NaN error
print(f"📚 Master dataset: {len(master)} rows")

# ── Train ─────────────────────────────────────────────────────────────────────
vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
X = vectorizer.fit_transform(master["headline"])
y = master["clickbait"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = MultinomialNB()
model.fit(X_train, y_train)

score = accuracy_score(y_test, model.predict(X_test))
print(f"🏁 Accuracy: {score:.2%}")

# ── Run ───────────────────────────────────────────────────────────────────────
print("\nDetector ready. Type 'exit' to quit.\n")
while True:
    headline = input("📝 Paste a headline: ")
    if headline.lower() == "exit":
        break
    result = model.predict(vectorizer.transform([headline]))[0]
    print("🚨 CLICKBAIT" if result == 1 else "✅ LEGIT")