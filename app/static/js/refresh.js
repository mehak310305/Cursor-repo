/* Shared 5s same-origin fetch helper (session cookies only; no credentials in JS). */
window.MonitoringRefresh = {
  intervalMs: 5000,
  async fetchJson(url) {
    const response = await fetch(url, {
      credentials: "same-origin",
      headers: { Accept: "application/json" },
    });
    if (response.status === 401 || response.status === 302) {
      window.location.href = "/login";
      return null;
    }
    if (!response.ok) {
      throw new Error("Request failed: " + response.status);
    }
    return response.json();
  },
  start(url, onData) {
    const tick = async () => {
      try {
        const data = await this.fetchJson(url);
        if (data) onData(data);
      } catch (_err) {
        /* keep polling; transient errors are fine for a demo */
      }
    };
    tick();
    return setInterval(tick, this.intervalMs);
  },
};
