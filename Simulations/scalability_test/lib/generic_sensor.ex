defmodule ScalabilityTest.GenericSensor do
  @moduledoc false

  use GenServer

  def start_link(initial) do
    GenServer.start(__MODULE__, initial)
  end

  def init(args) do
    {client_id, topic} = args

    mqtt_config = Application.get_env(:scalability_test, :mqtt)

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
      message_count: mqtt_config[:max_message_count]
    }

    {:ok, reset_timer(state), {:continue, :start}}
  end

  def handle_continue(:start, state) do
    {:noreply, state}
  end

  @doc """

  """
  def handle_info(:tick, %{message_count: message_count} = state) when message_count == 0 do
    # Supervisor.stop(Tortoise.Supervisor)
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
    Tortoise.publish(client_id, topic, Float.to_string(1.01))
  end

  defp reset_timer(state) do
    if state.timer do
      Process.cancel_timer(state.timer)
    end
    timer = Process.send_after(self(), :tick, state.interval_mills)
    %{state | timer: timer}
  end
end
