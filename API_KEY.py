import os

city_location = "101230101"
openai_key = "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"
weather_key = "e2774b7beb8a4bdea88b24d089f95360"

script_dir = os.path.dirname(os.path.abspath(__file__))
vits_model_path = os.path.join(script_dir, 'model', 'tts', 'G_latest.pth')
vits_config_path = os.path.join(
    script_dir, 'model', 'tts', 'config.json')