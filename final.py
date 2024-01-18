import pyxel
import random

class App:
    def __init__(self):
        pyxel.init(160, 120, fps=30)
        pyxel.mouse(True)
        self.reset_game()

        pyxel.run(self.update, self.draw)

    def reset_game(self):
        self.score = 0
        self.lives = 10
        self.timer = 63
        self.current_problem = None
        self.game_over = False
        self.generate_problem()

    def generate_problem(self):
        if self.score < 3:
            self.current_problem = {
                'operand1': random.randint(1, 9),
                'operand2': random.randint(1, 9),
                'operator': '+'
            }
        elif self.score < 6:
            self.current_problem = {
                'operand1': random.randint(10, 99),
                'operand2': random.randint(10, 99),
                'operator': '+'
            }
        elif self.score < 9:
            self.current_problem = {
                'operand1': random.randint(1, 9),
                'operand2': random.randint(1, 9),
                'operator': '*'
            }
        else:
            self.current_problem = {
                'operand1': random.randint(10, 99),
                'operand2': random.randint(10, 99),
                'operator': '*'
            }

        self.generate_choices()

    def generate_choices(self):
        correct_answer = self.evaluate_expression(
            self.current_problem['operand1'],
            self.current_problem['operand2'],
            self.current_problem['operator']
        )

        wrong_answers = [correct_answer]
        while len(wrong_answers) < 3:
            wrong_answer = correct_answer + random.randint(-10, 10)
            if wrong_answer not in wrong_answers and wrong_answer != correct_answer:
                wrong_answers.append(wrong_answer)

        random.shuffle(wrong_answers)
        self.choices = wrong_answers

    def evaluate_expression(self, operand1, operand2, operator):
        if operator == '+':
            return operand1 + operand2
        elif operator == '*':
            return operand1 * operand2
        else:
            raise ValueError("Invalid operator")

    def update(self):
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.reset_game()
                self.game_over = False
        else:
            if pyxel.btnp(pyxel.KEY_SPACE):
                selected_choice = self.check_selected_choice()
                if selected_choice == self.evaluate_expression(
                    self.current_problem['operand1'],
                    self.current_problem['operand2'],
                    self.current_problem['operator']
                ):
                    self.score += 1
                else:
                    self.lives -= 1

                if self.lives <= 0:
                    self.game_over = True
                else:
                    self.generate_problem()

                self.timer = 63

            self.timer -= 1
            if self.timer <= 0:
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
                else:
                    self.generate_problem()
                self.timer = 63

    def check_selected_choice(self):
        mouse_x, mouse_y = pyxel.mouse_x, pyxel.mouse_y

        for i, choice in enumerate(self.choices):
            if 40 + i * 40 <= mouse_x <= 80 + i * 40 and 80 <= mouse_y <= 100:
                return choice

        return None

    def draw(self):
        pyxel.cls(0)

        if not self.game_over:
            pyxel.text(10, 10, f"Score: {self.score}", 7)
            pyxel.text(70, 10, f"Lives: {self.lives}", 7)
            pyxel.rect(10, 30, 140, 40, 12)
            pyxel.text(20, 40, f"{self.current_problem['operand1']} {self.current_problem['operator']} {self.current_problem['operand2']} =", 7)

            for i, choice in enumerate(self.choices):
                pyxel.rect(40 + i * 40, 80, 30, 20, 8)
                pyxel.text(45 + i * 40, 85, str(choice), 7)

            pyxel.rect(10, 110, self.timer, 5, 11)
        else:
            pyxel.text(60, 50, "Game Over", 8)
            pyxel.text(50, 70, f"Final Score: {self.score}", 8)
            pyxel.text(40, 90, "Play Again : SPACE KEY", 8)

App()