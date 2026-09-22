import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window

GRID_SIZE = 20

class SnakeGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 0
        self.rows = 0
        self.snake = []
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.food = (0, 0)
        self.score = 0
        self.game_over = False
        self.score_label = Label(text="Score: 0", pos=(10, Window.height - 40),
                                  size_hint=(None, None), font_size=24)
        self.add_widget(self.score_label)
        Window.bind(size=self._on_resize)
        Clock.schedule_once(lambda dt: self.start_game(), 0)

    def _on_resize(self, *args):
        self.start_game()

    def start_game(self):
        self.cols = max(5, Window.width // GRID_SIZE)
        self.rows = max(5, (Window.height - 60) // GRID_SIZE)
        cx, cy = self.cols // 2, self.rows // 2
        self.snake = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.score = 0
        self.game_over = False
        self.score_label.text = "Score: 0"
        self.spawn_food()
        Clock.unschedule(self.update)
        Clock.schedule_interval(self.update, 0.15)

    def spawn_food(self):
        while True:
            fx = random.randint(0, self.cols - 1)
            fy = random.randint(0, self.rows - 1)
            if (fx, fy) not in self.snake:
                self.food = (fx, fy)
                break

    def on_touch_down(self, touch):
        if self.game_over:
            self.start_game()
            return
        cx, cy = Window.width / 2, Window.height / 2
        dx, dy = touch.x - cx, touch.y - cy
        if abs(dx) > abs(dy):
            self.next_direction = (1, 0) if dx > 0 else (-1, 0)
        else:
            self.next_direction = (0, 1) if dy > 0 else (0, -1)

    def update(self, dt):
        if self.game_over:
            return
        if (self.next_direction[0] != -self.direction[0] or
                self.next_direction[1] != -self.direction[1]):
            self.direction = self.next_direction

        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        if (new_head[0] < 0 or new_head[0] >= self.cols or
                new_head[1] < 0 or new_head[1] >= self.rows or
                new_head in self.snake):
            self.game_over = True
            self.score_label.text = f"Game Over! Score: {self.score} (tap to restart)"
            return

        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            self.score_label.text = f"Score: {self.score}"
            self.spawn_food()
        else:
            self.snake.pop()

        self.draw()

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            Color(0.1, 0.1, 0.1, 1)
            Rectangle(pos=(0, 0), size=Window.size)
            Color(0.2, 0.8, 0.2, 1)
            for x, y in self.snake:
                Rectangle(pos=(x * GRID_SIZE, y * GRID_SIZE + 60),
                          size=(GRID_SIZE - 2, GRID_SIZE - 2))
            Color(0.9, 0.2, 0.2, 1)
            fx, fy = self.food
            Rectangle(pos=(fx * GRID_SIZE, fy * GRID_SIZE + 60),
                      size=(GRID_SIZE - 2, GRID_SIZE - 2))


class SnakeApp(App):
    def build(self):
        return SnakeGame()


if __name__ == "__main__":
    SnakeApp().run()
