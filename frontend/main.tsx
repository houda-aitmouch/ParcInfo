import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./styles/globals.css";

// Version simplifiée pour tester
function mountApp() {
  const container = document.querySelector(".react-root");
  if (container) {
    const root = createRoot(container);
    root.render(
      <React.StrictMode>
        <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
          <h1>🚀 ParcInfo - Gestion de Parc Informatique</h1>
          <p>Application React fonctionne correctement !</p>
          <App />
        </div>
      </React.StrictMode>
    );
  } else {
    console.error("Element .react-root not found");
  }
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", mountApp);
} else {
  mountApp();
}


