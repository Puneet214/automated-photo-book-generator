# 📸 Automated Photo Book Generator

## 📌 About the Project

This project generates a photo book (PDF) from a folder of images.
It organizes images automatically and creates a simple story-like layout.

The idea is to reduce manual effort in arranging photos and exporting them into a structured format.

---

## ⚙️ Features

* Reads images from a folder
* Extracts basic features from images
* Groups and arranges images
* Generates a PDF photo book

---

## 🛠️ Tech Used

* Python
* OpenCV (for image handling)
* Scikit-learn (for grouping)
* Pillow (for image processing)
* Typer (for CLI)

---

## ▶️ How to Run

1. Clone the repository:

```
git clone <your-repo-link>
cd <repo-name>
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Add images inside the `images/` folder

4. Run the project:

```
python main.py images --output-pdf output.pdf
```

---

## 📌 Notes

* Works best with `.jpg` and `.png` images
* Make sure Python 3.9+ is installed
* Output PDF will be generated in the same folder

---

## ✨ Author

Puneet
