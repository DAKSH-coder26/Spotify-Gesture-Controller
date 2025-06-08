# 🎵 Spotify Gesture Controller

Control Spotify playback using your hand ✋ and face 👤 gestures via webcam!  
Built with Python, OpenCV, MediaPipe, and Spotify Web API.

> 🔗 Live Auth Redirect Page:  
> https://daksh-coder26.github.io/Spotify-Gesture-Controller/

---

## 🚀 Features

- ✌️ Play: Index + Middle fingers up
- 🖐 Pause: All fingers up
- 🤙 Shuffle: Index + Pinky
- 👍 Volume Up
- 👎 Volume Down
- 👆 Like Song
- 👤 Swipe Head Right → Next Track
- 👤 Swipe Head Left → Previous Track

---

## 🛠️ Installation

### 1. Clone this repository

```bash
git clone https://github.com/DAKSH-coder26/Spotify-Gesture-Controller.git
cd Spotify-Gesture-Controller
```

### 2. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Spotify API Setup

### Step 1: Create a Spotify Developer App

1. Go to: https://developer.spotify.com/dashboard
2. Create a new app
3. Set Redirect URI to:

```
https://daksh-coder26.github.io/Spotify-Gesture-Controller/
```

### Step 2: Create a `.env` file

In the root directory:

```env
CLIENT_ID1=your_spotify_client_id
REDIRECT_URL=https://daksh-coder26.github.io/Spotify-Gesture-Controller/
```

> 🔒 Do NOT share your `.env` or include it in commits. It is already gitignored.

---

## ✅ Authentication

Run the Spotify login flow:

```bash
python spotify_auth.py
```

1. A browser window will open.
2. Log in to Spotify and allow access.
3. Copy the **full redirect URL** shown in the browser.
4. Paste it back into the terminal.

This generates a `token_info.json` file.

---

## ▶️ Run the Gesture Controller

```bash
python main.py
```

Press `Q` to quit.

---

## 📁 Project Structure

| File | Purpose |
|------|---------|
| `main.py` | Main loop: webcam + gesture detection + Spotify control |
| `gesture_detection.py` | MediaPipe-based hand & face gesture recognizer |
| `spotify_auth.py` | Spotify OAuth2 PKCE flow for token generation |
| `index.html` | Redirect handler for authentication (GitHub Pages) |
| `.env` | Environment secrets (gitignored) |
| `token_info.json` | Stores user tokens (gitignored) |

---

## 📷 Screenshots / Demo (Coming Soon)

> You can add a demo GIF or screenshot here!

---

## 📝 License

MIT License © 2025 Daksh Bajaj  
Feel free to fork, improve, and share!

---

## 🙌 Contributions & Support

Pull requests are welcome!  
For major changes, please open an issue first.  
Star ⭐ the repo if you found it useful!