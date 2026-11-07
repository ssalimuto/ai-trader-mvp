const API_BASE = "";

function setToken(token) {
  if (token) {
    localStorage.setItem("token", token);
  } else {
    localStorage.removeItem("token");
  }
}

function getToken() {
  return localStorage.getItem("token");
}

function getAuthHeaders(extraHeaders = {}) {
  const token = getToken();
  return {
    ...extraHeaders,
    ...(token ? { Authorization: `Bearer ${token}` } : {})
  };
}

function showStatus(elId, message, isError = false) {
  const el = document.getElementById(elId);
  if (!el) return;
  el.textContent = message;
  el.style.color = isError ? "#ff8a8a" : "#9fe7a7";
}

async function apiRequest(endpoint, options = {}) {
  const defaultHeaders = {
    "Content-Type": "application/json"
  };

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      ...defaultHeaders,
      ...getAuthHeaders(options.headers || {})
    }
  });

  const contentType = response.headers.get("content-type") || "";
  const isJson = contentType.includes("application/json");

  let data = null;
  try {
    data = isJson ? await response.json() : await response.text();
  } catch (error) {
    data = null;
  }

  if (!response.ok) {
    const message = (data && data.detail) || (data && data.message) || "Request failed";
    throw new Error(message);
  }

  return data;
}

async function login() {
  const username = prompt("Username");
  const password = prompt("Password");

  if (!username || !password) {
    alert("Username and password are required.");
    return;
  }

  try {
    const form = new URLSearchParams();
    form.append("username", username);
    form.append("password", password);

    const response = await fetch(`${API_BASE}/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      body: form.toString()
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Login failed");
    }

    if (data.access_token) {
      setToken(data.access_token);
      alert("Logged in successfully.");
      showStatus("authStatus", "Authenticated", false);
      await loadTrades();
    } else {
      throw new Error("No token returned");
    }
  } catch (error) {
    console.error(error);
    alert(error.message || "Login failed");
    showStatus("authStatus", error.message || "Login failed", true);
  }
}

async function signup() {
  const email = prompt("Email");
  const username = prompt("Username");
  const password = prompt("Password");

  if (!email || !username || !password) {
    alert("Email, username, and password are required.");
    return;
  }

  try {
    const data = await apiRequest("/signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ email, username, password })
    });

    alert(data.message || "Signup successful.");
  } catch (error) {
    console.error(error);
    alert(error.message || "Signup failed");
  }
}

async function askAI() {
  const question = document.getElementById("question")?.value?.trim();
  const answerBox = document.getElementById("aiAnswer");
  if (!question) {
    showStatus("aiStatus", "Please enter a question.", true);
    return;
  }

  try {
    const data = await apiRequest("/ai/query", {
      method: "POST",
      body: JSON.stringify({ question })
    });

    if (answerBox) {
      answerBox.innerHTML = `<pre>${(data.answer || "No answer").replace(/</g, "&lt;")}</pre>`;
    }
    showStatus("aiStatus", "AI answered successfully.", false);
  } catch (error) {
    console.error(error);
    showStatus("aiStatus", error.message || "AI request failed.", true);
    if (answerBox) answerBox.innerHTML = "<pre>Request failed</pre>";
  }
}

async function placeTrade() {
  const symbol = document.getElementById("symbol")?.value?.trim();
  const side = document.getElementById("side")?.value;
  const quantity = Number(document.getElementById("qty")?.value || 0);
  const price = Number(document.getElementById("price")?.value || 0);

  if (!symbol || !side) {
    alert("Symbol and side are required.");
    return;
  }

  try {
    const data = await apiRequest("/paper-trade", {
      method: "POST",
      body: JSON.stringify({
        symbol,
        side,
        quantity,
        price
      })
    });

    const resultBox = document.getElementById("tradeResult");
    if (resultBox) {
      resultBox.textContent = JSON.stringify(data, null, 2);
    }

    await loadTrades();
  } catch (error) {
    console.error(error);
    alert(error.message || "Trade failed");
  }
}

async function loadTrades() {
  if (!getToken()) return;

  try {
    const data = await apiRequest("/trades");
    const list = document.getElementById("tradeList");
    if (!list) return;

    if (!data.trades || data.trades.length === 0) {
      list.innerHTML = "<p>No trades yet.</p>";
      return;
    }

    list.innerHTML = data.trades
      .map(
        (trade) => `
          <div class="trade-item">
            <strong>${trade.symbol}</strong> - ${trade.side}
            <span>Qty: ${trade.quantity}</span>
            <span>Price: ${trade.price}</span>
            <span>Status: ${trade.status}</span>
          </div>
        `
      )
      .join("");
  } catch (error) {
    console.error(error);
    const list = document.getElementById("tradeList");
    if (list) list.innerHTML = "<p>Unable to load trades.</p>";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const loginBtn = document.getElementById("loginBtn");
  const signupBtn = document.getElementById("signupBtn");
  const askAiBtn = document.getElementById("askAI");
  const placeTradeBtn = document.getElementById("placeTrade");

  if (loginBtn) loginBtn.addEventListener("click", login);
  if (signupBtn) signupBtn.addEventListener("click", signup);
  if (askAiBtn) askAiBtn.addEventListener("click", askAI);
  if (placeTradeBtn) placeTradeBtn.addEventListener("click", placeTrade);

  if (getToken()) {
    loadTrades();
  }
});
