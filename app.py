import streamlit as st
import hashlib
from cryptography.fernet import Fernet
import time

# Generate a key and store it in session
if "key" not in st.session_state:
    st.session_state.key = Fernet.generate_key()

# Dictionary to store encrypted data and hashed passkeys
if "storedData" not in st.session_state:
    st.session_state.storedData = {}

# Track failed decryption attempts
if "failedAttempts" not in st.session_state:
    st.session_state.failedAttempts = 0

cipher = Fernet(st.session_state.key)


def hashPasskey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()


def encryptData(text):
    return cipher.encrypt(text.encode()).decode()


def decryptData(encryptedText, passkey):
    data = st.session_state.storedData.get(encryptedText)
    hashedInput = hashPasskey(passkey)

    if data and data["passkey"] == hashedInput:
        st.session_state.failedAttempts = 0
        return cipher.decrypt(encryptedText.encode()).decode()
    else:
        st.session_state.failedAttempts += 1
        return None


st.set_page_config(page_title="Secure Data Vault", page_icon="🔐")
st.title("🔐 Secure Data Encryption & Retrieval System")

menu = ["🏠 Home", "📥 Store Data", "📤 Retrieve Data", "🔑 Admin Login"]
choice = st.sidebar.radio("Navigation", menu)

# Home
if choice == "🏠 Home":
    st.subheader("Welcome to the Secure Vault App")
    st.write("Encrypt your data with a secret passkey and retrieve it securely.")
    st.write(f"Currently stored items: {len(st.session_state.storedData)}")

# Store Data
elif choice == "📥 Store Data":
    st.subheader("📦 Store Your Data")
    text = st.text_area("Enter the data you want to encrypt")
    passkey = st.text_input("Set a passkey to lock your data", type="password")

    st.warning(
        "⚠️ WARNING: Your passkey is never stored. If you forget it, your data cannot be recovered."
    )

    if st.button("🔐 Encrypt & Save"):
        if text and passkey:
            encryptedText = encryptData(text)
            hashedPasskey = hashPasskey(passkey)
            st.session_state.storedData[encryptedText] = {"passkey": hashedPasskey}
            st.success("✅ Your data has been encrypted and saved.")
            st.code(encryptedText, language="text")
            st.warning(
                "⚠️ Save this encrypted text somewhere safe. You need it to retrieve your data."
            )
        else:
            st.error("❗ Please enter both data and a passkey.")

# Retrieve Data
elif choice == "📤 Retrieve Data":
    st.subheader("🔍 Retrieve Encrypted Data")
    encryptedInput = st.text_area("Paste your encrypted text")
    passkey = st.text_input("Enter your passkey", type="password")

    st.warning(
        "⚠️ WARNING: You must enter the exact same passkey used during encryption. Forgotten passkeys make decryption impossible."
    )

    if st.button("🔓 Decrypt"):
        if encryptedInput and passkey:
            if encryptedInput not in st.session_state.storedData:
                st.error("❌ This encrypted text doesn't exist in storage.")
            else:
                result = decryptData(encryptedInput, passkey)
                if result:
                    st.success("✅ Decryption successful!")
                    st.code(result, language="text")
                else:
                    remaining = max(0, 3 - st.session_state.failedAttempts)
                    st.error(f"❌ Incorrect passkey! Attempts left: {remaining}")
                    if st.session_state.failedAttempts >= 3:
                        st.warning(
                            "🚨 Too many failed attempts. Please wait and try again later."
                        )
                        time.sleep(5)
                        st.rerun()
        else:
            st.error("⚠️ Both fields are required.")

# Admin Login
elif choice == "🔑 Admin Login":
    st.subheader("Admin Login to Reset")
    master_pass = st.text_input("Enter Admin Password", type="password")

    st.warning(
        "⚠️ WARNING: This action will permanently delete all stored data. Make sure this is what you want!"
    )

    if st.button("Login"):
        if master_pass == "admin123":
            st.success("✅ Login successful!")
            st.session_state.storedData = {}
            st.session_state.failedAttempts = 0
            st.warning("⚠️ All stored data has been reset permanently!")
        else:
            st.error("❌ Incorrect admin password.")

# Debug / Developer Info
with st.expander("🛠️ Debug Info"):
    st.write(f"Failed attempts: {st.session_state.failedAttempts}")
    st.write(f"Number of stored items: {len(st.session_state.storedData)}")
    st.write(f"Session Key: {st.session_state.key.decode()}")

    if st.button("🧹 Clear All Data"):
        st.session_state.storedData = {}
        st.session_state.failedAttempts = 0
        st.success("✅ All data cleared from session.")
