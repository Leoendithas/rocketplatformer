# Rocket Platformer (Sky Navigator)

A small **Pygame** arcade platformer where you pilot a plane through an asteroid field, manage battery life, collect fuel and stars, and race to the finish line across **5 levels**.

<img width="1099" height="828" alt="image" src="https://github.com/user-attachments/assets/743c0eca-19be-4303-85d5-85ebf7003427" />
<img width="1105" height="825" alt="image" src="https://github.com/user-attachments/assets/811a747f-8db0-4747-95af-315caa086769" />


> Entry point: `app2.py`

---

## Gameplay

You control a plane flying through a side-scrolling level filled with:

- **Asteroids** (hazards): hitting one damages your battery and removes that asteroid.
- **Fuel canisters**: recharge your battery.
- **Stars**: bonus points.
- **Finish line**: reach it to complete the level (beat Level 5 to win).

### Win / lose conditions

You lose if:
- Your plane touches the **bottom** of the screen (crash), or
- Your **battery drains to 0** over time.

You win if:
- You reach the finish line on **Level 5**.

---

## Controls

- **↑**: move up (thrust against gravity)
- **↓**: move down faster
- **→**: speed up (adds forward velocity)
- **←**: slow down
- **SPACE**: start / next level / restart
- **ESC**: quit

---

## Scoring

- **+10 points / second** (time survived)
- **+100 points / star**

---

## Battery system

- Battery starts at **100**
- Drains over time (**1 per second**)
- Hitting an asteroid: **-20 battery** (with a short collision cooldown)
- Collecting fuel: **+30 battery** (capped at 100)

---

## Levels & difficulty

- Total levels: **5**
- More obstacles spawn as levels increase.
- From **Level 3 onward**, some asteroids **move** (oscillate side-to-side).
- Scroll speed increases slightly with each level.

---

## Quick start

### 1) Install
```bash
git clone https://github.com/Leoendithas/rocketplatformer.git
cd rocketplatformer

python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
````

> If `pygame` isn’t included in your `requirements.txt`, install it manually:
>
> ```bash
> pip install pygame
> ```

### 2) Run

```bash
python app2.py
```

---

## Notes

* Sprites are embedded directly in `app2.py` using base64-encoded SVGs, so the game runs without external image files.
* The repo includes `Background.mp3`, but the current script does not play music yet. (Easy upgrade: initialize `pygame.mixer` and load/play the file.)

---

## License

Licensed under the **Apache License 2.0**. See the `LICENSE` file for details.
