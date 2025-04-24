defmodule Dashboard.SensorAggregator do
  @moduledoc false
  alias Phoenix.PubSub

  use GenServer

  def start_link(initial) do
    GenServer.start(__MODULE__, initial)
  end

  def init(args) do
    [emqtt, config] = args

    {:ok, pid} = :emqtt.start_link(emqtt)
    {:ok, _} = :emqtt.connect(pid)

    measurements = Map.from_keys(config[:sub_topics], [])
    # Subscribe to each topic
    Enum.each(config[:sub_topics],
      fn t ->
        {:ok, _, _} = :emqtt.subscribe(pid, config[:base_sub_topic] <> Atom.to_string(t))
      end)

    state = %{
      pid: pid,
      base_pub_topic: config[:base_pub_topic],
      buffer_size: config[:buffer_size],
      measurements: measurements
    }

    {:ok, state, {:continue, :start}}
  end

  def handle_continue(:start, state) do
    {:noreply, state}
  end

  def handle_info({:publish, packet}, state) do
    split_topic = String.split(packet[:topic], "/")
    measurement_key = String.to_atom(Enum.join(Enum.take(split_topic, -1)))

    {:ok, state } = case Float.parse(packet[:payload]) do
      {num, _} -> update_buffer(num, measurement_key, state)
      {_} -> publish_buffer(measurement_key, state)
    end

    {:noreply, state}
  end

  def handle_info(_, state) do
    {:noreply, state}
  end


  defp update_buffer(num, key, %{buffer_size: max_size, measurements: measurements} = state) do
    buffer = case length(measurements[key]) >= max_size do
      true -> List.delete_at(measurements[key], - 1)
      false -> measurements[key]
    end

    measurements = Map.put(measurements, key, [num | buffer])
    state = %{state | measurements: measurements}

    publish_buffer(key, state)

    {:ok, state}
  end

  defp publish_buffer(key, %{pid: pid, measurements: measurements, base_pub_topic: topic} = state) do
    avg = Float.round(Enum.sum(measurements[key]) / length(measurements[key]), 3)
    :emqtt.publish(pid, topic <> Atom.to_string(key), Float.to_string(avg))
    # Broadcast within dashboard app
    PubSub.broadcast(Dashboard.PubSub, "measurements/ambient", {:update, key, avg})
    {:ok, state}
  end

end
