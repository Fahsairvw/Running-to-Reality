import tkinter as tk
from tkinter import font, ttk
from game import Game
import pygame as pg
from game_component import SelectedMenu
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from config import Config


class Stat:
    def __init__(self):
        """Initialize with game data from CSV"""
        self.__df = pd.read_csv('game_results.csv')

    def pie_chart(self, figure_size=(5, 4)):
        """Create a pie chart of theme distribution"""
        pie_df = self.__df.copy()
        theme_counts = pie_df['Theme'].value_counts()
        color_arr = Config.PALETTE

        fig, ax = plt.subplots(figsize=figure_size)
        slices, texts, numbers = ax.pie(theme_counts,
                                        colors=color_arr,
                                        labels=theme_counts.index,
                                        startangle=90, counterclock=False,
                                        autopct='%1.2f%%',
                                        textprops={'color': 'w'})
        ax.set_title('Selected Theme')
        ax.legend(slices,
                  theme_counts.index,
                  title="Themes",
                  bbox_to_anchor=(1, 1))
        return fig

    def boxplot(self, figure_size=(5, 4)):
        """Create a boxplot of scores by theme"""
        fig, ax = plt.subplots(figsize=figure_size)
        sns.boxplot(x='Score', hue='Theme', data=self.__df, palette=Config.PALETTE, ax=ax)
        plt.title('Score by Theme')
        return fig

    def histogram(self, figure_size=(5, 4)):
        """Create a histogram of total jumps"""
        fig, ax = plt.subplots(figsize=figure_size)
        self.__df['Total Jump'].hist(color=Config.PALETTE[0], ax=ax)
        plt.title('Distribution of Total Jumps')
        return fig

    def scatter_plot(self, figure_size=(5, 4)):
        """Create a scatter plot of jumps vs time played"""
        fig, ax = plt.subplots(figsize=figure_size)
        sns.scatterplot(data=self.__df,
                        x="Total Jump",
                        y="Time Played",
                        hue="Theme",
                        palette=Config.PALETTE,
                        ax=ax)
        plt.title('Relationship between Jumps and Time Played')
        return fig

    def descriptive(self):
        """Get descriptive statistics for selected columns"""
        display_list = ['Total Jump', 'Score', 'Level']
        return self.__df[display_list].describe()

    def get_dataframe(self):
        """Return the dataframe for direct access"""
        return self.__df


