import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
from main import RealEstateChatbot

QUIZ_QUESTIONS = [
    {"q": "What's your maximum budget (EGP)?", "type": "numeric"},
    {"q": "How many bedrooms do you need?", "type": "choice", "choices": ["1", "2", "3+"]},
    {"q": "Preferred area(s)? (comma separated)", "type": "text"},
    {"q": "Are you looking for a new or resale unit?", "type": "choice", "choices": ["New", "Resale", "Doesn’t matter"]},
    {"q": "What's more important to you?", "type": "choice", "choices": ["Area size", "Price", "Location", "Amenities"]},
    {"q": "Preferred type?", "type": "choice", "choices": ["Apartment", "Villa", "Duplex", "Studio"]},
    {"q": "Minimum required amenities? (comma separated, e.g. Garden, Parking, Pool, Elevator)", "type": "text"},
    {"q": "What's your intended use?", "type": "choice", "choices": ["Living", "Investment", "Rental"]},
]

class RealEstateChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Real Estate Chatbot")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        self.chatbot = RealEstateChatbot()
        self.dark_mode = False
        self.create_widgets()
        self.set_light_mode()
        self.display_response("Welcome to the Real Estate Chatbot! Type your command or use the buttons below.")

    def create_widgets(self):
        # Title label
        self.title_label = tk.Label(self.root, text="🏠 Real Estate Chatbot", font=("Arial", 22, "bold"))
        self.title_label.pack(pady=10)

        # Output area
        self.output_area = scrolledtext.ScrolledText(self.root, width=110, height=18, state='disabled', wrap=tk.WORD, font=("Consolas", 12))
        self.output_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=False)

        # Input frame
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=5, fill=tk.X, padx=10)

        self.input_label = tk.Label(self.input_frame, text="Command:", font=("Arial", 12))
        self.input_label.pack(side=tk.LEFT, padx=(0, 5))

        self.input_entry = tk.Entry(self.input_frame, width=60, font=("Arial", 12))
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.input_entry.bind('<Return>', lambda event: self.process_command())

        self.submit_button = tk.Button(self.input_frame, text="Submit", command=self.process_command, font=("Arial", 12))
        self.submit_button.pack(side=tk.LEFT, padx=5)

        # Feature buttons frame
        self.feature_frame = tk.Frame(self.root)
        self.feature_frame.pack(pady=10)

        self.list_button = tk.Button(self.feature_frame, text="List All", command=lambda: self.quick_command("list"), width=14)
        self.list_button.grid(row=0, column=0, padx=5, pady=2)

        self.filter_button = tk.Button(self.feature_frame, text="Filter", command=self.filter_dialog, width=14)
        self.filter_button.grid(row=0, column=1, padx=5, pady=2)

        self.sort_button = tk.Button(self.feature_frame, text="Sort", command=self.sort_dialog, width=14)
        self.sort_button.grid(row=0, column=2, padx=5, pady=2)

        self.next_button = tk.Button(self.feature_frame, text="Next Page", command=lambda: self.quick_command("next"), width=14)
        self.next_button.grid(row=0, column=3, padx=5, pady=2)

        self.prev_button = tk.Button(self.feature_frame, text="Previous Page", command=lambda: self.quick_command("previous"), width=14)
        self.prev_button.grid(row=0, column=4, padx=5, pady=2)

        self.details_button = tk.Button(self.feature_frame, text="Details", command=self.details_dialog, width=14)
        self.details_button.grid(row=1, column=0, padx=5, pady=2)

        self.compare_button = tk.Button(self.feature_frame, text="Compare", command=self.compare_dialog, width=14)
        self.compare_button.grid(row=1, column=1, padx=5, pady=2)

        self.fav_button = tk.Button(self.feature_frame, text="Show Favorites", command=lambda: self.quick_command("show favorites"), width=14)
        self.fav_button.grid(row=1, column=2, padx=5, pady=2)

        self.add_fav_button = tk.Button(self.feature_frame, text="Add Favorite", command=self.add_favorite_dialog, width=14)
        self.add_fav_button.grid(row=1, column=3, padx=5, pady=2)

        self.remove_fav_button = tk.Button(self.feature_frame, text="Remove Favorite", command=self.remove_favorite_dialog, width=14)
        self.remove_fav_button.grid(row=1, column=4, padx=5, pady=2)

        # Add Top Matched button (distinct and visible)
        self.quiz_button = tk.Button(self.feature_frame, text="Top Matched", command=self.start_quiz, width=14, bg="#4caf50", fg="white", activebackground="#388e3c")
        self.quiz_button.grid(row=3, column=2, padx=5, pady=10)

        # Bottom buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=5)

        self.help_button = tk.Button(self.button_frame, text="Help", command=self.show_help, width=12)
        self.help_button.pack(side=tk.LEFT, padx=5)

        self.theme_button = tk.Button(self.button_frame, text="Dark Mode", command=self.toggle_theme, width=12)
        self.theme_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(self.button_frame, text="Clear", command=self.clear_output, width=12)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.exit_button = tk.Button(self.button_frame, text="Exit", command=self.root.quit, width=12)
        self.exit_button.pack(side=tk.LEFT, padx=5)

    def process_command(self):
        user_input = self.input_entry.get()
        if hasattr(self, "quiz_in_progress") and self.quiz_in_progress:
            answer = user_input.strip()
            if not answer:
                messagebox.showwarning("Quiz", "Please enter an answer.")
                return
            self.quiz_answers.append(answer)
            self.quiz_index += 1
            self.input_entry.delete(0, tk.END)
            self.ask_quiz_question_chatbox()
            return
        if user_input.strip():
            if user_input.strip().lower() == "start quiz":
                self.start_quiz()
                self.input_entry.delete(0, tk.END)
                return
            self.display_response(f"You: {user_input}")
            response = self.chatbot.process_input(user_input)
            self.display_response(f"Bot: {response}")
            self.input_entry.delete(0, tk.END)

    def quick_command(self, command):
        self.display_response(f"You: {command}")
        response = self.chatbot.process_input(command)
        self.display_response(f"Bot: {response}")

    def filter_dialog(self):
        filter_str = simpledialog.askstring("Filter", "Enter filter (e.g. filter bedrooms at least 3 price under 2000000):", parent=self.root)
        if filter_str:
            self.quick_command(filter_str)

    def sort_dialog(self):
        sort_str = simpledialog.askstring("Sort", "Enter sort (e.g. sort by price ascending):", parent=self.root)
        if sort_str:
            self.quick_command(sort_str)

    def details_dialog(self):
        idx = simpledialog.askinteger("Details", "Enter property number for details:", parent=self.root)
        if idx:
            self.quick_command(f"details {idx}")

    def compare_dialog(self):
        idx1 = simpledialog.askinteger("Compare", "Enter first property number:", parent=self.root)
        idx2 = simpledialog.askinteger("Compare", "Enter second property number:", parent=self.root)
        if idx1 and idx2:
            self.quick_command(f"compare {idx1} and {idx2}")

    def add_favorite_dialog(self):
        idx = simpledialog.askinteger("Add Favorite", "Enter property number to add to favorites:", parent=self.root)
        if idx:
            self.quick_command(f"favorite {idx}")

    def remove_favorite_dialog(self):
        idx = simpledialog.askinteger("Remove Favorite", "Enter favorite number to remove:", parent=self.root)
        if idx:
            self.quick_command(f"remove {idx} from favorites")

    def display_response(self, response):
        self.output_area.config(state='normal')
        self.output_area.insert(tk.END, f"{response}\n")
        self.output_area.config(state='disabled')
        self.output_area.yview(tk.END)

    def clear_output(self):
        self.output_area.config(state='normal')
        self.output_area.delete(1.0, tk.END)
        self.output_area.config(state='disabled')

    def show_help(self):
        help_message = self.chatbot.help_message()
        messagebox.showinfo("Help", help_message)

    def toggle_theme(self):
        if self.dark_mode:
            self.set_light_mode()
        else:
            self.set_dark_mode()

    def set_dark_mode(self):
        self.dark_mode = True
        self.root.configure(bg="#181818")
        self.title_label.config(bg="#181818", fg="#e0e0e0")
        self.output_area.config(bg="#23272e", fg="#e0e0e0", insertbackground="#e0e0e0")
        self.input_frame.config(bg="#181818")
        self.input_label.config(bg="#181818", fg="#e0e0e0")
        self.input_entry.config(bg="#23272e", fg="#e0e0e0", insertbackground="#e0e0e0")
        self.feature_frame.config(bg="#181818")
        self.button_frame.config(bg="#181818")
        for widget in self.feature_frame.winfo_children() + self.button_frame.winfo_children():
            widget.config(bg="#23272e", fg="#e0e0e0", activebackground="#388e3c", activeforeground="#e0e0e0")

    def set_light_mode(self):
        self.dark_mode = False
        self.root.configure(bg="#f0f0f0")
        self.title_label.config(bg="#f0f0f0", fg="#222222")
        self.output_area.config(bg="#ffffff", fg="#222222", insertbackground="#222222")
        self.input_frame.config(bg="#f0f0f0")
        self.input_label.config(bg="#f0f0f0", fg="#222222")
        self.input_entry.config(bg="#ffffff", fg="#222222", insertbackground="#222222")
        self.feature_frame.config(bg="#f0f0f0")
        self.button_frame.config(bg="#f0f0f0")
        for widget in self.feature_frame.winfo_children() + self.button_frame.winfo_children():
            widget.config(bg="#e0e0e0", fg="#222222", activebackground="#b2dfdb", activeforeground="#222222")

    # --- Top Matched Quiz Logic (all questions in chatbox) ---
    def start_quiz(self):
        self.quiz_answers = []
        self.quiz_index = 0
        self.quiz_in_progress = True
        self.display_response("Top Matched Quiz started! Please answer the following questions:")
        self.ask_quiz_question_chatbox()

    def ask_quiz_question_chatbox(self):
        if self.quiz_index >= len(QUIZ_QUESTIONS):
            self.quiz_in_progress = False
            self.finish_quiz()
            return
        q = QUIZ_QUESTIONS[self.quiz_index]
        display_text = f"Q{self.quiz_index+1}: {q['q']}"
        if q["type"] == "choice":
            display_text += f" (Choices: {', '.join(q['choices'])})"
        self.display_response(display_text)
        self.input_entry.delete(0, tk.END)
        self.input_entry.focus_set()

    def finish_quiz(self):
        matches = []
        for key, prop in self.chatbot.properties.items():
            score = 0
            # Q1: Budget
            try:
                if self.quiz_answers[0] and prop.price <= int(self.quiz_answers[0]):
                    score += 1
            except:
                pass
            # Q2: Bedrooms
            if self.quiz_answers[1]:
                if self.quiz_answers[1] == "3+" and prop.bedrooms >= 3:
                    score += 1
                elif self.quiz_answers[1].isdigit() and prop.bedrooms == int(self.quiz_answers[1]):
                    score += 1
            # Q3: Area/Location
            if self.quiz_answers[2]:
                areas = [a.strip().lower() for a in self.quiz_answers[2].split(",")]
                if any(area in prop.city.lower() or area in prop.compound.lower() for area in areas):
                    score += 1
            # Q4: New/Resale
            if self.quiz_answers[3]:
                if self.quiz_answers[3].lower() == "new" and ("ready" in prop.delivery_date.lower() or "202" in prop.delivery_date):
                    score += 1
                elif self.quiz_answers[3].lower() == "resale" and "ready" in prop.delivery_date.lower():
                    score += 1
                elif self.quiz_answers[3].lower() == "doesn’t matter":
                    score += 1
            # Q5: Key preference (boost score)
            if self.quiz_answers[4]:
                if self.quiz_answers[4].lower() == "area size" and prop.area >= 150:
                    score += 1
                elif self.quiz_answers[4].lower() == "price":
                    score += 1
                elif self.quiz_answers[4].lower() == "location":
                    score += 1
                elif self.quiz_answers[4].lower() == "amenities":
                    score += 1
            # Q6: Type
            if self.quiz_answers[5]:
                if self.quiz_answers[5].lower() in prop.type.lower():
                    score += 1
            # Q7: Amenities (not in data, so just skip or always +1)
            if self.quiz_answers[6]:
                score += 1
            # Q8: Intended use (not in data, so just skip or always +1)
            if self.quiz_answers[7]:
                score += 1
            matches.append((score, prop))

        matches.sort(key=lambda x: (-x[0], x[1].price))
        top_matches = matches[:3]
        if not top_matches or top_matches[0][0] == 0:
            self.display_response("Sorry, no properties match your preferences.")
            return

        msg = "🏅 Top property matches for you:\n"
        for i, (score, prop) in enumerate(top_matches, 1):
            msg += (
                f"\n{i}. {prop.compound} | {prop.type} | {prop.city}\n"
                f"   Price: {prop.price:,.0f} EGP | Bedrooms: {prop.bedrooms} | Area: {prop.area}m²\n"
                f"   Delivery: {prop.delivery_date} | Level: {prop.level}\n"
            )
        self.display_response(msg)
        self.display_response("You can retake the quiz anytime by clicking 'Top Matched'.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RealEstateChatbotGUI(root)
    root.mainloop()