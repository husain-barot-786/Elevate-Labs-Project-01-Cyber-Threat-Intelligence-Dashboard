# Secure Chat App with End-to-End Encryption (E2EE)

A robust, real-time chat application that ensures privacy and security for all users by implementing true end-to-end encryption. Messages remain confidential from sender to receiver, protected even from the server itself. This project demonstrates industry-standard cryptographic practices and is suitable as a foundation for production-grade secure messaging.

---

## Features

- **End-to-End Encrypted Messaging:** Only sender and recipient can read the messages; even the server cannot decrypt them.
- **Hybrid Cryptography:** Uses RSA (asymmetric) for secure key exchange and AES (symmetric) for fast message encryption.
- **Encrypted Chat Logs:** All chat logs are encrypted at rest on the server using AES.
- **Real-Time Communication:** Built with Flask-SocketIO for instant messaging.
- **Group Chats:** Secure group messaging with group key management.
- **User-Friendly Web Interface:** Intuitive and responsive frontend built with HTML, CSS, and JavaScript.
- **Cross-Platform:** Works on all major operating systems where Python and a web browser are available.

---

## Project Structure

```
Secure-Chat-App-with-End-to-End-Encryption/
├── assets/
│   └── demo.mp4
├── app/
│   ├── __init__.py           # Flask app initialization
│   ├── chat_logs.py          # Encrypted chat log management
│   ├── encryption.py         # RSA/AES encryption utilities
│   ├── main.py               # Entry point, server setup, routes, and sockets
│   └── models.py             # User and message data models
├── static/
│   ├── chat.js               # Client-side logic for chat functionality
│   ├── index.html            # Frontend interface
│   └── styles.css
├── Report.pdf
├── .gitignore
├── README.md
├── requirements.txt
└── chat_logs                 # Auto created file
```

---

## Security Overview

- **End-to-End Encryption:** Each message is encrypted on the sender's device and only decrypted by the intended recipient.
- **RSA Public/Private Keys:** Each user generates their own key pair on registration; public keys are exchanged for secure key negotiation.
- **AES Message Encryption:** Fast symmetric encryption for all messages; AES keys are exchanged securely using RSA.
- **Encrypted Chat Logs:** All stored logs are AES-encrypted, so even a server breach does not reveal message content.
- **No Plaintext Storage:** Neither messages nor keys are ever stored or transmitted in plaintext.

---

## Requirements

- Python 3.8+
- `pip` (Python package manager)
- A modern web browser

---

## Quick Start

1. Clone the Repository
    ```sh
    git clone https://github.com/husain-barot-786/Elevate-Labs-Project-01-Cyber-Threat-Intelligence-Dashboard/Project-03-Secure-Chat-App-with-End-to-End-Encryption.git
    cd Project-03-Secure-Chat-App-with-End-to-End-Encryption
    ```

2. Create and Activate a Virtual Environment
    - Windows:
        bash
        ```
        python -m venv venv
        venv\Scripts\activate
        ```
    - macOS/Linux:
        bash
        ```
        python3 -m venv venv
        source venv/bin/activate
        ```

3. Install Dependencies
    bash
    ```
    pip install -r requirements.txt
    ```

4. Run the Application
    bash
    ```
    python -m app.main
    ```
    The server will start on `http://localhost:5000/`

5. Open the App
    - In your browser, go to: [http://localhost:5000/](http://localhost:5000/)

---

## Usage Guide

1. **Register a New User:** The app will generate your RSA key pair automatically.
2. **Login and Start Chatting:** You can send encrypted messages to any registered user in real time.
3. **Group Chats:** Create and join group chats; group keys are securely distributed among members.
4. **Chat Logs:** All messages are stored encrypted; only you and your chat partners can decrypt them.
5. **Logout:** Ends your session and clears any sensitive data from memory.

---

## Tech Stack

- **Backend:** Python 3, Flask, Flask-SocketIO, cryptography (RSA, AES)
- **Frontend:** HTML5, CSS3, JavaScript (vanilla)
- **Real-Time:** Socket.IO (with Eventlet for async support)
- **Security:** RSA (2048-bit default), AES (256-bit default), secure key exchanges

---

## Best Practices & Recommendations

- **Never commit your `venv/`, `__pycache__/`, or log files:** These are ignored by the included `.gitignore`.
- **Change default key sizes only if you know what you’re doing.**
- **Do not use this as-is for production without a full security audit.**

---

## Troubleshooting

- **Dependencies not installing?** Make sure your Python version is 3.8+ and pip is updated (`pip install --upgrade pip`).
- **Can't access app on localhost?** Ensure the server started successfully and no firewall is blocking port 5000.
- **Issues with encryption?** Check for error logs and confirm all cryptography dependencies are installed.

---

## Documentation & Report

- **`README.md`:** You’re reading it! All setup and usage information is here.
- **`Report.pdf`:** A detailed two-page report is included, covering project goals, cryptography choices, design, and implementation steps.

---

## Contribution

1. Fork the repository
2. Create a new branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

---

## Acknowledgements

- Python & Flask documentation
- cryptography.io for modern cryptographic primitives
- Socket.IO for real-time communication
- All open-source contributors who made these tools possible

---

**Secure your chats. Protect your privacy. Experience the future of encrypted communication!**

---

For questions or contributions, please open an issue or pull request!
