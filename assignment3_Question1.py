import tkinter as tk
from tkinter import filedialog, Label, Text, Button
from PIL import Image, ImageTk
import tensorflow as tf
import numpy as np
from transformers import pipeline  # For language translation

# Base class for GUI setup
class GUIBase:
    def __init__(self, root):
        self.root = root
        self.setup_gui()

    def setup_gui(self):
        self.root.title("AI-Powered Application")
        self.root.geometry("600x600")

    def show_message(self, message):
        label = Label(self.root, text=message)
        label.pack()

    def open_file_dialog(self):
        return filedialog.askopenfilename()

# Base class for Image Classification functionalities
class ImageClassifier:
    def __init__(self):
        self._model = None

    @property
    def model(self):
        if self._model is None:
            self._model = tf.keras.applications.MobileNetV2(weights='imagenet')
        return self._model

    def prepare_image(self, img_path):
        image = tf.keras.preprocessing.image.load_img(img_path, target_size=(224, 224))
        image_array = tf.keras.preprocessing.image.img_to_array(image)
        image_array = np.expand_dims(image_array, axis=0)
        image_array = tf.keras.applications.mobilenet_v2.preprocess_input(image_array)
        return image_array

    def classify_image(self, image_array):
        predictions = self.model.predict(image_array)
        decoded = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=1)[0]
        return decoded[0][1]  # Get the label of the top prediction

# Base class for Language Translation functionalities
class Translator:
    def __init__(self):
        self.translation_pipeline = pipeline("translation_en_to_fr")

    def translate(self, text):
        translation_result = self.translation_pipeline(text)
        return translation_result[0]['translation_text']

# Multi-functional class inheriting from GUIBase, ImageClassifier, and Translator
class AIApp(GUIBase, ImageClassifier, Translator):
    def __init__(self, root):
        GUIBase.__init__(self, root)
        ImageClassifier.__init__(self)
        Translator.__init__(self)

        # UI Elements
        self.setup_widgets()

    def setup_widgets(self):
        # Application header
        self.show_message("AI-Powered Application: Image Classification & Translation")

        # Image classification section
        self.upload_button = Button(self.root, text="Upload Image for Classification", command=self.classify_uploaded_image)
        self.upload_button.pack()

        self.classification_result = Label(self.root, text="Upload an image to classify.")
        self.classification_result.pack()

        # Language translation section
        self.input_text_box = Text(self.root, height=5, width=50)
        self.input_text_box.pack()

        self.translate_button = Button(self.root, text="Translate to French", command=self.translate_text)
        self.translate_button.pack()

        self.translation_result_label = Label(self.root, text="Enter text for translation.")
        self.translation_result_label.pack()

    def classify_uploaded_image(self):
        file_path = self.open_file_dialog()
        if file_path:
            image_array = self.prepare_image(file_path)
            classification_result = self.classify_image(image_array)
            self.classification_result.config(text=f"Prediction: {classification_result}")

    def translate_text(self):
        input_text = self.input_text_box.get("1.0", tk.END).strip()
        if input_text:
            translated_text = self.translate(input_text)
            self.translation_result_label.config(text=f"Translated: {translated_text}")

# Main execution for running the application
if __name__ == "__main__":
    root = tk.Tk()
    app = AIApp(root)
    root.mainloop()
