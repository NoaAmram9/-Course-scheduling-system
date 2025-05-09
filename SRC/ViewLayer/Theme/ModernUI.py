import tkinter as tk
from tkinter import ttk

class ModernUI:
    """Class providing modern UI styling and components for Tkinter GUIs."""

    # === Soft Pastel Color Palette ===
    COLORS = {
        "primary": "#398677",     # Muted blue
        "secondary": "#5de89c",   # Muted mint green
        "accent": "#e75e5e",      # Soft coral red
        "light": "#ebebeb",       # Soft light gray white!!
        "dark": "#2C3E50",        # Deep navy/gray
        "white": "#F9FAFB",       # Off-white
        "gray": "#A0A0A0",        # Medium gray
        "selected": "#B5EAD7"     # Soft green for selection
    }

    @staticmethod
    def create_rounded_button(parent, text, command, bg_color=None, fg_color=None, width=120, height=30):
        """Creates a rounded rectangle button using Canvas with hover and click effects."""
        if not bg_color:
            bg_color = ModernUI.COLORS["primary"]
        if not fg_color:
            fg_color = ModernUI.COLORS["white"]

        # Outer frame holds the canvas
        frame = tk.Frame(parent, bg=parent["bg"])

        # Canvas is used to draw a custom rounded shape
        canvas = tk.Canvas(
            frame, width=width, height=height,
            bg=parent["bg"], highlightthickness=0
        )
        canvas.pack()

        # Lambda to draw a rounded rectangle manually
        canvas.create_rounded_rectangle = lambda x1, y1, x2, y2, radius, **kwargs: canvas.create_polygon(
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1,
            smooth=True, **kwargs
        )

        # Draw button shape and text
        button_shape = canvas.create_rounded_rectangle(0, 0, width, height, 15, fill=bg_color, outline="")
        button_text = canvas.create_text(width // 2, height // 2, text=text, fill=fg_color, font=("Calibri", 10, "bold"))

        # === Hover and Click Effects ===
        def on_enter(e):
            canvas.itemconfig(button_shape, fill=ModernUI.adjust_color(bg_color, -5))  # Darker on hover

        def on_leave(e):
            canvas.itemconfig(button_shape, fill=bg_color)

        def on_click(e):
            # Click flash effect and trigger command
            canvas.itemconfig(button_shape, fill=ModernUI.adjust_color(bg_color, -15))
            parent.after(100, lambda: canvas.itemconfig(button_shape, fill=bg_color))
            command()

        # Bind mouse events
        canvas.bind("<Enter>", on_enter)
        canvas.bind("<Leave>", on_leave)
        canvas.bind("<Button-1>", on_click)
        canvas.bind("<ButtonRelease-1>", on_leave)

        return frame

    @staticmethod
    def adjust_color(hex_color, amount):
        """Adjusts brightness of a hex color by a given amount."""
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)

        # Clamp values between 0 and 255
        r = max(0, min(255, r + amount))
        g = max(0, min(255, g + amount))
        b = max(0, min(255, b + amount))

        return f"#{r:02x}{g:02x}{b:02x}"

    @staticmethod
    def configure_treeview_style():
        """Applies a modern pastel style to ttk Treeview widgets."""
        style = ttk.Style()
        style.theme_use("clam")  # More customizable than 'default' or 'vista'

        # General treeview appearance
        style.configure("Treeview",
                        background=ModernUI.COLORS["white"],
                        foreground=ModernUI.COLORS["dark"],
                        rowheight=25,
                        fieldbackground=ModernUI.COLORS["white"])

        # Selected row colors
        style.map("Treeview",
                  background=[("selected", ModernUI.COLORS["primary"])],
                  foreground=[("selected", ModernUI.COLORS["dark"])])

        # Header styling
        style.configure("Treeview.Heading",
                        background=ModernUI.COLORS["light"],
                        foreground=ModernUI.COLORS["dark"],
                        relief="flat",
                        font=('Calibri', 10, 'bold'))

        style.map("Treeview.Heading",
                  background=[("active", ModernUI.COLORS["white"])])
