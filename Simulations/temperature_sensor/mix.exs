defmodule TemperatureSensor.MixProject do
  use Mix.Project

  def project do
    [
      app: :temperature_sensor,
      version: "0.1.0",
      elixir: "~> 1.17",
      start_permanent: Mix.env() == :prod,
      deps: deps()
    ]
  end

  # Run "mix help compile.app" to learn about applications.
  def application do
    [
      extra_applications: [:logger],
      mod: {TemperatureSensor.Application, []}
    ]
  end

  # Run "mix help deps" to learn about dependencies.
  defp deps do
    [
      {:emqtt, github: "emqx/emqtt", tag: "1.14.0", system_env: [{"BUILD_WITHOUT_QUIC", "1"}]}
    ]
  end
end
