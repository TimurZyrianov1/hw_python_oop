from typing import List, Union


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str, duration: float, distance: float,
                 speed: float, calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: Union[int, float],
                 duration: Union[int, float],
                 weight: Union[int, float]):
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        raise NotImplementedError(
            "Subclasses must implement the get_spent_calories method."
        )

    def show_training_info(self) -> InfoMessage:
        calories = self.get_spent_calories()
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            calories
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_CORRECTION: float = 1.79

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()
        return (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER * mean_speed
             + self.CALORIES_MEAN_CORRECTION) * self.weight
            / self.M_IN_KM * (self.duration * self.MIN_IN_HOUR)
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_MEAN_CORRECTION: float = 0.035
    CALORIES_MEAN_COEFF: float = 0.029
    METERS_IN_SM: int = 100
    C_MH_IN_HOUR: float = 0.278

    def __init__(
        self,
        action: Union[int, float],
        duration: Union[int, float],
        weight: Union[int, float],
        height: Union[int, float]
    ):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):

        mean_speed = self.get_mean_speed() * self.C_MH_IN_HOUR
        return ((self.CALORIES_MEAN_CORRECTION
                * self.weight + (mean_speed ** 2
                 / (self.height / self.METERS_IN_SM))
                * self.CALORIES_MEAN_COEFF * self.weight)
                * self.duration * self.MIN_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""

    SWIMMING_COUNT_MULTIPLIER: float = 1.1
    CALORIES_MEAN_CORRECTION_THREE: int = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: Union[int, float],
                 duration: Union[int, float],
                 weight: Union[int, float],
                 length_pool: Union[int, float],
                 count_pool: Union[int, float]
                 ):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()
        return (
            (mean_speed + self.SWIMMING_COUNT_MULTIPLIER)
            * self.CALORIES_MEAN_CORRECTION_THREE * self.weight * self.duration
        )


def read_package(workout_type: str, data: List[int]) -> Training:
    training_classes = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}

    if workout_type not in training_classes:
        raise ValueError(f'UnXknown workout type: {workout_type}')
    return training_classes[workout_type](*data)


def main(training: Training) -> None:
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
