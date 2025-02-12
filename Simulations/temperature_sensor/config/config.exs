import Config

config :temperature_sensor, :emqtt,
  host: "127.0.0.1",
  port: 1883,
  clientid: "temp_sensor",
  clean_start: false,
  name: :emqtt

config :temperature_sensor, :topic, "ambient/temperature"

config :temperature_sensor, :interval, 1000
