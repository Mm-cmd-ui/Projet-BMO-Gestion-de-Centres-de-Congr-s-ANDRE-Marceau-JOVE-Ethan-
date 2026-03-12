import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { TableProvider } from "./contexts/TableContext";
import Gestionnaire from "./pages/Gestionnaire";
import Reservation from "./pages/Reservation";
import EvenementSalle from "./pages/EvenementSalle";

function App() {
  return (
    <TableProvider>
      <div className="app-container">
        <main className="app-main">
          <Routes>
            <Route path="/gestionnaire" element={<Gestionnaire />} />
            <Route path="/reservation" element={<Reservation />} />
            <Route path="/evenement_salle" element={<EvenementSalle />} />
            <Route path="/" element={<Navigate to="/gestionnaire" replace />} />
            <Route path="*" element={<Navigate to="/gestionnaire" replace />} />
          </Routes>
        </main>
      </div>
    </TableProvider>
  );
}
export default App;
