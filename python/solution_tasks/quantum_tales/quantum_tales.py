import re
import time
import sys
import random
import pickle
from colorama import Fore, init
from typing import Dict, List, Tuple, Optional, Any

init(autoreset=True)

class Scene:
    def __init__(self, name: str):
        self.name = name
        self.text: str = ""
        self.choices: List[Tuple[str, str, Optional[str]]] = []
        self.effects: List[str] = []
        self.art: str = ""
        self.on_enter: List[str] = []

class StoryParser:
    def __init__(self, source: str):
        self.source = source
        self.scenes: Dict[str, Scene] = {}

    def parse(self) -> Dict[str, Scene]:
        scene_blocks = re.split(r'\n(?=scene )', self.source)
        
        for block in scene_blocks:
            lines = [line.strip() for line in block.split('\n') if line.strip()]
            if not lines:
                continue
                
            header_match = re.match(r'scene (\w+):', lines[0])
            if not header_match:
                continue
                
            scene = Scene(header_match.group(1))
            current_section = None
            
            for line in lines[1:]:
                if line.startswith('text:'):
                    current_section = 'text'
                elif line.startswith('art:'):
                    current_section = 'art'
                elif line.startswith('effects:'):
                    current_section = 'effects'
                elif line.startswith('choices:'):
                    current_section = 'choices'
                elif line.startswith('on_enter:'):
                    current_section = 'on_enter'
                else:
                    self._process_line(line, scene, current_section)

            self.scenes[scene.name] = scene
        return self.scenes

    def _process_line(self, line: str, scene: Scene, section: str):
        if section == 'text':
            scene.text += line + '\n'
        elif section == 'art':
            scene.art += line + '\n'
        elif section == 'effects':
            scene.effects.append(line)
        elif section == 'on_enter':
            scene.on_enter.append(line)
        elif section == 'choices':
            choice_match = re.match(
                r'"(.+?)" -> (\w+)(?: if (.+))?(?: \[(.+)\])?', 
                line
            )
            if choice_match:
                text, target, condition, tags = choice_match.groups()
                scene.choices.append((text, target, condition, tags))

