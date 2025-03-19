import Config

config :scalability_test, test_filename: "1bay.json"

config :scalability_test, :mqtt,
  host: "192.168.68.63",
  port: 1883,
  max_message_count: 10
