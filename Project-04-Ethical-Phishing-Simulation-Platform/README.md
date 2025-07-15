# Ethical Phishing Simulation Platform

A comprehensive web-based platform for simulating phishing email campaigns in a safe, educational environment. This project helps organizations and individuals raise awareness and educate users about phishing attacks by providing end-to-end simulation—from campaign creation to analytics and user education—using a modern, user-friendly interface.

---

## Features

- **Phishing Campaign Simulation:** Create and manage realistic phishing email campaigns for training and awareness.
- **Customizable Templates:** Design and use HTML-based phishing email templates to fit various training scenarios.
- **Safe Lab Environment:** Send phishing emails to test users in a controlled, non-malicious environment.
- **User Interaction Tracking:** Monitor who clicked phishing links, entered data, and log timestamps for all actions.
- **Detailed Analytics Dashboard:** Visualize campaign results including open rates, click rates, and success rates.
- **Post-Campaign Education:** Automatically display best practices and educational content to users after campaign completion.
- **Simple Web Interface:** Easy-to-use dashboards for admins to manage campaigns and view analytics.

---

## Project Structure

```
Ethical-Phishing-Simulation-Platform/
├── assets/
│   └── demo.mp4
├── phishing_templates/
│   ├── template1.html
│   └── template2.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── images/
│       └── phishlab_logo.png
├── templates/
│   ├── analytics.html
│   ├── base.html
│   ├── base_login.html
│   ├── base_sidebar.html
│   ├── campaign_new.html
│   ├── campaign_view.html
│   ├── dashboard.html
│   ├── educate.html
│   ├── error.html
│   ├── index.html
│   ├── login.html
│   └── sent.html
├── Report.pdf
├── .gitignore
├── README.md
├── app.py
├── config.py
├── database.db             # SQLite DB (auto-created)
└── requirements.txt
```

---

## Security & Data Management

- **Safe Testing Only:** All phishing simulations are for educational purposes only and run in a closed lab environment.
- **SQLite Database:** All campaign data, results, and user interactions are stored securely in an auto-generated `database.db` file.
- **Data Privacy:** No real malicious emails or harmful payloads are sent—everything is for awareness and training.
- **Project Hygiene:** Database files and other runtime artifacts are excluded from version control using `.gitignore`.

---

## Requirements

- Python 3.8+
- `pip` (Python package manager)
- Flask web framework
- (Optional) Sendmail/Postfix for local SMTP testing
- Modern web browser

---

## Quick Start

1. **Clone the Repository**
    bash
    ```
    git clone https://github.com/husain-barot-786/Elevate-Labs-Project-01-Cyber-Threat-Intelligence-Dashboard.git
    cd Project-04-Ethical-Phishing-Simulation-Platform
    ```

2. **Create and Activate a Virtual Environment**
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

3. **Install Dependencies**
    bash
    ```
    pip install -r requirements.txt
    ```

5. **Run the Application**
    bash
    ```
    python app.py
    ```
    The server will start on `http://localhost:5000/`.

6. **Open the App**
    - In your browser, go to: [http://localhost:5000/](http://localhost:5000/)
    - Sign in infor - Username: Admin | Password: Admin123    (Refer app.py)

---

## Usage Guide

1. **Admin Login:** Access the admin dashboard through the login page.
2. **Create a Campaign:** Specify recipients, select or customize a phishing template, and launch the campaign.
3. **User Interaction:** Test users receive emails and interact with simulated phishing pages in a safe lab.
4. **Track Results:** The dashboard provides analytics for opened emails, clicked links, and data entry actions.
5. **Educate Users:** After campaign completion, the platform displays educational messages to reinforce best practices.

---

## Tech Stack

- **Backend:** Python 3, Flask, SQLite
- **Email:** Sendmail/Postfix (or any SMTP server) for sending simulated phishing emails
- **Frontend:** HTML5, CSS3 (custom), Jinja2 templating
- **Data:** SQLite3 for campaign and analytics storage

---

## Best Practices & Recommendations

- **Never commit your `database.db` or lab/testing data to git.**  
  These are ignored by the included `.gitignore`.
- **Use only in a controlled, educational environment.**
- **Do not use for real-world phishing or malicious purposes.**
- **Customize templates to fit your organization’s awareness needs.**

---

## Troubleshooting

- **Emails not sending?** Ensure your SMTP server (Sendmail/Postfix) is set up and accessible.
- **Database errors?** The `database.db` file is auto-generated; if deleted, a fresh database will be created, but all old data will be lost.
- **UI issues?** Ensure all static files (CSS, images) are present and browser cache is cleared.

---

## Documentation & Report

- **`README.md`:** This file—setup, usage, and technical details.
- **`Report.pdf`:** A concise report (max two pages) describing the project, tools, design, and results.

---

## Contribution

1. Fork the repository
2. Create a new branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

---

## Acknowledgements

- Flask documentation
- SQLite documentation
- Open-source security and awareness resources
- All contributors to phishing simulation and security education tools

---

**Empower users. Raise awareness. Simulate safely.**

---

For questions or contributions, please open an issue or pull request!
