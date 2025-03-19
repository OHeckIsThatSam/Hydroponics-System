defmodule ScalabilityTest.Application do
  @moduledoc false

  use Application

  @impl true
  def start(_type, _args) do
    children = [
      {PartitionSupervisor,
       child_spec: DynamicSupervisor,
       name: ScalabilityTest.DynamicSupervisors}
    ]

    {:ok, pid} = Supervisor.start_link(children, strategy: :one_for_one)

    parse_schema()

    {:ok, pid}
  end


  defp parse_schema() do
    path = File.cwd!()
    file = Application.get_env(:scalability_test, :test_filename)

    {:ok, json} = File.read("#{path}/test_schemas/#{file}")
    {:ok, schema} = JSON.decode(json)

    Enum.each(schema["ambient_sensors"], &create_sensors(&1, "measurements/ambient"))

    bay_count = schema["bay_count"]
    cond do
      not is_integer(bay_count) -> raise ArgumentError, message: "bay_count must be an integer"
      bay_count < 0 -> raise ArgumentError, message: "bay_count must be greater than 0"
      bay_count > 999 -> raise ArgumentError, message: "bay_count must be smaller than 999"
      bay_count == 0 -> :ok
      true -> Enum.each(1..bay_count, &create_bay_sensors(&1, schema["bay_sensors"]))
    end
  end

  defp create_bay_sensors(count, types) do
    Enum.each(types, &create_sensors(&1, "measurements/bay-#{count}"))
  end

  defp create_sensors({type, count} = _sensor, topic) do
    Enum.each(1..count, &create_sensor(&1, type, topic))
  end

  defp create_sensor(_, type, topic) do
    clientid = UUID.uuid4()

    DynamicSupervisor.start_child(
      {:via, PartitionSupervisor, {ScalabilityTest.DynamicSupervisors, self()}},
      {ScalabilityTest.GenericSensor, {clientid, "#{topic}/#{clientid}/#{type}"}}
    )
  end
end
