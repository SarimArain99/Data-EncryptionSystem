# 🔐 Secure Data Encryption & Retrieval System

A secure and minimal Streamlit app to encrypt and retrieve your sensitive data using a passkey. Built using Python, Streamlit, and the cryptography library, this vault-style app is perfect for learning how encryption and hashing work in a practical way.

---

## 🚀 Live Demo

👉 **Try it out here:** [dataencryptionsystem.streamlit.app](https://dataencryptionsystem.streamlit.app/)  
📁 **View Source:** [GitHub Repository](https://github.com/SarimArain99/Data-EncryptionSystem)

---

## 🧠 What Can It Do?

🔐 Encrypt any custom text using a private passkey  
🔓 Retrieve your encrypted data using the exact same passkey  
🔑 SHA-256 passkey hashing to ensure strong security  
🚫 Prevents access after 3 failed decryption attempts  
🧹 Admin reset feature to clear all session data  
📦 Uses Streamlit's session state to temporarily store data  

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Streamlit**
- **cryptography.fernet**
- **hashlib (for passkey hashing)**

---

## 🧪 How to Use

### 1️⃣ Store Data
- Enter the data you want to encrypt
- Choose a passkey
- Click **"Encrypt & Save"** to generate the encrypted text
- Save the encrypted text to use later

### 2️⃣ Retrieve Data
- Paste the encrypted text
- Enter the original passkey
- Click **"Decrypt"** to retrieve your secure data

### 3️⃣ Admin Login
- Enter the admin password: `admin123`
- This will reset all stored data in the current session

---

## ⚙️ Local Installation

```bash
# Step 1: Clone the repo
git clone https://github.com/SarimArain99/Data-EncryptionSystem.git
cd Data-EncryptionSystem

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Run the app
streamlit run app.py
