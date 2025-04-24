defmodule DashboardWeb.AmbientLive.Index do
  alias Phoenix.PubSub
  use DashboardWeb, :live_view

  require Logger

  @impl true
  def mount(_params, _session, socket) do

    PubSub.subscribe(Dashboard.PubSub, "measurements/ambient")

    vals = Map.new()
    plots = %{
      light_level: nil,
      temperature: nil,
      humidity: nil}
    reports = %{
      light_level: [],
      temperature: [],
      humidity: []}

    {:ok, assign(socket,
      ambient_values: vals,
      plots: plots,
      reports: reports)}
  end

  @impl true
  def handle_params(_params, _url, socket) do
    {:noreply, socket}
  end

  @impl true
  def handle_event(name, data, socket) do
    Logger.info("handle_event: #{inspect([name, data])}")
    {:noreply, socket}
  end

  @impl true
  def handle_info({:update, key, val}, socket) do
    current_vals = socket.assigns[:ambient_values]
    val = case key == :light_level do
      false -> val
      true -> round((val / 3.3) * 100)
    end

    updated_vals = case Map.has_key?(current_vals, key) do
      true -> Map.put(current_vals, key, val)
      false -> Map.put_new(current_vals, key, val)
    end

    {key_reports, plot} = update_plot(key, val, socket)
    reports = Map.put(socket.assigns[:reports], key, key_reports)
    plots = Map.put(socket.assigns[:plots], key, plot)

    {:noreply, assign(socket,
      ambient_values: updated_vals,
      reports: reports,
      plots: plots)}
  end

  def handle_info(_, socket) do
    {:noreply, socket}
  end

  defp update_plot(key, val, socket) do
    now = DateTime.utc_now()
    new_report = {now, val}
    deadline = DateTime.add(now, - 2 * Application.get_env(:dashboard, :timespan), :second)
    reports = [new_report | socket.assigns[:reports][key]]
      |> Enum.filter(fn {dt, _} -> DateTime.compare(dt, deadline) == :gt end)
      |> Enum.sort()

    {reports, plot(reports, deadline, now)}
  end

  defp plot(reports, deadline, now) do
    max = reports
    |> Enum.map(fn {_, val} -> val end)
    |> Enum.max()
    min = reports
    |> Enum.map(fn {_, val} -> val end)
    |> Enum.min()

    x_scale = Contex.TimeScale.new()
      |> Contex.TimeScale.domain(deadline, now)
      |> Contex.TimeScale.interval_count(10)

    y_scale = Contex.ContinuousLinearScale.new()
      |> Contex.ContinuousLinearScale.domain(min - 1, max + 1)

    options = [
      smoothed: false,
      custom_x_scale: x_scale,
      custom_y_scale: y_scale,
      custom_x_formatter: &x_formatter/1,
      axis_lavel_rotation: 45
    ]

    reports
    |> Enum.map(fn {dt, val} -> [dt, val] end)
    |> Contex.Dataset.new()
    |> Contex.Plot.new(Contex.LinePlot, 600, 250, options)
    |> Contex.Plot.to_svg()
  end

  defp x_formatter(datetime) do
    datetime
    |> Calendar.strftime("%H:%M:%S")
  end
end
