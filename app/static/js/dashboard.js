(function () {
  const table = document.getElementById("dashboard-table");
  if (!table || !window.MonitoringRefresh) return;

  function render(data) {
    const byId = {};
    (data.servers || []).forEach(function (s) {
      byId[s.id] = s;
    });
    table.querySelectorAll("tbody tr[data-server-id]").forEach(function (row) {
      const s = byId[row.getAttribute("data-server-id")];
      if (!s) return;
      row.querySelector(".metric-cpu").textContent = s.cpu_percent.toFixed(1) + "%";
      row.querySelector(".metric-mem").textContent = s.memory.percent.toFixed(1) + "%";
      row.querySelector(".metric-net-in").textContent = s.network.in_mbps.toFixed(2) + " Mbps";
      row.querySelector(".metric-net-out").textContent = s.network.out_mbps.toFixed(2) + " Mbps";
    });
  }

  MonitoringRefresh.start("/api/dashboard", render);
})();
