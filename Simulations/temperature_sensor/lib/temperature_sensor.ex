defmodule TemperatureSensor do
  @moduledoc false

  use GenServer

  def start_link([]) do
    GenServer.start(__MODULE__, [])
  end

  def init([]) do
    config = Application.get_all_env(:temperature_sensor)
    emqtt_opts = config[:emqtt]
    publish_topic = config[:topic]
    interval = config[:interval]

    {:ok, pid} = :emqtt.start_link(emqtt_opts)
    state = %{
      interval: interval,
      timer: nil,
      topic: publish_topic,
      pid: pid
    }

    {:ok, _} = :emqtt.connect(pid)

    {:ok, reset_timer(state), {:continue, :start_emqtt}}
  end

  def handle_continue(:start_emqtt, %{pid: pid} = state) do
    # Add inital subscriptions in here.
    {:noreply, state}
  end

  @doc """

  """
  def handle_info(:tick, %{topic: topic, pid: pid} = state) do
    publish_temperature(pid, topic)
    {:noreply, reset_timer(state)}
  end

  def handle_info(_, state) do
    {:noreply, state}
  end


  defp publish_temperature(pid, topic) do
    temp = 15.0 + (5 * :rand.normal())
    payload = Float.to_string(temp)
    :emqtt.publish(pid, topic, payload)
  end


  defp reset_timer(state) do
    if state.timer do
      Process.cancel_timer(state.timer)
    end
    timer = Process.send_after(self(), :tick, state.interval)
    %{state | timer: timer}
  end
end
