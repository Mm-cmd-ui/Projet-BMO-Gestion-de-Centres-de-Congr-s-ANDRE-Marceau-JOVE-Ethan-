import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { TableProvider } from "./contexts/TableContext";
import Gestionnaire from "./pages/Gestionnaire";
import Stats from "./pages/Stats";
import Reservation from "./pages/Reservation";
import Disponibilites from "./pages/Disponibilites";
import Materielsprestations from "./pages/Materielsprestations";
import Evenementsalle from "./pages/Evenementsalle";
import Tarifs from "./pages/Tarifs";
import Centredecongres from "./pages/Centredecongres";

function App() {
  return (
    <TableProvider>
      <div className="app-container">
        <main className="app-main">
          <Routes>
            <Route path="/gestionnaire" element={<Gestionnaire />} />
            <Route path="/stats" element={<Stats />} />
            <Route path="/reservation" element={<Reservation />} />
            <Route path="/disponibilites" element={<Disponibilites />} />
            <Route path="/materielsprestations" element={<Materielsprestations />} />
            <Route path="/evenementsalle" element={<Evenementsalle />} />
            <Route path="/tarifs" element={<Tarifs />} />
            <Route path="/centredecongres" element={<Centredecongres />} />
            <Route path="/" element={<Navigate to="/gestionnaire" replace />} />
            <Route path="*" element={<Navigate to="/gestionnaire" replace />} />
          </Routes>
        </main>
      </div>
    </TableProvider>
  );
}
export default App;
