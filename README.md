# 🐺📖 Interactive Storytelling with Chainlit & Mistral

Welcome to your **interactive storytelling adventure**! 🚀 This project lets you explore a rich fantasy world where you interact with a **magical crow**, a **mercenary wolf**, and a **mysterious narrator**. You can influence the story by chatting with these characters and making choices!

## ✨ Features
- **Dynamic AI Characters**: Engage with the Crow, Wolf, and Narrator, each with unique personalities and dialogue styles.
- **Streaming Responses**: Real-time storytelling powered by Mistral 7B running locally via LM Studio.
- **Character-Driven Interaction**: Use `@crow` or `@wolf` to address your companions.
- **Customizable AI Behavior**: Modify `cast_of_characters.py` to tweak character personalities and responses.
- **Interactive Adventure**: Start in the Black Woods, tracking a mystical creature. What happens next is up to you! 🌲🔮

---

## 🛠 Installation & Setup

### 1️⃣ Install Dependencies
Make sure you have **Python 3.9+** installed in your system or in a [virtual enviroment](https://realpython.com/python-virtual-environments-a-primer/#how-can-you-work-with-a-python-virtual-environment). Then, install the required packages:
```bash
pip install -r requirements.txt
```

### 2️⃣ Run LM Studio
This project uses **LM Studio** to serve the Mistral model locally. Download and install [LM Studio](https://lmstudio.ai/), download mistral-7b-instruct-v0.3 from the 🔍discover tab of LM Studio, then start the server at the ▶️ developer tab:
```
http://localhost:1234/v1/completions
```
![image](https://github.com/user-attachments/assets/a212c3b0-3681-410d-9e90-1f795f14d65a)


### 3️⃣ Launch the Chainlit App
Run the interactive storytelling app with:
```bash
chainlit run app.py
```
Your chat adventure will open in a browser tab! 🏹📜

---

## 🗣 How to Play
- Start the story and read the **narrator’s introduction**.
- Chat with characters by mentioning them: `@crow` or `@wolf`.
- Make decisions that shape the journey.
- Watch the AI **stream responses in real-time**!

💡 *Pro Tip:* You can modify character behavior in `cast_of_characters.py`.

---

## 🔧 Advanced Configuration
Want to customize the storytelling experience? Try these:
- **Modify the Story Opening**: Edit `story.py` to change how the adventure begins.
- **Adjust AI Personalities**: Change attributes in `cast_of_characters.py`.
- **Fine-Tune Responses**: Implement text analysis in `app.py` to process dialogue.

---

## 🛠 Troubleshooting
❌ **Issue:** "Connection refused at localhost:1234"  
✅ **Solution:** Ensure LM Studio is running and serving the API.

❌ **Issue:** "Characters not responding properly"  
✅ **Solution:** Check `cast_of_characters.py` for errors in character definitions.

❌ **Issue:** "Chainlit not launching"  
✅ **Solution:** Ensure `chainlit` is installed (`pip show chainlit`) and restart the app.

---

## 💬 Join the Community
Need help or want to share your adventure? Join the [Chainlit Discord](https://discord.gg/k73SQ3FyUh)!

Happy storytelling! 🎭📚