class StoryRunner:
    def __init__(self, scenes: Dict[str, Scene]):
        self.scenes = scenes
        self.state = {
            'stats': {'courage': 0, 'health': 100},
            'inventory': {},
            'flags': set(),
            'relationships': {}
        }
        self.current_scene = "start"
        self.choice_history = []
        self.achievements = set()
        self.visited_scenes = set()

    def run(self):
        try:
            while True:
                self._clear_screen()
                scene = self.scenes[self.current_scene]
                
                # Обработка при первом входе в сцену
                if self.current_scene not in self.visited_scenes:
                    self._process_effects(scene.on_enter)
                    self.visited_scenes.add(self.current_scene)
                
                self._process_effects(scene.effects)
                self._display_scene(scene)
                self._check_achievements()
                
                next_scene = self._handle_choices(scene)
                if not next_scene:
                    break
                    
                self.current_scene = next_scene
                self._handle_random_events()
        except KeyboardInterrupt:
            self.save_game('autosave.pkl')
            print("\nИгра сохранена!")

    def _display_scene(self, scene: Scene):
        if scene.art:
            print(Fore.CYAN + scene.art.strip())
            
        self._slow_print(Fore.YELLOW + scene.text.strip())
        print()

        # Показать статус
        print(Fore.LIGHTBLUE_EX + f"Здоровье: {self.state['stats']['health']}")
        print(Fore.LIGHTBLUE_EX + f"Смелость: {self.state['stats']['courage']}")

    def _process_effects(self, effects: List[str]):
        for effect in effects:
            try:
                if effect.startswith('set '):
                    key, op, value = re.match(r'set (\w+)([+-=])(\d+)', effect).groups()
                    if op == '+':
                        self.state['stats'][key] += int(value)
                    elif op == '-':
                        self.state['stats'][key] -= int(value)
                    else:
                        self.state['stats'][key] = int(value)
                elif effect.startswith('flag '):
                    self.state['flags'].add(effect[5:])
                elif effect.startswith('unflag '):
                    self.state['flags'].discard(effect[7:])
                elif effect.startswith('relationship '):
                    name, op, value = re.match(r'relationship (\w+)([+-])(\d+)', effect).groups()
                    current = self.state['relationships'].get(name, 0)
                    self.state['relationships'][name] = current + (int(value) * (1 if op == '+' else -1))
                elif effect.startswith('add_item '):
                    item = effect[9:]
                    self.state['inventory'][item] = self.state['inventory'].get(item, 0) + 1
                elif effect.startswith('remove_item '):
                    item = effect[12:]
                    if self.state['inventory'].get(item, 0) > 0:
                        self.state['inventory'][item] -= 1
            except Exception as e:
                print(f"Ошибка в эффекте '{effect}': {e}")

    def _handle_choices(self, scene: Scene) -> Optional[str]:
        valid_choices = []
        for idx, (text, target, condition, tags) in enumerate(scene.choices):
            if condition and not self._check_condition(condition):
                continue
            valid_choices.append((idx, text, target, tags))

        if not valid_choices:
            print(Fore.RED + "Нет доступных вариантов! Игра завершена.")
            return None

        for idx, choice in enumerate(valid_choices):
            tags = f" [{choice[3]}]" if choice[3] else ""
            print(Fore.GREEN + f"{idx+1}. {choice[1]}{tags}")

        while True:
            try:
                choice = int(input(Fore.MAGENTA + "> ")) - 1
                if 0 <= choice < len(valid_choices):
                    selected = valid_choices[choice]
                    self._record_choice(scene.name, selected[1], selected[2])
                    return selected[2]
                raise ValueError
            except (ValueError, IndexError):
                print(Fore.RED + f"Введите число от 1 до {len(valid_choices)}")

    def _record_choice(self, scene: str, choice: str, target: str):
        self.choice_history.append({
            'scene': scene,
            'choice': choice,
            'target': target,
            'timestamp': time.time()
        })

    def _check_condition(self, condition: str) -> bool:
        try:
            if condition.startswith('has_item('):
                item = condition[9:-1]
                return self.state['inventory'].get(item, 0) > 0
            elif condition.startswith('relationship('):
                name, comparison, value = re.match(r'relationship\((\w+)\)\s*([>=<]+)\s*(\d+)', condition).groups()
                return eval(f"{self.state['relationships'].get(name,0)} {comparison} {value}")
            elif condition.startswith('visited('):
                scene, comparison, num = re.match(r'visited\((\w+)\)\s*([>=<]+)\s*(\d+)', condition).groups()
                count = sum(1 for h in self.choice_history if h['target'] == scene)
                return eval(f"{count} {comparison} {num}")
            elif condition.startswith('flag('):
                return condition[5:-1] in self.state['flags']
            return eval(condition, None, self.state['stats'])
        except:
            return False

    def _check_achievements(self):
        achievements = {
            'hero': lambda: self.state['stats']['courage'] >= 50,
            'collector': lambda: sum(self.state['inventory'].values()) >= 10,
            'romantic': lambda: any(v >= 50 for v in self.state['relationships'].values()),
            'explorer': lambda: len(self.visited_scenes) >= 5
        }
        for name, check in achievements.items():
            if name not in self.achievements and check():
                self.achievements.add(name)
                self._slow_print(Fore.LIGHTMAGENTA_EX + f"Достижение получено: {name}!")

    def _handle_random_events(self):
        if random.random() < 0.15:
            events = [
                (Fore.BLUE + "Случайное событие: найдено зелье!", "add_item potion"),
                (Fore.RED + "Случайное событие: атакованы бандитами!", "set health -20"),
                (Fore.GREEN + "Случайное событие: помогли путнику!", "relationship traveler +10"),
            ]
            event, effect = random.choice(events)
            self._slow_print(event)
            self._process_effects([effect])
    
    def _show_status(self):
        print(f"\n{Fore.BLUE} СТАТУС {'':<60}")
        print(f"{Fore.CYAN}❤️ Здоровье: {self.state.stats['health']}")
        print(f"{Fore.YELLOW}⚔️ Смелость: {self.state.stats['courage']}")
        print(f"{Fore.GREEN}📚 Интеллект: {self.state.stats['intelligence']}")
        print(f"{Fore.MAGENTA}💰 Золото: {self.state.stats['gold']}")
        print("-" * 70)

    def save_game(self, filename: str):
        with open(filename, 'wb') as f:
            pickle.dump({
                'current_scene': self.current_scene,
                'state': self.state,
                'history': self.choice_history,
                'achievements': self.achievements,
                'visited': self.visited_scenes
            }, f)

    @classmethod
    def load_game(cls, scenes: Dict[str, Scene], filename: str) -> 'StoryRunner':
        with open(filename, 'rb') as f:
            data = pickle.load(f)
            runner = cls(scenes)
            runner.current_scene = data['current_scene']
            runner.state = data['state']
            runner.choice_history = data['history']
            runner.achievements = data['achievements']
            runner.visited_scenes = data['visited']
            return runner

    @staticmethod
    def _slow_print(text: str, delay: float = 0.03):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    @staticmethod
    def _clear_screen():
        print("\033[H\033[J")

# Пример истории
STORY = """
scene start:
    text:
        Вы стоите на площади средневекового города. 
        Куда отправитесь?
    art:
            .........／フ   フ    💕
            ........(  _  _ )   💕
            ......／` ミ_x_ノ мур
            ...../         |
            ..../   ヽ     ﾉ
            ...│    | |  |
            ..／￣| | |  |
            ..| (￣ヽ_ヽ_)__)
            ..＼二つ
    effects:
        set courage+5
    on_enter:
        add_item map
    choices:
        "В таверну" -> tavern if has_item(map)
        "На рынок" -> market [Торговля]
        "В замок" -> castle if courage>=10 [Секрет]

scene tavern:
    text:
        В таверне шумно. За стойкой стоит улыбающийся бармен.
    choices:
        "Заказать эль" -> ale_scene [−2 золота]
        "Спросить о новостях" -> rumors_scene if relationship(barman)>=20
        "Уйти" -> start

scene castle:
    text:
        Вы стоите перед величественными воротами замка.
    choices:
        "Попытаться войти" -> castle_inside if flag(noble)
        "Осмотреть стены" -> walls_scene if visited(start)>=3
        "Вернуться" -> start

scene market:
    text:
        На рынке кипит жизнь. Торговцы предлагают товары.
    effects:
        add_item gold +10
    choices:
        "Купить меч" -> buy_sword if has_item(gold>=5)
        "Поговорить с торговцем" -> merchant_talk [Дипломатия]
        "Уйти" -> start
"""

if __name__ == "__main__":
    parser = StoryParser(STORY)
    scenes = parser.parse()
    
    try:
        runner = StoryRunner.load_game(scenes, 'autosave.pkl')
        print("Загружено сохранение")
    except FileNotFoundError:
        runner = StoryRunner(scenes)
    
    runner.run()
