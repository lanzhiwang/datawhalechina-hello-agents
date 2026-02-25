import requests
import os
from dotenv import load_dotenv

load_dotenv()


class Weather:
    """天气查询类，封装OpenWeatherMap API功能"""

    def __init__(self, api_key=None, unit="metric"):
        """
        初始化Weather类
        :param api_key: OpenWeatherMap API密钥，默认为环境变量中的OPENWEATHER_API_KEY
        :param unit: 温度单位（metric=摄氏，imperial=华氏）
        """
        self.api_key = api_key or os.environ.get("OPENWEATHER_API_KEY")
        self.unit = unit
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

        # 如果没有API密钥，使用模拟数据
        self.demo_mode = not self.api_key
        if self.demo_mode:
            print("⚠️  警告: 未设置API密钥，使用演示模式")
            print("   请设置OPENWEATHER_API_KEY环境变量以获得真实天气数据")

    def get_weather(self, city_name):
        """
        查询指定城市的天气信息
        :param city_name: 城市名称（英文）
        :return: 格式化后的天气信息字符串
        """
        # 如果是演示模式，使用模拟数据
        if self.demo_mode:
            return self._get_demo_weather()

        params = {"q": city_name, "appid": self.api_key, "units": self.unit}

        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()

            if response.status_code == 200:
                return self._format_weather_data(data)
            else:
                return f"错误 {data['cod']}: {data['message']}"

        except Exception as e:
            return f"请求失败: {str(e)}"

    def get_weather_details(self, city_name):
        """
        获取详细的天气数据（字典格式）
        :param city_name: 城市名称（英文）
        :return: 包含详细天气数据的字典
        """
        # 如果是演示模式，使用模拟数据
        if self.demo_mode:
            return self._get_demo_weather()

        params = {"q": city_name, "appid": self.api_key, "units": self.unit}

        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()

            if response.status_code == 200:
                return self._parse_weather_data(data)
            else:
                return {"error": f"错误 {data['cod']}: {data['message']}"}

        except Exception as e:
            return {"error": f"请求失败: {str(e)}"}

    def _get_demo_weather(self):
        return {
            "city": "shanghai",
            "temperature": 25,
            "temperature_unit": "°C",
            "description": "晴天",
            "humidity": 60,
            "wind_speed": 10,
            "wind_unit": "m/s",
        }

    def _parse_weather_data(self, data):
        """
        解析天气数据为字典格式
        :param data: API返回的原始数据
        :return: 解析后的天气数据字典
        """
        weather_desc = data["weather"][0]["description"].title()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        city = data["name"]

        return {
            "city": city,
            "temperature": temp,
            "temperature_unit": "°C" if self.unit == "metric" else "°F",
            "description": weather_desc,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "wind_unit": "m/s",
        }

    def _format_weather_data(self, data):
        """
        格式化天气数据为字符串
        :param data: API返回的原始数据
        :return: 格式化后的天气信息字符串
        """
        weather_data = self._parse_weather_data(data)

        return (
            f"🏙️ 城市: {weather_data['city']}\n"
            f"🌡️ 温度: {weather_data['temperature']}{weather_data['temperature_unit']}\n"
            f"📝 天气: {weather_data['description']}\n"
            f"💧 湿度: {weather_data['humidity']}%\n"
            f"🌬️ 风速: {weather_data['wind_speed']} {weather_data['wind_unit']}"
        )

    def set_unit(self, unit):
        """
        设置温度单位
        :param unit: 温度单位（metric=摄氏，imperial=华氏）
        """
        if unit not in ["metric", "imperial"]:
            raise ValueError("单位必须是 'metric' 或 'imperial'")
        self.unit = unit

    def set_api_key(self, api_key):
        """
        设置API密钥
        :param api_key: 新的API密钥
        """
        self.api_key = api_key


def get_weather(
    city_name, api_key=os.environ.get("OPENWEATHER_API_KEY"), unit="metric"
):
    """
    向后兼容的函数，使用Weather类实现
    :param city_name: 城市名称（英文）
    :param api_key: 你的OpenWeatherMap API密钥
    :param unit: 温度单位（metric=摄氏，imperial=华氏）
    :return: 格式化后的天气信息
    """
    weather = Weather(api_key=api_key, unit=unit)
    return weather.get_weather(city_name)


# 使用示例
if __name__ == "__main__":
    weather = Weather()
    weather_info = weather.get_weather("harbin")
    print(weather_info)
