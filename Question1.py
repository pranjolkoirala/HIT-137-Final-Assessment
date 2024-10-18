import tkinter as tk
from tkinter import ttk, messagebox
from transformers import MarianMTModel, MarianTokenizer

# Base Class for Model and GUI
class TranslatorModel:
    def __init__(self, src_lang="en", tgt_lang="fr"):
        # Model and tokenizer are encapsulated as private variables
        self._src_lang = src_lang
        self._tgt_lang = tgt_lang
        self._model_name = f'Helsinki-NLP/opus-mt-{self._src_lang}-{self._tgt_lang}'
        
        self._model = MarianMTModel.from_pretrained(self._model_name)
        self._tokenizer = MarianTokenizer.from_pretrained(self._model_name)

    # Encapsulation: Translation functionality is hidden and secured within the class
    def _translate(self, text):
        # Tokenization
        tokens = self._tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        # Translation
        translated = self._model.generate(**tokens)
        # Decoding
        return self._tokenizer.decode(translated[0], skip_special_tokens=True)

class TkinterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Language Translation App")
        self.root.geometry("500x400")

    def start_app(self):
        raise NotImplementedError("Subclasses should implement this method")

# Multiple Inheritance: TranslatorApp inherits from both TranslatorModel and TkinterApp
class TranslatorApp(TranslatorModel, TkinterApp):
    def __init__(self, root, src_lang="en", tgt_lang="fr"):
        TranslatorModel.__init__(self, src_lang, tgt_lang)  # Initializing TranslatorModel
        TkinterApp.__init__(self, root)  # Initializing TkinterApp

    # Polymorphism: Override start_app() to implement specific GUI functionality
    def start_app(self):
        self.label = ttk.Label(self.root, text="Enter text to translate:")
        self.label.pack(pady=10)

        self.input_text = tk.Text(self.root, height=5, width=50)
        self.input_text.pack(pady=10)

        self.translate_button = ttk.Button(self.root, text="Translate", command=self._handle_translation)
        self.translate_button.pack(pady=10)

        self.output_label = ttk.Label(self.root, text="Translation:")
        self.output_label.pack(pady=10)

        self.output_text = tk.Text(self.root, height=5, width=50)
        self.output_text.pack(pady=10)

    # Decorator: Limit execution of translation (Example use of decorators)
    def log_translation(func):
        def wrapper(self, *args, **kwargs):
            print(f"Translating text at: {args}")
            return func(self, *args, **kwargs)
        return wrapper

    # Overriding _translate method and adding decorator for logging
    @log_translation
    def _handle_translation(self):
        input_text = self.input_text.get("1.0", tk.END).strip()

        if not input_text:
            messagebox.showwarning("Input Error", "Please enter some text!")
            return

        try:
            translated_text = self._translate(input_text)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, translated_text)
        except Exception as e:
            messagebox.showerror("Translation Error", str(e))

# Application Execution
if __name__ == "__main__":
    root = tk.Tk()
    app = TranslatorApp(root, src_lang="en", tgt_lang="fr")  # You can switch languages as needed
    app.start_app()
    root.mainloop()
