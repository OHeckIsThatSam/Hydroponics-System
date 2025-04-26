defmodule ScalabilityTest.GenericSensor do
  @moduledoc false
alias IEx.App

  use GenServer

  def start_link(initial) do
    GenServer.start(__MODULE__, initial)
  end

  def init(args) do
    {client_id, topic} = args

    mqtt_config = Application.get_env(:scalability_test, :mqtt)
    is_resilience_test = Application.get_env(:scalability_test, :is_resilience_test)
    fail_percent = Application.get_env(:scalability_test, :fail_percent)

    message_count = mqtt_config[:max_message_count]
    message_count = case is_resilience_test do
      true -> set_fail_message_count(message_count, fail_percent)
      false -> message_count
    end

    {:ok, pid} = Tortoise.Supervisor.start_child(
      client_id: client_id,
      handler: {Tortoise.Handler.Logger, []},
      server: {Tortoise.Transport.Tcp, host: mqtt_config[:host], port: mqtt_config[:port]}
    )

    state = %{
      pid: pid,
      client_id: client_id,
      timer: nil,
      interval_mills: 1000,
      topic: topic,
      message_count: message_count

    }

    {:ok, reset_timer(state), {:continue, :start}}
  end

  def handle_continue(:start, state) do
    {:noreply, state}
  end

  def handle_info(:tick, %{message_count: message_count, client_id: client_id} = state) when message_count == 0 do
    Tortoise.Connection.disconnect(client_id)
    {:stop, :normal, state}
  end

  def handle_info(:tick, %{client_id: client_id, topic: topic} = state) do
    publish(client_id, topic)
    {:noreply, reset_timer(%{state | message_count: state.message_count - 1})}
  end

  def handle_info(_, state) do
    {:noreply, state}
  end


  defp publish(client_id, topic) do
    type = String.split(topic, "/")
    |> Enum.take(-1)
    |> Enum.join()

    payload = case type do
      "temperature" -> :rand.uniform(30)
      "humidity" -> :rand.uniform() * 100
      "light_level" -> :rand.uniform() * 3.3
      "water_temperature" -> :rand.uniform(30)
      "water_level" -> :rand.uniform()
      "water_ph" -> :rand.uniform(14)
      "water_conductivity" -> :rand.uniform()
      _ -> 0
    end

    Tortoise.publish(client_id, topic, "#{payload}")
  end

  defp reset_timer(state) do
    if state.timer do
      Process.cancel_timer(state.timer)
    end
    timer = Process.send_after(self(), :tick, state.interval_mills)
    %{state | timer: timer}
  end

  defp set_fail_message_count(count, chance) do
    cond do
      :rand.uniform() <= chance / 100 -> 2
      true -> count
    end
  end
end
