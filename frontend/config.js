/**
 * LocalJobs Frontend Configuration
 * Manages API Base URL and Telephony Mode across environments.
 */

// If deployed on static hosts like Cloudflare Pages, set default backend URL:
window.LOCALJOBS_CONFIG = {
  // In development/same-host, empty string uses relative paths
  DEFAULT_API_BASE: "",
  TELEPHONY_MODE: "MOCK"
};

function getApiBaseUrl() {
  const custom = localStorage.getItem("LOCALJOBS_CUSTOM_API_URL");
  if (custom && custom.trim()) {
    return custom.trim().replace(/\/+$/, "");
  }
  // Check if Vite or script injected VITE_API_BASE_URL
  if (window.VITE_API_BASE_URL) {
    return window.VITE_API_BASE_URL.replace(/\/+$/, "");
  }
  if (window.LOCALJOBS_API_BASE_URL) {
    return window.LOCALJOBS_API_BASE_URL.replace(/\/+$/, "");
  }
  // Fallback: if served directly via file:// or different port, default to backend standard port
  if (window.location.protocol === "file:") {
    return "http://127.0.0.1:8000";
  }
  return window.LOCALJOBS_CONFIG.DEFAULT_API_BASE || "";
}

function setCustomApiUrl(url) {
  if (url && url.trim()) {
    localStorage.setItem("LOCALJOBS_CUSTOM_API_URL", url.trim().replace(/\/+$/, ""));
  } else {
    localStorage.removeItem("LOCALJOBS_CUSTOM_API_URL");
  }
  window.location.reload();
}

async function loadTelephonyBanner() {
  const api = getApiBaseUrl();
  try {
    const res = await fetch(`${api}/telephony/status`);
    if (res.ok) {
      const data = await res.json();
      const badgeElem = document.getElementById("telephony-mode-badge");
      const phoneElem = document.getElementById("telephony-phone-display");
      const descElem = document.getElementById("telephony-desc-display");
      const noteElem = document.getElementById("telephony-banner-note");

      if (badgeElem) badgeElem.innerText = data.badge || data.mode;
      if (phoneElem) phoneElem.innerText = data.phone_display;
      if (descElem) descElem.innerText = data.description;

      if (data.is_mock && noteElem) {
        noteElem.style.display = "block";
      }
    }
  } catch (e) {
    console.warn("Unable to fetch telephony status from backend:", e);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  loadTelephonyBanner();
});
