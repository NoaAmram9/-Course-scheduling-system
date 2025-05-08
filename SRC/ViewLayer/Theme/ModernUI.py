import tkinter as tk
from tkinter import ttk

class ModernUI:
    """Class with modern UI elements and styling"""
    
    # Color palette
    COLORS = {
        "primary": "#3499FF",     # Blue
        "secondary": "#36F6A9",   # Green
        "accent": "#FF1313",      # Red
        "light": "#ecf0f1",       # Light Gray
        "dark": "#2c3e50",        # Dark Blue/Gray
        "white": "#ffffff",       # White
        "gray": "#95a5a6",        # Medium Gray
        "selected": "#d5f5e3"     # Light Green for selected items
    }
    
    @staticmethod
    def create_rounded_button(parent, text, command, bg_color=None, fg_color=None, width=120, height=30):
        """Creates a custom canvas button with rounded corners"""
        if not bg_color:
            bg_color = ModernUI.COLORS["primary"]
        if not fg_color:
            fg_color = ModernUI.COLORS["white"]
            
        frame = tk.Frame(parent, bg=parent["bg"])
        canvas = tk.Canvas(frame, width=width, height=height, bg=parent["bg"], 
                         highlightthickness=0)
        canvas.pack()
        
        # Draw rounded rectangle
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
            smooth=True, **kwargs)
            
        button_shape = canvas.create_rounded_rectangle(0, 0, width, height, 15, 
                                                    fill=bg_color, outline="")
        button_text = canvas.create_text(width//2, height//2, text=text, 
                                       fill=fg_color, font=("Calibri", 10, "bold"))
        
        # Hover effects
        def on_enter(e):
            # Darken the button slightly on hover
            canvas.itemconfig(button_shape, fill=ModernUI.adjust_color(bg_color, -20))
            
        def on_leave(e):
            canvas.itemconfig(button_shape, fill=bg_color)
            
        def on_click(e):
            # Flash effect and execute command
            canvas.itemconfig(button_shape, fill=ModernUI.adjust_color(bg_color, -40))
            parent.after(100, lambda: canvas.itemconfig(button_shape, fill=bg_color))
            command()
            
        canvas.bind("<Enter>", on_enter)
        canvas.bind("<Leave>", on_leave)
        canvas.bind("<Button-1>", on_click)
        canvas.bind("<ButtonRelease-1>", on_leave)
        
        return frame
    
    @staticmethod
    def adjust_color(hex_color, amount):
        """Adjusts a hex color by the given amount (positive = lighter, negative = darker)"""
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        
        r = max(0, min(255, r + amount))
        g = max(0, min(255, g + amount))
        b = max(0, min(255, b + amount))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    @staticmethod
    def configure_treeview_style():
        """Configures a custom style for treeview"""
        style = ttk.Style()
        style.theme_use("clam")
        
        # Configure the Treeview colors
        style.configure("Treeview", 
                      background=ModernUI.COLORS["white"],
                      foreground=ModernUI.COLORS["dark"],
                      rowheight=25,
                      fieldbackground=ModernUI.COLORS["white"])
        
        # Change selected color
        style.map('Treeview', 
                background=[('selected', ModernUI.COLORS["primary"])],
                foreground=[('selected', ModernUI.COLORS["white"])])
        
        # Configure the header
        style.configure("Treeview.Heading",
                      background=ModernUI.COLORS["light"],
                      foreground=ModernUI.COLORS["dark"],
                      relief="flat",
                      font=('Calibri', 10, 'bold'))
        
        style.map("Treeview.Heading",
                background=[('active', ModernUI.COLORS["gray"])])