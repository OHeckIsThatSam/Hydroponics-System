defmodule TemperatureSensor.Application do
  @moduledoc false

  use Application

  @impl true
  def start(_type, _args) do
    children = [
      TemperatureSensor
    ]

    opts = [strategy: :one_for_one, name: TemperatureSensor.Supervisor]
    Supervisor.start_link(children, opts)
  end
end
