class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        message = (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )
        return message


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65  # Расстояние, которое спортсмен преодолевает за один шаг
    M_IN_KM = 1000  # Константа для перевода метров в километры
    MIN_IN_HOUR = 60

    def __init__(self, action, duration, weight):
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self):
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self):
        return self.get_distance() / self.duration

    def get_spent_calories(self):
        pass

    def show_training_info(self):
        calories = self.get_spent_calories()
        message = InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            calories
        )
        return message


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self):
        mean_speed = self.get_mean_speed()
        calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                    * mean_speed + self.CALORIES_MEAN_SPEED_SHIFT)
                    * self.weight / self.M_IN_KM
                    * (self.duration * self.MIN_IN_HOUR))
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEF_1 = 0.035
    COEF_2 = 0.029
    METTERS_IN_SM = 100
    C_MH_IN_HOUR = 0.278

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        mean_speed = self.get_mean_speed() * self.C_MH_IN_HOUR
        calories = ((self.COEF_1 * self.weight + (mean_speed ** 2
                    / (self.height / self.METTERS_IN_SM))
                    * self.COEF_2 * self.weight)
                    * self.duration * self.MIN_IN_HOUR)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""

    ANOTHER_COEF_1 = 1.1
    ANOTHER_COEF_2 = 2
    LEN_STEP = 1.38

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        return (self.length_pool
                * self.count_pool / self.M_IN_KM / self.duration)

    def get_spent_calories(self):
        mean_speed = self.get_mean_speed()
        calories = ((mean_speed + self.ANOTHER_COEF_1)
                    * self.ANOTHER_COEF_2 * self.weight * self.duration)
        return calories


def read_package(workout_type, data):
    training_classes = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type in training_classes:
        return training_classes[workout_type](*data)
    else:
        raise ValueError(f'Unknown workout type: {workout_type}')


def main(training):
    info_message = training.show_training_info()
    print(info_message.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

