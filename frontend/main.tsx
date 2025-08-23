import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./styles/globals.css";
import { Dashboard } from "./components/Dashboard";
import { CommandesIT } from "./components/CommandesIT";
import { CommandesBureau } from "./components/CommandesBureau";
import { MaterielsIT } from "./components/MaterielsIT";
import { MaterielsBureau } from "./components/MaterielsBureau";
import { Livraisons } from "./components/Livraisons";
import { Demandes } from "./components/Demandes";
import { Fournisseurs } from "./components/Fournisseurs";
import { Utilisateurs } from "./components/Utilisateurs";
import { Profile } from "./components/Profile";
import { AdminDashboardShell } from "./components/AdminShell";

function mountAll() {
  const containers = document.querySelectorAll<HTMLElement>(".react-root");
  containers.forEach((el) => {
    if ((el as any)._reactMounted) return;
    (el as any)._reactMounted = true;
    const component = el.dataset.component || "App";
    const props = el.dataset.props ? JSON.parse(el.dataset.props) : {};
    const root = createRoot(el);
    const render = () => {
      switch (component) {
        case "Dashboard":
          return <AdminDashboardShell {...props} />;
        case "CommandesIT":
          return <CommandesIT {...props} />;
        case "CommandesBureau":
          return <CommandesBureau {...props} />;
        case "MaterielsIT":
          return <MaterielsIT {...props} />;
        case "MaterielsBureau":
          return <MaterielsBureau {...props} />;
        case "Livraisons":
          return <Livraisons {...props} />;
        case "Demandes":
          return <Demandes {...props} />;
        case "Fournisseurs":
          return <Fournisseurs {...props} />;
        case "Utilisateurs":
          return <Utilisateurs {...props} />;
        case "Profile":
          return <Profile {...props} />;
        case "App":
        default:
          return <App />;
      }
    };
    root.render(<React.StrictMode>{render()}</React.StrictMode>);
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", mountAll);
} else {
  mountAll();
}


