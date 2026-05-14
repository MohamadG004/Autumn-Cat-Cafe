# 🍂 Autumn Cat Café

A cozy idle café management game built with Python + pygame.

```
  /\_/\       AUTUMN CAT CAFÉ
 ( >O.O< )    秋のカフェ
  > ⌒ <      
```

---

## ✨ Features

- 🐱 **Animated black cat barista** – blinks, wags tail, bobs gently
- 🍂 **Falling autumn leaves** – particle system with rotation & drift
- 🏮 **Japanese café aesthetic** – lanterns, banners, カフェ signs
- 💴 **Idle income system** – earn ¥ per second, watch it grow
- 🛒 **5 upgrades** with increasing cost and income bonuses
- 🧑 **Chibi customer walk-ins** – tiny guests bring bonus yen
- ✨ **Floating money text** & **screen shake** on purchases
- 🔊 **Procedural audio** – click, coin, and upgrade sounds

---

## 🛠️ Installation

### 1. Clone / unzip the project
```bash
cd AutumnCatCafe
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```
> `numpy` is optional – audio still works without it (silently disabled).  
> `Pillow` is optional – used only for pre-generating PNG sprites.

### 3. Run the game
```bash
python main.py
```

---

## 🎮 Controls

| Input | Action |
|-------|--------|
| **Left-click** upgrade button | Purchase upgrade |
| **Hover** over button | Preview cost & highlight |
| **ESC** | Quit |

---

## 📐 Project Structure

```
AutumnCatCafe/
├── main.py               ← Entry point
├── settings.py           ← Constants (colours, layout, gameplay)
├── generate_assets.py    ← Pillow asset generator (optional)
├── requirements.txt
├── README.md
│
├── src/
│   ├── game.py           ← Game loop & state
│   ├── renderer.py       ← All procedural drawing
│   ├── ui.py             ← Button classes
│   ├── upgrades.py       ← Upgrade definitions
│   ├── customer.py       ← Walk-in customer system
│   ├── particles.py      ← Leaves + floating text
│   ├── animations.py     ← Cat animator & screen shake
│   ├── audio.py          ← Tone generation
│   └── utils.py          ← Fonts, drawing helpers
│
└── assets/               ← Generated PNG sprites (optional)
    ├── characters/
    ├── backgrounds/
    ├── ui/
    ├── icons/
    ├── particles/
    ├── audio/
    └── decorations/
```

---

## 🍵 Upgrades

| Upgrade | Base Cost | Income Boost |
|---------|-----------|-------------|
| Chochin Lantern | ¥500 | +0.5/sec |
| Espresso Machine | ¥2,000 | +2.0/sec |
| More Seating | ¥5,000 | +5.0/sec |
| Premium Beans | ¥15,000 | +15.0/sec |
| Lucky Cat Statue | ¥50,000 | +50.0/sec |

Each upgrade scales ×1.6 per level.

---

## 🎨 Art Style

All visuals are **procedurally generated** using `pygame.draw` primitives –  
no external image files are required to run the game.

Palette: warm autumn tones – cream, maroon, golden, rust orange.

---

*Made with ❤️ and lots of ☕*