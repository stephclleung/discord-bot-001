
class Car:
    def __init__(self, speed=0):
        self.speed = speed
        self.odometer = 0
        self.time = 0

    def say_state(self):
        print("testing testing")

    def accelerate(self):
        self.speed += 5

    def brake(self):
        self.speed -= 5

    def step(self):
        self.time += 1

    def average_speed(self):
        return self.odometer / self.time

if __name__ == '__main__':
    my_car = Car()
    print(my_car.say_state())
    print(my_car.average_speed())