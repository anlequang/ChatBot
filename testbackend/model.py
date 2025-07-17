# model.py
import pandas as pd
import numpy as np
from underthesea import word_tokenize
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Bước 1: Load dữ liệu
df = pd.read_csv("ViMedical_Disease.csv")
df.drop_duplicates(inplace=True)
df.dropna(subset=["Question", "Disease"], inplace=True)
df["Question_tokenized"] = df["Question"].apply(lambda x: word_tokenize(x, format="text"))

# Bước 2: One-hot encode
encoder = OneHotEncoder(sparse_output=False)
y_onehot = encoder.fit_transform(df[["Disease"]])
y_df = pd.DataFrame(y_onehot, columns=encoder.get_feature_names_out(["Disease"]))
df = pd.concat([df, y_df], axis=1)

# Bước 3: Chuẩn bị tập train/test
X = df["Question_tokenized"]
y = df.filter(like="Disease_")
y_labels = np.argmax(y.values, axis=1)

X_train, X_temp, y_train, y_temp = train_test_split(X, y_labels, test_size=0.4, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# Vector hóa
vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train.astype(str))
X_val_vec = vectorizer.transform(X_val.astype(str))
X_test_vec = vectorizer.transform(X_test.astype(str))

# Huấn luyện mô hình
model = LogisticRegression(solver="saga", random_state=42, max_iter=1000)
model.fit(X_train_vec, y_train)

# Danh sách tên bệnh
disease_names = [col.replace("Disease_", "") for col in y.columns]

# 👉 Hàm dự đoán từ câu hỏi
def du_doan_benh(cau_hoi: str) -> str:
    cau_hoi_token = word_tokenize(cau_hoi, format="text")
    cau_hoi_vec = vectorizer.transform([cau_hoi_token])
    label = model.predict(cau_hoi_vec)[0]
    return disease_names[label]