class GameMenu:
    def __init__(self, root):
        self.__root = root
        self.__root.title("Runner Game Menu")
        self.__root.geometry("600x500")
        self.__root.resizable(True, True)

        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)

        self.__main_container = tk.Frame(root, bg="white")
        self.__main_container.grid(row=0, column=0, sticky="nsew")

        self.__main_container.grid_rowconfigure(0, weight=1)
        self.__main_container.grid_columnconfigure(1, weight=1)

        self.__frame = tk.Frame(self.__main_container, bg="white", width=50)
        self.__frame.grid(row=0, column=0, sticky="ns")

        self.__main_frame = tk.Frame(self.__main_container, bg="white")
        self.__main_frame.grid(row=0, column=1, sticky="nsew")

        self.__frame2 = tk.Frame(self.__main_container, bg="white", width=50)
        self.__frame2.grid(row=0, column=2, sticky="ns")

        self.__main_frame.grid_rowconfigure(0, weight=1)
        self.__main_frame.grid_rowconfigure(1, weight=1)
        self.__main_frame.grid_rowconfigure(2, weight=1)
        self.__main_frame.grid_rowconfigure(3, weight=1)
        self.__main_frame.grid_columnconfigure(0, weight=1)

        self.__stat = Stat()

        self.__root.protocol("WM_DELETE_WINDOW", self.exit_game)

        title_font = font.Font(family="Arial", size=24, weight="bold")
        self.__title_label = tk.Label(
            self.__main_frame,
            text="Running to Reality",
            font=title_font,
            bg="white",
            fg="black"
        )
        self.__title_label.grid(row=0, column=0, pady=30, sticky="nsew")

        button_style = {
            "font": ("Arial", 16, "bold"),
            "bg": "white",
            "fg": "black",
            "relief": tk.RAISED,
            "borderwidth": 2,
            "padx": 20,
            "pady": 10
        }

        self.__play_button = tk.Button(
            self.__main_frame,
            text="PLAY GAME",
            command=self.start_game,
            **button_style
        )
        self.__play_button.grid(row=1, column=0, pady=20, sticky="nsew")

        self.__statistic_button = tk.Button(
            self.__main_frame,
            text="Statistic Page",
            command=self.show_stat,
            **button_style
        )
        self.__statistic_button.grid(row=2, column=0, pady=20, sticky="nsew")

        self.__exit_button = tk.Button(
            self.__main_frame,
            text="Exit",
            command=self.exit_game,
            **button_style
        )
        self.__exit_button.grid(row=3, column=0, pady=20, sticky="nsew")

        self.__stat_windows = []
        self.__active_figures = []

    def start_game(self):
        """linking to selecting theme page"""
        self.__root.withdraw()

        try:
            pg.init()
            menu = SelectedMenu()

            running = True
            while running:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.__root.deiconify()
                        pg.quit()
                        return

                    menu.handle_events(event)

                menu.draw_menu()
                pg.display.update()

                if menu.selected_theme:
                    running = False

            selected_theme = menu.selected_theme

            game = Game()
            game.set_theme(selected_theme)
            game.run()

        except Exception as e:
            print(f"Error during game: {e}")
        finally:
            print("Returning to main menu")
            self.__root.deiconify()
            try:
                pg.quit()
            except:
                pass

    def exit_game(self):
        """Properly clean up and exit the game"""
        for window in self.__stat_windows:
            if window.winfo_exists():
                window.destroy()

        for fig in self.__active_figures:
            plt.close(fig)

        try:
            pg.quit()
        except:
            pass

        self.__root.destroy()
        print("Game exited properly")

    def show_stat(self):
        """Open statistics in a new popup window"""
        stat_window = tk.Toplevel(self.__root)
        stat_window.title("Game Statistics")
        stat_window.geometry("800x600")
        stat_window.configure(bg="white")

        self.__stat_windows.append(stat_window)

        stat_window.grid_rowconfigure(0, weight=1)
        stat_window.grid_columnconfigure(0, weight=1)

        stat_window.protocol("WM_DELETE_WINDOW",
                             lambda: self.close_stat_window(stat_window))

        notebook = ttk.Notebook(stat_window)
        notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        desc_stats_frame = tk.Frame(notebook, bg="white")
        notebook.add(desc_stats_frame, text="Descriptive Statistics")

        desc_stats_frame.grid_rowconfigure(0, weight=0)  # Title
        desc_stats_frame.grid_rowconfigure(1, weight=1)  # Table frame
        desc_stats_frame.grid_rowconfigure(2, weight=0)  # Explanation
        desc_stats_frame.grid_columnconfigure(0, weight=1)

        story_frame = tk.Frame(notebook, bg="white")
        notebook.add(story_frame, text="Visualizations")

        story_frame.grid_rowconfigure(0, weight=1)
        story_frame.grid_columnconfigure(0, weight=1)

        self.populate_descriptive_stats(desc_stats_frame)

        self.populate_storytelling(story_frame)

        close_button = tk.Button(
            stat_window,
            text="Close",
            command=lambda: self.close_stat_window(stat_window),
            font=("Arial", 12, "bold"),
            bg="white",
            fg="black",
            relief=tk.RAISED,
            borderwidth=2,
            padx=10,
            pady=5
        )
        close_button.grid(row=1, column=0, pady=10)

    def close_stat_window(self, window):
        """Properly close a statistics window and clean up resources"""
        if window in self.__stat_windows:
            self.__stat_windows.remove(window)

        for fig in self.__active_figures:
            plt.close(fig)
        self.__active_figures = []

        try:
            window.unbind_all("<MouseWheel>")
        except:
            pass

        window.destroy()

    def populate_descriptive_stats(self, frame):
        """Fill the descriptive statistics tab with content"""
        title_label = tk.Label(
            frame,
            text="Descriptive Statistics",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="black"
        )
        title_label.grid(row=0, column=0, pady=20)

        desc_stats = self.__stat.descriptive()

        table_frame = tk.Frame(frame, bg="white")
        table_frame.grid(row=1, column=0, sticky="nsew", padx=20)

        table_canvas = tk.Canvas(table_frame, bg="white")
        table_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=table_canvas.xview)
        scrollable_table = tk.Frame(table_canvas, bg="white")

        scrollable_table.bind(
            "<Configure>",
            lambda e: table_canvas.configure(
                scrollregion=table_canvas.bbox("all")
            )
        )

        table_canvas.create_window((0, 0), window=scrollable_table, anchor="nw")
        table_canvas.configure(xscrollcommand=table_scrollbar.set)

        table_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        table_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        df = desc_stats

        header_style = {
            "font": ("Arial", 11, "bold"),
            "bg": "#4a7abc",
            "fg": "white",
            "padx": 10,
            "pady": 5,
            "borderwidth": 1,
            "relief": "raised"
        }

        cell_style = {
            "font": ("Arial", 10),
            "bg": "white",
            "fg": "black",
            "padx": 10,
            "pady": 5,
            "borderwidth": 1,
            "relief": "sunken"
        }

        alt_cell_style = {
            "font": ("Arial", 10),
            "bg": "#f0f0f0",
            "fg": "black",
            "padx": 10,
            "pady": 5,
            "borderwidth": 1,
            "relief": "sunken"
        }

        row_header_style = {
            "font": ("Arial", 10, "bold"),
            "bg": "#e6e6e6",
            "fg": "black",
            "padx": 10,
            "pady": 5,
            "borderwidth": 1,
            "relief": "raised",
            "anchor": "w"
        }

        tk.Label(scrollable_table, text="", **header_style).grid(row=0, column=0, sticky="nsew")
        for j, col in enumerate(df.columns):
            tk.Label(scrollable_table, text=col, **header_style).grid(row=0, column=j + 1, sticky="nsew")

        for i, idx in enumerate(df.index):
            tk.Label(scrollable_table, text=idx, **row_header_style).grid(row=i + 1, column=0, sticky="nsew")

            style = cell_style if i % 2 == 0 else alt_cell_style
            for j, col in enumerate(df.columns):
                value = df.loc[idx, col]
                if isinstance(value, float):
                    value = f"{value:.2f}"
                tk.Label(scrollable_table, text=value, **style).grid(row=i + 1, column=j + 1, sticky="nsew")

        explanation_frame = tk.Frame(frame, bg="white")
        explanation_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=20)

        explanation_frame.grid_columnconfigure(0, weight=1)

        explanation_text = """
• Total Jump: Number of jumps performed during gameplay
• Score: Points accumulated during gameplay
• Level: Difficulty levels reached

Statistics shown include count (number of games), mean (average), standard deviation (std),
minimum values (min), quartiles (25%, 50%, 75%), and maximum values (max).
        """

        explanation_label = tk.Label(
            explanation_frame,
            text=explanation_text,
            font=("Arial", 11),
            bg="white",
            fg="black",
            justify=tk.LEFT,
            anchor="w"
        )
        explanation_label.grid(row=0, column=0, sticky="w")

    def populate_storytelling(self, frame):
        """Show graphs in the storytelling tab with button selection"""
        main_frame = tk.Frame(frame, bg="white")
        main_frame.grid(row=0, column=0, sticky="nsew")

        main_frame.grid_rowconfigure(0, weight=0)  # Button frame
        main_frame.grid_rowconfigure(1, weight=1)  # Graph frame
        main_frame.grid_columnconfigure(0, weight=1)

        button_frame = tk.Frame(main_frame, bg="white")
        button_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)

        graph_frame = tk.Frame(main_frame, bg="white", highlightbackground="#ddd", highlightthickness=1)
        graph_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        graph_frame.grid_rowconfigure(0, weight=1)
        graph_frame.grid_columnconfigure(0, weight=1)

        self.empty_label = tk.Label(
            graph_frame,
            text="Select a graph type using the buttons above",
            font=("Arial", 14),
            bg="white"
        )
        self.empty_label.grid(row=0, column=0)

        self.graph_canvases = {}

        button_style = {
            "font": ("Arial", 10, "bold"),
            "bg": "#4a7abc",
            "fg": "black",
            "padx": 15,
            "pady": 5,
            "borderwidth": 1,
            "relief": "raised",
        }

        graphs = [
            ("1. Theme Distribution", self.create_pie_chart),
            ("2. Scores by Theme", self.create_boxplot),
            ("3. Jump Distribution", self.create_histogram),
            ("4. Jumps vs Time", self.create_scatter_plot)
        ]

        for i, (text, command) in enumerate(graphs):
            btn = tk.Button(
                button_frame,
                text=text,
                command=lambda cmd=command, frm=graph_frame: self.show_graph(cmd, frm),
                **button_style
            )
            btn.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            button_frame.grid_columnconfigure(i, weight=1)

    @staticmethod
    def show_graph(graph_creator_func, frame):
        """Show a graph based on button selection"""
        for widget in frame.winfo_children():
            widget.grid_forget()

        graph_creator_func(frame)

    def create_pie_chart(self, frame):
        """Create and display pie chart in frame"""
        pie_fig = self.__stat.pie_chart(figure_size=(8, 6))
        self.__active_figures.append(pie_fig)

        pie_canvas = FigureCanvasTkAgg(pie_fig, master=frame)
        pie_canvas.draw()
        pie_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        title = tk.Label(
            frame,
            text="Theme Proportion",
            font=("Arial", 14, "bold"),
            bg="white"
        )
        title.grid(row=1, column=0, pady=5)

        explanation = tk.Label(
            frame,
            text="This chart shows the proportion of theme selection across all games.",
            font=("Arial", 11),
            bg="white",
            wraplength=500
        )
        explanation.grid(row=2, column=0, pady=5)

    def create_boxplot(self, frame):
        """Create and display boxplot in frame"""
        box_fig = self.__stat.boxplot(figure_size=(8, 6))
        self.__active_figures.append(box_fig)

        box_canvas = FigureCanvasTkAgg(box_fig, master=frame)
        box_canvas.draw()
        box_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        title = tk.Label(
            frame,
            text="Score Distribution by Theme",
            font=("Arial", 14, "bold"),
            bg="white"
        )
        title.grid(row=1, column=0, pady=5)

        explanation = tk.Label(
            frame,
            text="This boxplot shows the distribution of scores across different themes. " +
                 "The box represents the middle 50% of scores, while the whiskers show the range.",
            font=("Arial", 11),
            bg="white",
            wraplength=500
        )
        explanation.grid(row=2, column=0, pady=5)

    def create_histogram(self, frame):
        """Create and display histogram in frame"""
        hist_fig = self.__stat.histogram(figure_size=(8, 6))
        self.__active_figures.append(hist_fig)

        hist_canvas = FigureCanvasTkAgg(hist_fig, master=frame)
        hist_canvas.draw()
        hist_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Add title
        title = tk.Label(
            frame,
            text="Distribution of Total Jumps",
            font=("Arial", 14, "bold"),
            bg="white"
        )
        title.grid(row=1, column=0, pady=5)

        explanation = tk.Label(
            frame,
            text="This histogram shows the frequency distribution of total jumps across all games. " +
                 "The x-axis shows the number of jumps, and the y-axis shows the frequency.",
            font=("Arial", 11),
            bg="white",
            wraplength=500
        )
        explanation.grid(row=2, column=0, pady=5)

    def create_scatter_plot(self, frame):
        """Create and display scatter plot in frame"""
        scatter_fig = self.__stat.scatter_plot(figure_size=(8, 6))
        self.__active_figures.append(scatter_fig)

        scatter_canvas = FigureCanvasTkAgg(scatter_fig, master=frame)
        scatter_canvas.draw()
        scatter_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        title = tk.Label(
            frame,
            text="Relationship between Jumps and Time Played",
            font=("Arial", 14, "bold"),
            bg="white"
        )
        title.grid(row=1, column=0, pady=5)

        explanation = tk.Label(
            frame,
            text="This scatter plot shows the relationship between the number of jumps and time played. " +
                 "Each point represents a game, colored by theme.",
            font=("Arial", 11),
            bg="white",
            wraplength=500
        )
        explanation.grid(row=2, column=0, pady=5)
