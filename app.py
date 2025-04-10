import streamlit as st
import hashlib
from cryptography.fernet import Fernet
import time

# Initialize session state for persistence
if "key" not in st.session_state:
    st.session_state.key = Fernet.generate_key()

if "stored_data" not in st.session_state:
    st.session_state.stored_data = (
        {}
    )  # Format: {"encrypted_text": {"passkey": "hashed_passkey"}}

if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0

# Create cipher with persistent key
cipher = Fernet(st.session_state.key)


# 3. Hashing Function
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()


# 4. Encrypt Function
def encrypt_data(text):
    return cipher.encrypt(text.encode()).decode()


# 5. Decrypt Function
def decrypt_data(encrypted_text, passkey):
    hashed_input = hash_passkey(passkey)

    data = st.session_state.stored_data.get(encrypted_text)
    if data and data["passkey"] == hashed_input:
        st.session_state.failed_attempts = 0
        return cipher.decrypt(encrypted_text.encode()).decode()
    else:
        st.session_state.failed_attempts += 1
        return None


# 6. UI Setup
st.set_page_config(page_title="Secure Data Vault", page_icon="🔐")
st.title("🔐 Secure Data Encryption & Retrieval System")

menu = ["🏠 Home", "📥 Store Data", "📤 Retrieve Data", "🔑 Admin Login"]
choice = st.sidebar.radio("Navigation", menu)

# 7. Home
if choice == "🏠 Home":
    st.subheader("Welcome to the Secure Vault App")
    st.write("Encrypt your data with a secret passkey and retrieve it securely.")
    # Display storage status for debugging
    st.write(f"Currently stored items: {len(st.session_state.stored_data)}")

# 8. Store Data
elif choice == "📥 Store Data":
    st.subheader("📦 Store Your Data")
    text = st.text_area("Enter the data you want to encrypt")
    passkey = st.text_input("Set a passkey to lock your data", type="password")

    if st.button("🔐 Encrypt & Save"):
        if text and passkey:
            encrypted_text = encrypt_data(text)
            hashed_pass = hash_passkey(passkey)
            st.session_state.stored_data[encrypted_text] = {"passkey": hashed_pass}
            st.success("✅ Your data has been encrypted and saved.")
            st.code(encrypted_text, language="text")
            st.info("⚠️ Save this encrypted text to retrieve your data later")
        else:
            st.error("❗ Please enter both data and a passkey.")

# 9. Retrieve Data
elif choice == "📤 Retrieve Data":
    st.subheader("🔍 Retrieve Encrypted Data")
    encrypted_input = st.text_area("Paste your encrypted text")
    passkey = st.text_input("Enter your passkey", type="password")

    if st.button("🔓 Decrypt"):
        if encrypted_input and passkey:
            # Check if the encrypted text exists in our storage
            if encrypted_input not in st.session_state.stored_data:
                st.error("❌ This encrypted text doesn't exist in storage.")
            else:
                result = decrypt_data(encrypted_input, passkey)
                if result:
                    st.success("✅ Data Decrypted Successfully")
                    st.code(result, language="text")
                else:
                    remaining = max(0, 3 - st.session_state.failed_attempts)
                    st.error(f"❌ Incorrect passkey! Attempts left: {remaining}")
                    if st.session_state.failed_attempts >= 3:
                        st.warning(
                            "🔐 Too many failed attempts. Reauthorization required."
                        )
                        time.sleep(1)
                        st.rerun()  # Modern replacement for experimental_rerun
        else:
            st.error("⚠️ Both fields are required.")

# 10. Login (for reset)
elif choice == "🔑 Admin Login":
    st.subheader("Admin Login to Reset")
    master_pass = st.text_input("Enter Admin Password", type="password")

    if st.button("Login"):
        if master_pass == "admin123":  # You can change this for security
            st.session_state.failed_attempts = 0
            st.success("✅ Access granted! You can try retrieving data again.")
            time.sleep(1)
            st.rerun()  # Modern replacement for experimental_rerun
        else:
            st.error("❌ Incorrect admin password.")

# Debug section (can be removed in production)
with st.expander("Debug Info"):
    st.write(f"Failed attempts: {st.session_state.failed_attempts}")
    st.write(f"Number of stored items: {len(st.session_state.stored_data)}")
    if st.button("Clear All Data"):
        st.session_state.stored_data = {}
        st.session_state.failed_attempts = 0
        st.success("All data cleared!")
