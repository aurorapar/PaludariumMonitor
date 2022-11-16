import adafruit_dht
import board


class DHT22(adafruit_dht.DHT22):
    def __init__(self, pin):
        try:
            super().__init__(pin, False)
        except e:
            print(e)
            print("You didn't pass in a correct pin. Do board.D{BCM PIN NUMBER}")
            exit()

    def get_temperature(self):
        return self.temperature

    def get_humidity(self):
        return self.humidity
