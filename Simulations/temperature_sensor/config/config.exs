import Config

config :temperature_sensor, :emqtt,
  host: "192.168.68.63",
  port: 1883,
  clientid: "temp_sensor",
  clean_start: false,
  name: :emqtt

config :temperature_sensor, :topic, "sensor/ambient/temperature"

config :temperature_sensor, :interval, 1000
