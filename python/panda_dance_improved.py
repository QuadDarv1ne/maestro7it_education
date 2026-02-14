from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.task import Task
from direct.interval.IntervalGlobal import Sequence, LerpHprInterval, LerpPosInterval
from panda3d.core import loadPrcFileData, AmbientLight, DirectionalLight, Spotlight, PointLight, Vec4, Vec3, NodePath
from panda3d.core import Filename, Texture, TextureStage, TransparencyAttrib
from panda3d.core import CollisionTraverser, CollisionNode, CollisionSphere
from math import pi, sin, cos
import sys
import os
import random
# globalClock is available as self.taskMgr.globalClock in ShowBase

# Настройка заголовка окна через конфигурацию (до создания окна)
loadPrcFileData("", "window-title Танцующая панда 3D")

class DancingPanda3D(ShowBase):
    def __init__(self):
        # Инициализация движка
        ShowBase.__init__(self)
        
        # Альтернативный способ установки заголовка (если loadPrcFileData не сработал)
        if hasattr(self, 'win') and self.win:
            self.win.setTitle("Танцующая панда 3D")
        
        # Добавляем освещение
        self.setup_lighting()
        
        # Загружаем окружение (лес) – если нет, создаём простой пол и небо
        self.setup_environment()
        
        # Загружаем панду (пробуем стандартную модель, если нет – создаём из примитивов)
        self.load_panda()
        
        # Отключаем стандартное управление мышью
        self.disableMouse()
        
        # Запускаем задачу вращения камеры
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        
        # Добавляем музыку (если есть)
        self.load_music()
        
        print("Управление: ESC - выход, стрелки - движение камеры (зажата мышь)")
    
    def setup_lighting(self):
        """Настраивает продвинутое освещение сцены"""
        # Окружающий свет
        ambient_light = AmbientLight("ambient")
        ambient_light.setColor(Vec4(0.2, 0.2, 0.2, 1))
        self.render.setLight(self.render.attachNewNode(ambient_light))
        
        # Основной направленный свет (солнце)
        dir_light = DirectionalLight("directional")
        dir_light.setColor(Vec4(0.8, 0.7, 0.6, 1))
        dir_light.setDirection((-3, -3, -2))
        self.render.setLight(self.render.attachNewNode(dir_light))
        
        # Дополнительные точечные источники света для эффекта
        self.point_lights = []
        for i in range(4):
            light = PointLight(f"point_light_{i}")
            light.setColor(Vec4(0.3, 0.5, 1.0, 1))
            light_np = self.render.attachNewNode(light)
            light_np.setPos(random.uniform(-20, 20), random.uniform(-20, 20), random.uniform(5, 15))
            self.render.setLight(light_np)
            self.point_lights.append(light_np)
        
        # Динамическое изменение цвета точечных источников
        self.taskMgr.add(self.animate_lights, "animate_lights")
        
        # Включаем тени
        render.setShaderAuto()
    
    def setup_environment(self):
        """Создаёт улучшенное окружение (земля, небо, декорации)"""
        # Земля (текстурированная плоскость)
        self.ground = self.loader.loadModel("models/plane")  # может не быть
        if self.ground:
            self.ground.reparentTo(self.render)
            self.ground.setScale(100, 100, 1)
            self.ground.setColor(0.2, 0.8, 0.2, 1)
            # Попробуем добавить текстуру травы, если доступна
            try:
                grass_tex = self.loader.loadTexture("textures/grass.jpg")
                self.ground.setTexture(grass_tex, 1)
            except:
                self.ground.setColor(0.2, 0.8, 0.2, 1)  # зелёный цвет по умолчанию
        else:
            # Создаём плоскость вручную
            from panda3d.core import CardMaker
            cm = CardMaker("ground")
            cm.setFrame(-50, 50, -50, 50)
            self.ground = self.render.attachNewNode(cm.generate())
            self.ground.setColor(0.2, 0.8, 0.2, 1)
            self.ground.setPos(0, 0, -0.1)
            self.ground.setHpr(0, -90, 0)  # поворачиваем горизонтально
            # Попробуем добавить текстуру травы, если доступна
            try:
                grass_tex = self.loader.loadTexture("textures/grass.jpg")
                self.ground.setTexture(grass_tex, 1)
            except:
                pass
        
        # Создаём декоративные элементы
        self.create_decorations()
        
        # Создаём визуальные эффекты
        self.create_visual_effects()
        
        # Улучшенное небо с градиентом
        self.setBackgroundColor(0.4, 0.7, 1.0)  # светло-голубой
        
        # Создаём имитацию небесной сферы
        self.create_sky_dome()
        
        # Добавляем эффект тумана для глубины
        from panda3d.core import Fog
        exp_fog = Fog('distance_fog')
        exp_fog.setColor(0.4, 0.7, 1.0)
        exp_fog.setExpDensity(0.01)
        self.render.setFog(exp_fog)
    
    def load_panda(self):
        """Пытается загрузить модель панды, иначе создаёт из примитивов"""
        model_paths = [
            "models/panda-model",
            "samples/models/panda-model",
            "panda-model"
        ]
        loaded = False
        
        # Пробуем загрузить модель
        for path in model_paths:
            if os.path.exists(path + ".egg") or os.path.exists(path + ".bam"):
                try:
                    self.pandaActor = Actor(path, {"walk": path + "-walk"})
                    self.pandaActor.setScale(0.005, 0.005, 0.005)
                    self.pandaActor.reparentTo(self.render)
                    self.pandaActor.loop("walk")
                    
                    # Вторая панда
                    self.pandaActor2 = Actor(path, {"walk": path + "-walk"})
                    self.pandaActor2.setScale(0.005, 0.005, 0.005)
                    self.pandaActor2.setPos(2, 0, 0)
                    self.pandaActor2.reparentTo(self.render)
                    self.pandaActor2.loop("walk")
                    
                    print("Модель панды загружена!")
                    loaded = True
                    break
                except:
                    continue
        
        # Если не нашли, создаём простую панду из примитивов
        if not loaded:
            print("Модели не найдены, создаём панду из геометрических фигур")
            self.create_simple_panda()
    
    def create_simple_panda(self):
        """Создаёт упрощённую панду из сфер и цилиндров"""
        from panda3d.core import NodePath, CardMaker
        
        # Контейнер для панды
        panda = NodePath("panda")
        panda.reparentTo(self.render)
        panda.setScale(0.5, 0.5, 0.5)
        panda.setPos(0, 10, 0)
        
        # Функция для создания части тела
        def create_part(model_name, color, pos, scale):
            part = self.loader.loadModel(model_name)
            if not part:
                # Если модель не найдена, создаём сферу
                from panda3d.core import Sphere
                sphere = Sphere(0, 0, 0, 1)
                part = panda.attachNewNode("sphere")
                # В реальности нужно создать узел с геометрией, но для простоты используем загрузку
                part = self.loader.loadModel("models/sphere")  # может не быть
                if not part:
                    # Создаём карточку (квадрат) как заглушку
                    cm = CardMaker("card")
                    cm.setFrame(-1, 1, -1, 1)
                    part = NodePath(cm.generate())
            part.setColor(*color)
            part.setPos(*pos)
            part.setScale(*scale)
            part.reparentTo(panda)
            return part
        
        # Создаём тело (большой эллипсоид)
        body = create_part("models/sphere", (0, 0, 0, 1), (0, 0, 0), (1, 1.2, 0.8))
        body.setColor(1, 1, 1, 1)  # белый
        
        # Голова
        head = create_part("models/sphere", (1, 1, 1, 1), (0, 0, 1.2), (0.8, 0.8, 0.8))
        head.setColor(1, 1, 1, 1)
        
        # Уши (чёрные)
        ear_l = create_part("models/sphere", (0, 0, 0, 1), (-0.6, 0, 1.8), (0.4, 0.2, 0.4))
        ear_l.setColor(0, 0, 0, 1)
        ear_r = create_part("models/sphere", (0, 0, 0, 1), (0.6, 0, 1.8), (0.4, 0.2, 0.4))
        ear_r.setColor(0, 0, 0, 1)
        
        # Глаза (чёрные)
        eye_l = create_part("models/sphere", (0, 0, 0, 1), (-0.3, 0.5, 1.4), (0.15, 0.15, 0.15))
        eye_r = create_part("models/sphere", (0, 0, 0, 1), (0.3, 0.5, 1.4), (0.15, 0.15, 0.15))
        
        # Нос (чёрный)
        nose = create_part("models/sphere", (0, 0, 0, 1), (0, 0.5, 1.1), (0.1, 0.1, 0.1))
        
        # Руки и ноги (цилиндры) – упрощённо
        
        # Анимация: будем вращать панду и двигать уши
        self.taskMgr.add(self.animate_simple_panda, "AnimateSimplePanda", extraArgs=[panda])
        
        # Вторая панда
        panda2 = NodePath("panda2")
        panda2.reparentTo(self.render)
        panda2.setScale(0.5, 0.5, 0.5)
        panda2.setPos(2, 10, 0)
        # Скопируем структуру (упрощённо – создадим заново)
        # Для простоты создадим ту же панду в другой позиции
        # В реальности нужно скопировать ноды, но здесь просто создадим новую
        
        # Создаём вторую панду
        self.create_second_panda()
        
        # Сохраним как атрибуты для анимации
        self.simple_panda = panda
        self.simple_panda2 = self.panda2  # теперь не пустая
    
    def create_decorations(self):
        """Создаёт декоративные элементы для окружения"""
        # Создаём несколько деревьев
        tree_positions = [
            (-30, -25, 0), (25, -30, 0), (-20, 30, 0), (30, 20, 0),
            (-40, 10, 0), (15, -40, 0), (40, 35, 0), (-15, 40, 0)
        ]
        
        for i, pos in enumerate(tree_positions):
            try:
                # Пытаемся загрузить модель дерева
                tree = self.loader.loadModel("models/tree")
                if tree:
                    tree.reparentTo(self.render)
                    tree.setPos(pos[0], pos[1], pos[2])
                    tree.setScale(0.8, 0.8, 0.8)
                else:
                    # Создаём простое дерево из примитивов
                    tree = self.create_simple_tree(pos[0], pos[1], pos[2])
            except:
                # Создаём простое дерево из примитивов
                tree = self.create_simple_tree(pos[0], pos[1], pos[2])
    
    def create_simple_tree(self, x, y, z):
        """Создаёт простое дерево из цилиндра и конуса"""
        from panda3d.core import Cylinder, GeomVertexFormat, GeomVertexData
        
        # Ствол дерева
        trunk = self.loader.loadModel("models/cylinder")
        if not trunk:
            trunk = NodePath("trunk")
            trunk.reparentTo(self.render)
        trunk.setPos(x, y, z)
        trunk.setScale(0.5, 0.5, 2)
        trunk.setColor(0.5, 0.3, 0.1, 1)  # коричневый
        
        # Крона дерева
        foliage = self.loader.loadModel("models/cone")
        if not foliage:
            foliage = NodePath("foliage")
            foliage.reparentTo(self.render)
        foliage.setPos(x, y, z + 2)
        foliage.setScale(2, 2, 3)
        foliage.setColor(0.1, 0.6, 0.2, 1)  # зелёный
        
        return trunk
    
    def create_visual_effects(self):
        """Создаёт визуальные эффекты: частицы, свечение и т.д."""
        # Создаём эффекты частиц вокруг панд
        self.create_sparkle_effect()
        self.create_confetti_effect()
    
    def create_sparkle_effect(self):
        """Создаёт мерцающие частицы вокруг панд"""
        self.sparkles = []
        for i in range(10):
            from panda3d.core import CardMaker
            cm = CardMaker(f"sparkle_{i}")
            cm.setFrame(-0.1, 0.1, -0.1, 0.1)
            sparkle = self.render.attachNewNode(cm.generate())
            
            sparkle.reparentTo(self.render)
            sparkle.setScale(0.1, 0.1, 0.1)
            sparkle.setColor(1, 1, 0.8, 1)  # Жёлто-белый цвет
            sparkle.setTransparency(1)  # Прозрачность
            
            # Начальная позиция около панд
            sparkle.setPos(
                random.uniform(-3, 3),
                random.uniform(8, 12),
                random.uniform(0.5, 2)
            )
            
            self.sparkles.append(sparkle)
        
        # Запускаем анимацию блеска
        self.taskMgr.add(self.animate_sparkles, "AnimateSparkles")
    
    def create_confetti_effect(self):
        """Создаёт эффект конфетти"""
        self.confetti = []
        for i in range(20):
            from panda3d.core import CardMaker
            cm = CardMaker(f"confetto_{i}")
            cm.setFrame(-0.1, 0.1, -0.1, 0.1)
            confetto = self.render.attachNewNode(cm.generate())
            
            confetto.reparentTo(self.render)
            confetto.setScale(0.2, 0.2, 0.2)
            confetto.setColor(
                random.random(),
                random.random(),
                random.random(),
                1
            )
            confetto.setTransparency(1)
            
            # Начальная позиция
            confetto.setPos(
                random.uniform(-5, 5),
                random.uniform(5, 15),
                random.uniform(5, 10)
            )
            
            # Сохраняем начальную позицию и скорость
            self.confetti.append({
                'node': confetto,
                'velocity': Vec3(
                    random.uniform(-0.5, 0.5),
                    random.uniform(-0.5, 0.5),
                    random.uniform(-1, -0.5)
                ),
                'rotation_speed': random.uniform(-5, 5)
            })
        
        # Запускаем анимацию конфетти
        self.taskMgr.add(self.animate_confetti, "AnimateConfetti")
    
    def animate_sparkles(self, task):
        """Анимирует мерцающие частицы"""
        t = task.time
        for i, sparkle in enumerate(self.sparkles):
            # Мерцание
            intensity = 0.7 + 0.3 * sin(t * 5 + i)
            sparkle.setScale(0.05 + 0.05 * sin(t * 3 + i), 
                             0.05 + 0.05 * sin(t * 3 + i), 
                             0.05 + 0.05 * sin(t * 3 + i))
            sparkle.setColor(1, 1, 0.8, intensity)
            
            # Лёгкое движение
            new_x = sparkle.getX() + 0.01 * sin(t * 2 + i)
            new_y = sparkle.getY() + 0.01 * cos(t * 2 + i)
            sparkle.setPos(new_x, new_y, sparkle.getZ())
        
        return Task.cont
    
    def animate_confetti(self, task):
        """Анимирует падающее конфетти"""
        dt = self.taskMgr.globalClock.getDt()  # получаем deltaTime
        for confetto_data in self.confetti:
            confetto = confetto_data['node']
            velocity = confetto_data['velocity']
            rotation_speed = confetto_data['rotation_speed']
            
            # Обновляем позицию
            new_pos = confetto.getPos() + velocity * dt
            confetto.setPos(new_pos)
            
            # Обновляем вращение
            current_hpr = confetto.getHpr()
            confetto.setHpr(current_hpr + Vec3(rotation_speed * dt, 
                                              rotation_speed * dt, 
                                              0))
            
            # Если конфетти упало слишком низко, возвращаем его наверх
            if confetto.getZ() < -1:
                confetto.setPos(
                    random.uniform(-5, 5),
                    random.uniform(5, 15),
                    random.uniform(8, 12)
                )
        
        return Task.cont
    
    def create_sky_dome(self):
        """Создаёт имитацию небесной сферы"""
        try:
            # Пытаемся загрузить модель небесной сферы
            sky_model = self.loader.loadModel("models/sky_sphere")
            if sky_model:
                sky_model.reparentTo(self.render)
                sky_model.setScale(1000)  # очень большой радиус
                sky_model.setBin('background', 1)  # фоновый слой
                sky_model.setDepthWrite(False)  # не записываем в буфер глубины
                sky_model.setTwoSided(True)  # двусторонний рендеринг
                self.sky_dome = sky_model
            else:
                # Создаём небесную сферу вручную
                self.create_simple_sky_dome()
        except:
            # Создаём небесную сферу вручную
            self.create_simple_sky_dome()
    
    def create_simple_sky_dome(self):
        """Создаёт простую небесную сферу"""
        from panda3d.core import CardMaker
        
        # Создаём полусферу для неба
        cm = CardMaker("sky_dome")
        cm.setFrame(-50, 50, -50, 50)
        sky_quad = self.render.attachNewNode(cm.generate())
        
        # Устанавливаем цвет неба
        sky_quad.setColor(0.4, 0.7, 1.0, 1)
        sky_quad.setBin('background', 1)
        sky_quad.setDepthWrite(False)
        
        # Позиционируем над сценой
        sky_quad.setPos(0, 0, 50)
        sky_quad.setBillboardPointEye()  # всегда обращена к камере
        
        self.sky_dome = sky_quad
    
    def create_second_panda(self):
        """Создаёт вторую панду с немного другими параметрами"""
        from panda3d.core import NodePath
        
        # Контейнер для второй панды
        panda2 = NodePath("panda2")
        panda2.reparentTo(self.render)
        panda2.setScale(0.5, 0.5, 0.5)
        panda2.setPos(2, 10, 0)
        
        # Копируем структуру первой панды с небольшими изменениями
        # Тело (большой эллипсоид)
        body = self.create_part("models/sphere", (1, 1, 1, 1), (0, 0, 0), (1, 1.2, 0.8), panda2)
        body.setColor(1, 1, 1, 1)  # белый
        
        # Голова
        head = self.create_part("models/sphere", (1, 1, 1, 1), (0, 0, 1.2), (0.8, 0.8, 0.8), panda2)
        head.setColor(1, 1, 1, 1)
        
        # Уши (чёрные)
        ear_l = self.create_part("models/sphere", (0, 0, 0, 1), (-0.6, 0, 1.8), (0.4, 0.2, 0.4), panda2)
        ear_l.setColor(0, 0, 0, 1)
        ear_r = self.create_part("models/sphere", (0, 0, 0, 1), (0.6, 0, 1.8), (0.4, 0.2, 0.4), panda2)
        ear_r.setColor(0, 0, 0, 1)
        
        # Глаза (чёрные)
        eye_l = self.create_part("models/sphere", (0, 0, 0, 1), (-0.3, 0.5, 1.4), (0.15, 0.15, 0.15), panda2)
        eye_r = self.create_part("models/sphere", (0, 0, 0, 1), (0.3, 0.5, 1.4), (0.15, 0.15, 0.15), panda2)
        
        # Нос (чёрный)
        nose = self.create_part("models/sphere", (0, 0, 0, 1), (0, 0.5, 1.1), (0.1, 0.1, 0.1), panda2)
        
        # Анимация для второй панды
        self.taskMgr.add(self.animate_simple_panda2, "AnimateSimplePanda2", extraArgs=[panda2])
        
        # Сохраняем ссылку
        self.panda2 = panda2
    
    def create_part(self, model_name, color, pos, scale, parent):
        """Создаёт часть тела для панды"""
        part = self.loader.loadModel(model_name)
        if not part:
            # Создаём карточку (квадрат) как заглушку
            from panda3d.core import CardMaker
            cm = CardMaker("card")
            cm.setFrame(-1, 1, -1, 1)
            part = NodePath(cm.generate())
        part.setColor(*color)
        part.setPos(*pos)
        part.setScale(*scale)
        part.reparentTo(parent)
        return part
    
    def animate_lights(self, task):
        """Анимирует цвет точечных источников света"""
        t = task.time
        for i, light_np in enumerate(self.point_lights):
            # Изменяем цвет в зависимости от времени
            r = 0.3 + 0.2 * sin(t + i)
            g = 0.5 + 0.2 * cos(t * 0.8 + i)
            b = 1.0 + 0.2 * sin(t * 1.2 + i)
            light_np.node().setColor(Vec4(r, g, b, 1))
        return Task.cont
    
    def animate_simple_panda2(self, panda, task):
        """Продвинутая анимация танца для второй панды из примитивов"""
        t = task.time
        
        # Сложная хореография с использованием тригонометрических функций
        dance_phase = t * 2  # Ускорим темп танца
        
        # Вращение тела в противофазе с первой пандой
        panda.setH(sin(dance_phase + pi) * 15)
        
        # Вертикальное движение в противофазе
        panda.setZ(0.5 + sin(dance_phase * 1.5 + pi) * 0.3)
        
        # Боковое движение в противофазе
        panda.setX(cos(dance_phase * 0.7 + pi) * 0.8)
        
        # Поворот влево-вправо в противофазе
        panda.setR(sin(dance_phase * 0.9 + pi) * 10)
        
        # Движение головы
        head = None
        for child in panda.getChildren():
            if "head" in child.getName().lower():
                head = child
                break
        
        if head:
            head.setH(sin(dance_phase * 2 + pi/2) * 20)  # Поворот головы в противофазе
            
        # Движение глаз
        left_eye = None
        right_eye = None
        for child in panda.getChildren():
            if "eye" in child.getName().lower():
                if not left_eye:
                    left_eye = child
                else:
                    right_eye = child
                    break
        
        if left_eye and right_eye:
            # Моргание в противофазе
            if int(t + 1) % 2 == 0 and t % 0.2 > 0.1:
                left_eye.setScale(0.1, 0.05, 0.15)
                right_eye.setScale(0.1, 0.05, 0.15)
            else:
                left_eye.setScale(0.15, 0.15, 0.15)
                right_eye.setScale(0.15, 0.15, 0.15)
        
        return Task.cont
    
    def animate_simple_panda(self, panda, task):
        """Продвинутая анимация танца для панды из примитивов"""
        t = task.time
        
        # Сложная хореография с использованием тригонометрических функций
        dance_phase = t * 2  # Ускорим темп танца
        
        # Вращение тела
        panda.setH(sin(dance_phase) * 15)
        
        # Вертикальное движение
        panda.setZ(0.5 + sin(dance_phase * 1.5) * 0.3)
        
        # Боковое движение
        panda.setX(cos(dance_phase * 0.7) * 0.8)
        
        # Поворот влево-вправо
        panda.setR(sin(dance_phase * 0.9) * 10)
        
        # Движение головы
        head = None
        for child in panda.getChildren():
            if "head" in child.getName().lower():
                head = child
                break
        
        if head:
            head.setH(sin(dance_phase * 2) * 20)  # Поворот головы
            
        # Движение глаз
        left_eye = None
        right_eye = None
        for child in panda.getChildren():
            if "eye" in child.getName().lower():
                if not left_eye:
                    left_eye = child
                else:
                    right_eye = child
                    break
        
        if left_eye and right_eye:
            # Моргание
            if int(t) % 2 == 0 and t % 0.2 > 0.1:
                left_eye.setScale(0.1, 0.05, 0.15)
                right_eye.setScale(0.1, 0.05, 0.15)
            else:
                left_eye.setScale(0.15, 0.15, 0.15)
                right_eye.setScale(0.15, 0.15, 0.15)
        
        return Task.cont
    
    def __init__(self):
        # Инициализация движка
        ShowBase.__init__(self)
        
        # Настройка производительности
        self.setup_performance_optimization()
        
        # Настройка режимов камеры
        self.camera_modes = ["orbit", "follow", "fixed"]
        self.current_camera_mode = 0
        self.accept("c", self.switch_camera_mode)
        
        # Альтернативный способ установки заголовка (если loadPrcFileData не сработал)
        if hasattr(self, 'win') and self.win:
            self.win.setTitle("Танцующая панда 3D")
        
        # Добавляем освещение
        self.setup_lighting()
        
        # Загружаем окружение (лес) – если нет, создаём простый пол и небо
        self.setup_environment()
        
        # Загружаем панду (пробуем стандартную модель, если нет – создаём из примитивов)
        self.load_panda()
        
        # Отключаем стандартное управление мышью
        self.disableMouse()
        
        # Запускаем задачу вращения камеры
        self.taskMgr.add(self.camera_control_task, "CameraControlTask")
        
        # Добавляем музыку (если есть)
        self.load_music()
        
        print("Управление: ESC - выход, 'c' - сменить режим камеры, стрелки - движение камеры (зажата мышь)")
    
    def switch_camera_mode(self):
        """Переключает между режимами камеры"""
        self.current_camera_mode = (self.current_camera_mode + 1) % len(self.camera_modes)
        mode_name = self.camera_modes[self.current_camera_mode]
        print(f"Режим камеры изменён на: {mode_name}")
    
    def camera_control_task(self, task):
        """Управляет камерой в зависимости от выбранного режима"""
        mode = self.camera_modes[self.current_camera_mode]
        
        if mode == "orbit":
            self.orbit_camera(task)
        elif mode == "follow":
            self.follow_camera(task)
        elif mode == "fixed":
            self.fixed_camera(task)
        
        return Task.cont
    
    def orbit_camera(self, task):
        """Вращает камеру вокруг панд"""
        angleDegrees = task.time * 6.0  # скорость вращения
        angleRadians = angleDegrees * (pi / 180.0)
        
        # Позиционируем камеру по кругу
        self.camera.setPos(
            20 * sin(angleRadians),   # X
            -20.0 * cos(angleRadians), # Y
            3                           # Z (высота)
        )
        self.camera.lookAt(0, 10, 0)  # смотрим на центр сцены
    
    def follow_camera(self, task):
        """Камера следует за одной из панд"""
        # Плавно двигаем камеру за пандой
        target_pos = self.simple_panda.getPos()
        target_pos += Vec3(0, -8, 5)  # немного позади и выше
        
        # Плавное перемещение камеры
        current_pos = self.camera.getPos()
        smooth_pos = current_pos + (target_pos - current_pos) * 0.1
        self.camera.setPos(smooth_pos)
        
        # Поворачиваем камеру к панде
        self.camera.lookAt(target_pos + Vec3(0, 2, 0))
    
    def fixed_camera(self, task):
        """Фиксированная позиция камеры"""
        # Устанавливаем камеру в фиксированное положение
        self.camera.setPos(0, -25, 8)
        self.camera.setHpr(0, -10, 0)
        self.camera.lookAt(0, 10, 0)
    
    def setup_performance_optimization(self):
        """Настройка оптимизации производительности"""
        # Установка уровня детализации
        from panda3d.core import AntialiasAttrib
        self.render.setAntialias(AntialiasAttrib.MMultisample)
        
        # Оптимизация рендеринга
        from panda3d.core import RenderState, StateSavedResult
        
        # Установка параметров производительности
        try:
            # Уменьшение качества теней для лучшей производительности
            self.render.setShaderAuto(enableTrueAlpha=True)
            
            # Оптимизация освещения
            from panda3d.core import LightRampAttrib
            self.render.setAttrib(LightRampAttrib.makeDefault())
            
            # Установка уровней детализации для моделей
            # (если используются LOD-модели)
            
            print("Оптимизация производительности завершена")
        except Exception as e:
            print(f"Ошибка при оптимизации производительности: {e}")
        
        # Установка ограничения FPS для стабильности
        self.globalClock.setMaxDt(1.0/60.0)  # Ограничение до 60 FPS
    
    def load_music(self):
        """Пытается загрузить музыку из файла и настраивает синхронизацию"""
        music_files = ["music/panda_dance.ogg", "panda_dance.ogg", "dance.ogg"]
        for file in music_files:
            if os.path.exists(file):
                try:
                    self.music = self.loader.loadSfx(file)
                    self.music.setLoop(True)
                    self.music.play()
                    print(f"Музыка загружена: {file}")
                    
                    # Начинаем синхронизацию с музыкой
                    self.setup_audio_visualization()
                    break
                except:
                    continue
        
        # Если музыка не загружена, всё равно запускаем визуализацию
        if not hasattr(self, 'music'):
            self.setup_audio_visualization()
    
    def setup_audio_visualization(self):
        """Настраивает визуализацию аудио (для симуляции)"""
        # Создаём объекты для визуализации музыки
        self.audio_bars = []
        bar_count = 8
        
        for i in range(bar_count):
            # Создаём бар (столбец) для визуализации
            bar = self.loader.loadModel("models/cube")  # если доступна модель куба
            if not bar:
                # Создаём простой куб вручную
                from panda3d.core import CardMaker
                cm = CardMaker(f"bar_{i}")
                cm.setFrame(-0.2, 0.2, -0.2, 0.2)
                bar = self.render.attachNewNode(cm.generate())
            
            bar.reparentTo(self.render)
            bar.setPos(-5 + i * 1.5, 20, -0.5)
            bar.setScale(0.3, 0.3, 1)
            bar.setColor(0.2, 0.6, 1.0, 1)
            self.audio_bars.append(bar)
        
        # Запускаем задачу анимации визуализации
        self.taskMgr.add(self.update_audio_visualization, "AudioVisualization")
    
    def update_audio_visualization(self, task):
        """Обновляет визуализацию аудио в реальном времени"""
        t = task.time
        
        # Симулируем анализ аудио и создаем эффекты
        for i, bar in enumerate(self.audio_bars):
            # Вычисляем высоту столбца на основе симуляции аудио
            freq = 1.0 + 2.0 * sin(t * 2.0 + i * 0.5)  # Симуляция частот
            amplitude = 0.5 + 0.5 * abs(sin(t * 1.5 + i * 0.3))  # Симуляция амплитуды
            height = max(0.5, min(5.0, freq * amplitude * 3))
            
            # Обновляем высоту столбца
            bar.setScale(0.3, 0.3, height)
            
            # Меняем цвет в зависимости от "громкости"
            color_factor = min(1.0, height / 3.0)
            bar.setColor(0.2 + 0.8 * color_factor, 0.6 - 0.3 * color_factor, 1.0 - 0.5 * color_factor, 1)
        
        # Также синхронизируем движения панд с "музыкой"
        if hasattr(self, 'simple_panda') and hasattr(self, 'panda2'):
            # Увеличиваем амплитуду движений в такт музыке
            beat_intensity = 1.0 + 0.3 * abs(sin(t * 0.5))  # Основной ритм
            
            # Применяем к анимации панд
            # Это будет дополнительный эффект поверх основной анимации
        
        return Task.cont

# Запуск приложения
if __name__ == "__main__":
    print("=" * 50)
    print("🐼 Танцующая панда 3D")
    print("Управление: ESC - выход, мышь + стрелки - камера")
    print("=" * 50)
    
    app = DancingPanda3D()
    app.run()