#Name: Sravya Kodavatiganti
#Date: 10/21/2024
#Class: 601007
#App name: Movie Ticket Booking System
import tkinter as tk
from tkinter import messagebox, simpledialog, font

class MovieTicketBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Ticket Booking System")
        self.root.configure(bg="#f0f0f0")  # Light background color

        # Set a custom font
        self.custom_font = font.Font(family="Helvetica", size=12)

        # User input fields
        self.first_name_label = tk.Label(root, text="Please enter your first name:", bg="#f0f0f0", font=self.custom_font)
        self.first_name_label.pack(pady=5)
        self.first_name_entry = tk.Entry(root, font=self.custom_font)
        self.first_name_entry.pack(pady=5)

        self.last_name_label = tk.Label(root, text="Please enter your last name:", bg="#f0f0f0", font=self.custom_font)
        self.last_name_label.pack(pady=5)
        self.last_name_entry = tk.Entry(root, font=self.custom_font)
        self.last_name_entry.pack(pady=5)

        self.submit_button = tk.Button(root, text="Submit", command=self.greet_user, bg="#4CAF50", fg="white", font=self.custom_font)
        self.submit_button.pack(pady=10)

        self.movies = [
            {"title": "Avengers: Endgame", "genre": "Action", "price": 12.00, "available_tickets": 40},  
            {"title": "The Lion King", "genre": "Animation", "price": 10.00, "available_tickets": 100},
            {"title": "Joker", "genre": "Drama", "price": 15.00, "available_tickets": 50},
            {"title": "Frozen II", "genre": "Animation", "price": 10.00, "available_tickets": 100},
            {"title": "Spider-Man: Far From Home", "genre": "Action", "price": 12.00, "available_tickets": 100},
            {"title": "Toy Story 4", "genre": "Animation", "price": 10.00, "available_tickets": 100},
            {"title": "Inception", "genre": "Sci-Fi", "price": 14.00, "available_tickets": 30},
            {"title": "The Matrix", "genre": "Sci-Fi", "price": 13.00, "available_tickets": 20},
        ]

        self.user_first_name = None  # Store the user's first name
        self.user_last_name = None   # Store the user's last name
        self.movie_frame = None  # To hold movie selection widgets

    def greet_user(self):
        self.user_first_name = self.first_name_entry.get()
        self.user_last_name = self.last_name_entry.get()

        if not self.user_first_name or not self.user_last_name:
            messagebox.showerror("Input Error", "Please enter both your first and last names.")
            return

        greeting_message = f"Hello, {self.user_first_name} {self.user_last_name}! Welcome to the Movie Ticket Booking System."
        messagebox.showinfo("Welcome", greeting_message)
        # Set up the movie selection interface
        self.setup_movie_selection()

    def setup_movie_selection(self):
        if self.movie_frame is not None:
            self.movie_frame.destroy()  # Clear previous movie selection frame if it exists

        self.movie_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.movie_frame.pack(pady=10)

        self.movie_listbox = tk.Listbox(self.movie_frame, width=60, height=10, font=self.custom_font)
        for index, movie in enumerate(self.movies):
            movie_info = f"{index + 1}. {movie['title']} - Genre: {movie['genre']} - Price: ${movie['price']:.2f} - Available Tickets: {movie['available_tickets']}"
            self.movie_listbox.insert(tk.END, movie_info)
        self.movie_listbox.pack(pady=5)

        self.select_button = tk.Button(self.movie_frame, text="Select Movie (Enter number or first letter)", command=self.select_movie, bg="#2196F3", fg="white", font=self.custom_font)
        self.select_button.pack(pady=10)

    def select_movie(self):
        selection = simpledialog.askstring("Select Movie", "Enter the movie number or first letter of the title:")
        selected_movie = None

        if selection.isdigit():
            selected_index = int(selection) - 1
            if 0 <= selected_index < len(self.movies):
                selected_movie = self.movies[selected_index]
        else:
            selected_movie = next((movie for movie in self.movies if movie['title'].startswith(selection)), None)

        if selected_movie:
            if selected_movie['available_tickets'] > 0:
                self.show_ticket_booking(selected_movie)
            else:
                messagebox.showerror("Booking Error", "No available tickets for this movie. Please choose a different movie or number of tickets.")
                self.setup_movie_selection()  # Show the movie list again
        else:
            messagebox.showerror("Selection Error", "Invalid movie selection. Please try again.")
            self.setup_movie_selection()  # Show the movie list again

    def show_ticket_booking(self, selected_movie):
        self.ticket_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.ticket_frame.pack(pady=10)

        self.tickets_label = tk.Label(self.ticket_frame, text=f"You selected: {selected_movie['title']} - Genre: {selected_movie['genre']} - Price: ${selected_movie['price']:.2f}", bg="#f0f0f0", font=self.custom_font)
        self.tickets_label.pack(pady=5)

        self.tickets_entry = tk.Entry(self.ticket_frame, font=self.custom_font)
        self.tickets_entry.pack(pady=5)
        self.tickets_entry.insert(0, "Enter number of tickets")

        self.confirm_button = tk.Button(self.ticket_frame, text="Confirm Booking", command=lambda: self.confirm_booking(selected_movie), bg="#FF9800", fg="white", font=self.custom_font)
        self.confirm_button.pack(pady=10)

    def confirm_booking(self, selected_movie):
        try:
            tickets_requested = int(self.tickets_entry.get())
            if tickets_requested < 1:
                messagebox.showerror("Booking Error", "You must request at least one ticket.")
                return
            if tickets_requested > selected_movie['available_tickets']:
                messagebox.showerror("Booking Error", f"Only {selected_movie['available_tickets']} tickets are available. Please choose a different number.")
                return

            total_price = tickets_requested * selected_movie['price']
            selected_movie['available_tickets'] -= tickets_requested  # Update available tickets

            # Ask if the user wants to apply a coupon code
            apply_coupon = messagebox.askyesno("Coupon Code", "Do you have a coupon code? (5%, 10%, 15%)")
            discount = 0

            if apply_coupon:
                coupon_code = simpledialog.askstring("Coupon Code", "Enter your coupon code (5%, 10%, 15%):")
                if coupon_code == "5%":
                    discount = 0.05
                elif coupon_code == "10%":
                    discount = 0.10
                elif coupon_code == "15%":
                    discount = 0.15
                else:
                    messagebox.showinfo("Coupon Code", "Invalid coupon code. No discount applied.")

            total_price *= (1 - discount)  # Apply discount if valid
            final_message = f"You have successfully booked {tickets_requested} tickets for {selected_movie['title']}.\n"
            final_message += f"Total Price: ${total_price:.2f}\n"
            final_message += f"Thank you, {self.user_first_name} {self.user_last_name}, for using the Movie Ticket Booking System! We hope to see you again!"
            messagebox.showinfo("Booking Confirmed", final_message)

            # Clear the ticket booking frame
            self.ticket_frame.destroy()
            self.setup_movie_selection()  # Show the movie list again

        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number of tickets.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieTicketBookingApp(root)
    root.mainloop()