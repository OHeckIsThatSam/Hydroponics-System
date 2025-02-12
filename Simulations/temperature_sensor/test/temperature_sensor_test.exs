defmodule TemperatureSensorTest do
  use ExUnit.Case
  doctest TemperatureSensor

  test "greets the world" do
    assert TemperatureSensor.hello() == :world
  end
end
