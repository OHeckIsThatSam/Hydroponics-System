import Config

config :scalability_test, test_filename: "100bays.json"

config :scalability_test, is_resilience_test: false
config :scalability_test, fail_percent: 20

config :scalability_test, :mqtt,
  host: "192.168.68.63",
  port: 1883,
  max_message_count: 100
