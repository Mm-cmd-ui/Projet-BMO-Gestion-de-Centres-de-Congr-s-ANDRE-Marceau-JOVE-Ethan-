import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";
import { MethodButton } from "../components/MethodButton";

const EvenementSalle: React.FC = () => {
  return (
    <div id="page-evenement_salle-2">
    <div id="iai8y" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="iwmcx" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="iezrd" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="i419h" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}}>
          <a id="ig91s" className="reservation" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/gestionnaire">{"gestionnaire"}</a>
          <a id="i6uuj" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/reservation">{"reservation"}</a>
          <a id="i373y" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "rgba(255,255,255,0.2)", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/evenement_salle">{"Evenement_Salle"}</a>
        </div>
        <p id="idu3h" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="iq4p1" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="i664t" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"Evenement_Salle"}</h1>
        <p id="ih4qu" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"Manage Evenement_Salle data"}</p>
        <TableBlock id="table-evenement_salle-2" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Evenement_Salle List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "Nom", "column_type": "field", "field": "nom", "type": "str", "required": true}, {"label": "CapaciteMax", "column_type": "field", "field": "capaciteMax", "type": "int", "required": true}, {"label": "TypeElement", "column_type": "field", "field": "typeElement", "type": "str", "required": true}], "formColumns": [{"column_type": "field", "field": "nom", "label": "nom", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "capaciteMax", "label": "capaciteMax", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "typeElement", "label": "typeElement", "type": "str", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "reservation_1", "field": "reservation_1", "lookup_field": "nomEvenement", "entity": "reservation", "type": "str", "required": false}]}} dataBinding={{"entity": "Evenement_Salle", "endpoint": "/evenement_salle/"}} />
        <div id="imgvb" style={{"marginTop": "20px", "display": "flex", "gap": "10px", "flexWrap": "wrap", "--chart-color-palette": "default"}}>
          <MethodButton id="iapr3" className="action-button-component" style={{"display": "inline-flex", "alignItems": "center", "padding": "6px 14px", "background": "linear-gradient(90deg, #2563eb 0%, #1e40af 100%)", "color": "#fff", "textDecoration": "none", "borderRadius": "4px", "fontSize": "13px", "fontWeight": "600", "letterSpacing": "0.01em", "cursor": "pointer", "border": "none", "boxShadow": "0 1px 4px rgba(37,99,235,0.10)", "transition": "background 0.2s", "--chart-color-palette": "default"}} endpoint="/evenement_salle/{evenement_salle_id}/methods/verifierCapacite/" label="+ verifierCapacite" parameters={[{"name": "nb_a_tester", "type": "any", "required": true}]} isInstanceMethod={true} instanceSourceTableId="table-evenement_salle-2" />
        </div>
      </main>
    </div>    </div>
  );
};

export default EvenementSalle;
