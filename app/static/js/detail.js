(function () {
  const root = document.getElementById("detail-metrics");
  if (!root || !window.MonitoringRefresh) return;
  const serverId = root.getAttribute("data-server-id");

  function render(data) {
    document.getElementById("detail-cpu").textContent =
      data.cpu_percent.toFixed(1) + "%";
    document.getElementById("detail-mem").textContent =
      data.memory.used_mb.toFixed(0) +
      " / " +
      data.memory.total_mb.toFixed(0) +
      " MB (" +
      data.memory.percent.toFixed(1) +
      "%)";
    document.getElementById("detail-net").textContent =
      "In " +
      data.network.in_mbps.toFixed(2) +
      " Mbps · Out " +
      data.network.out_mbps.toFixed(2) +
      " Mbps";

    const tbody = document.querySelector("#ports-table tbody");
    tbody.textContent = "";
    (data.listening_ports || []).forEach(function (p) {
      const tr = document.createElement("tr");
      const port = document.createElement("td");
      port.textContent = String(p.port);
      const proto = document.createElement("td");
      proto.textContent = p.protocol;
      const proc = document.createElement("td");
      proc.textContent = p.process;
      tr.appendChild(port);
      tr.appendChild(proto);
      tr.appendChild(proc);
      tbody.appendChild(tr);
    });
  }

  MonitoringRefresh.start("/api/servers/" + encodeURIComponent(serverId), render);
})();
