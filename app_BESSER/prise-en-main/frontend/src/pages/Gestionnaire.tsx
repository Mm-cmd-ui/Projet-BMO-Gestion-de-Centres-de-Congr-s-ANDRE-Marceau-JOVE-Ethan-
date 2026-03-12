import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";
import { MethodButton } from "../components/MethodButton";

const Gestionnaire: React.FC = () => {
  return (
    <div id="page-gestionnaire-0">
    <div id="ilk8g" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="i23od" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="i3huh" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="i0jpr" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}}>
          <a id="i8k5j" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "rgba(255,255,255,0.2)", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/gestionnaire">{"gestionnaire"}</a>
          <a id="is1ki" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/reservation">{"reservation"}</a>
          <a id="ittk5" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/evenement_salle">{"Evenement_Salle"}</a>
        </div>
        <p id="ij3hf" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="i4e4e" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="i9li8" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"gestionnaire"}</h1>
        <p id="i0ahc" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"Manage gestionnaire data"}</p>
        <TableBlock id="table-gestionnaire-0" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="gestionnaire List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "Identitfiant", "column_type": "field", "field": "identitfiant", "type": "str", "required": true}, {"label": "Nom", "column_type": "field", "field": "nom", "type": "str", "required": true}, {"label": "Reservation", "column_type": "lookup", "path": "reservation", "entity": "reservation", "field": "nomEvenement", "type": "list", "required": false}], "formColumns": [{"column_type": "field", "field": "identitfiant", "label": "identitfiant", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "nom", "label": "nom", "type": "str", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "reservation", "field": "reservation", "lookup_field": "nomEvenement", "entity": "reservation", "type": "list", "required": false}]}} dataBinding={{"entity": "gestionnaire", "endpoint": "/gestionnaire/"}} />
        <div id="i51b9" style={{"marginTop": "20px", "display": "flex", "gap": "10px", "flexWrap": "wrap", "--chart-color-palette": "default"}}>
          <MethodButton id="iudvg" className="action-button-component" style={{"display": "inline-flex", "alignItems": "center", "padding": "6px 14px", "background": "linear-gradient(90deg, #2563eb 0%, #1e40af 100%)", "color": "#fff", "textDecoration": "none", "borderRadius": "4px", "fontSize": "13px", "fontWeight": "600", "letterSpacing": "0.01em", "cursor": "pointer", "border": "none", "boxShadow": "0 1px 4px rgba(37,99,235,0.10)", "transition": "background 0.2s", "--chart-color-palette": "default"}} endpoint="/gestionnaire/{gestionnaire_id}/methods/consulterStats/" label="+ consulterStats" parameters={[{"name": "periode_nom", "type": "any", "required": true}]} isInstanceMethod={true} instanceSourceTableId="table-gestionnaire-0" />
        </div>
      </main>
    </div>    </div>
  );
};

export default Gestionnaire;
