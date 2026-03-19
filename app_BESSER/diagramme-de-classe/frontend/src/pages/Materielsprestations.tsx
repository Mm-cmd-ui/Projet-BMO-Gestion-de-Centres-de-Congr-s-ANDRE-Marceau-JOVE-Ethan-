import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";
import { MethodButton } from "../components/MethodButton";

const Materielsprestations: React.FC = () => {
  return (
    <div id="page-materielsprestations-4">
    <div id="iqghao" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="ijqmxs" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="i9rzrt" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="io4o96" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}}>
          <a id="ip1u0e" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/gestionnaire">{"Gestionnaire"}</a>
          <a id="irt1ef" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/stats">{"Stats"}</a>
          <a id="ishtlx" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/reservation">{"Reservation"}</a>
          <a id="iat7vl" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/disponibilites">{"Disponibilites"}</a>
          <a id="idhfk8" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "rgba(255,255,255,0.2)", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/materielsprestations">{"Materielsprestations"}</a>
          <a id="izjgpl" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/evenementsalle">{"EvenementSalle"}</a>
          <a id="i5dau2" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/tarifs">{"Tarifs"}</a>
          <a id="i9tqx1" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/centredecongres">{"CentredeCongres"}</a>
        </div>
        <p id="iowpif" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="i07nlx" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="iyhp8u" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"Materielsprestations"}</h1>
        <p id="il51uk" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"Manage Materielsprestations data"}</p>
        <TableBlock id="table-materielsprestations-4" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Materielsprestations List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "Nom", "column_type": "field", "field": "nom", "type": "str", "required": true}, {"label": "Type", "column_type": "field", "field": "type", "type": "str", "required": true}, {"label": "QuantiteMax", "column_type": "field", "field": "quantiteMax", "type": "int", "required": true}, {"label": "PrixUnitaire", "column_type": "field", "field": "prixUnitaire", "type": "float", "required": true}], "formColumns": [{"column_type": "field", "field": "nom", "label": "nom", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "type", "label": "type", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "quantiteMax", "label": "quantiteMax", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "prixUnitaire", "label": "prixUnitaire", "type": "float", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "reservation_3", "field": "reservation_3", "lookup_field": "delaiConfirmation", "entity": "Reservation", "type": "str", "required": true}, {"column_type": "lookup", "path": "tarifs_1", "field": "tarifs_1", "lookup_field": "saison", "entity": "Tarifs", "type": "list", "required": false}]}} dataBinding={{"entity": "Materielsprestations", "endpoint": "/materielsprestations/"}} />
        <div id="iyvp63" style={{"marginTop": "20px", "display": "flex", "gap": "10px", "flexWrap": "wrap", "--chart-color-palette": "default"}}>
          <MethodButton id="i6cvuz" className="action-button-component" style={{"display": "inline-flex", "alignItems": "center", "padding": "6px 14px", "background": "linear-gradient(90deg, #2563eb 0%, #1e40af 100%)", "color": "#fff", "textDecoration": "none", "borderRadius": "4px", "fontSize": "13px", "fontWeight": "600", "letterSpacing": "0.01em", "cursor": "pointer", "border": "none", "boxShadow": "0 1px 4px rgba(37,99,235,0.10)", "transition": "background 0.2s", "--chart-color-palette": "default"}} endpoint="/materielsprestations/{materielsprestations_id}/methods/verifierStockDisponible/" label="+ verifierStockDisponible" parameters={[{"name": "quantiteDemandee", "type": "int", "required": true}]} isInstanceMethod={true} instanceSourceTableId="table-materielsprestations-4" />
        </div>
      </main>
    </div>    </div>
  );
};

export default Materielsprestations;
