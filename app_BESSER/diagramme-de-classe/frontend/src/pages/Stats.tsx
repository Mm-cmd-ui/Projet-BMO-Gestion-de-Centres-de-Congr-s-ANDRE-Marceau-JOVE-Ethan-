import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";
import { MethodButton } from "../components/MethodButton";

const Stats: React.FC = () => {
  return (
    <div id="page-stats-1">
    <div id="i4ebe" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="irf97" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="irh1p" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="ishso" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}}>
          <a id="iyrll" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/gestionnaire">{"Gestionnaire"}</a>
          <a id="iqs9u" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "rgba(255,255,255,0.2)", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/stats">{"Stats"}</a>
          <a id="igs1h" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/reservation">{"Reservation"}</a>
          <a id="iq484" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/disponibilites">{"Disponibilites"}</a>
          <a id="idcki" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/materielsprestations">{"Materielsprestations"}</a>
          <a id="inf9e" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/evenementsalle">{"EvenementSalle"}</a>
          <a id="iidbf" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/tarifs">{"Tarifs"}</a>
          <a id="i4kjj" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/centredecongres">{"CentredeCongres"}</a>
        </div>
        <p id="isgif" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="izgkd" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="icsvb" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"Stats"}</h1>
        <p id="i9ugx" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"Manage Stats data"}</p>
        <TableBlock id="table-stats-1" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Stats List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "ChiffresAffaires", "column_type": "field", "field": "chiffresAffaires", "type": "float", "required": true}, {"label": "TauxOccupation", "column_type": "field", "field": "tauxOccupation", "type": "float", "required": true}, {"label": "Periode", "column_type": "field", "field": "periode", "type": "str", "required": true}], "formColumns": [{"column_type": "field", "field": "chiffresAffaires", "label": "chiffresAffaires", "type": "float", "required": true, "defaultValue": null}, {"column_type": "field", "field": "tauxOccupation", "label": "tauxOccupation", "type": "float", "required": true, "defaultValue": null}, {"column_type": "field", "field": "periode", "label": "periode", "type": "str", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "gestionnaire_2", "field": "gestionnaire_2", "lookup_field": "identifiant", "entity": "Gestionnaire", "type": "str", "required": false}]}} dataBinding={{"entity": "Stats", "endpoint": "/stats/"}} />
        <div id="i9ki2" style={{"marginTop": "20px", "display": "flex", "gap": "10px", "flexWrap": "wrap", "--chart-color-palette": "default"}}>
          <MethodButton id="i3tai" className="action-button-component" style={{"display": "inline-flex", "alignItems": "center", "padding": "6px 14px", "background": "linear-gradient(90deg, #2563eb 0%, #1e40af 100%)", "color": "#fff", "textDecoration": "none", "borderRadius": "4px", "fontSize": "13px", "fontWeight": "600", "letterSpacing": "0.01em", "cursor": "pointer", "border": "none", "boxShadow": "0 1px 4px rgba(37,99,235,0.10)", "transition": "background 0.2s", "--chart-color-palette": "default"}} endpoint="/stats/{stats_id}/methods/calculerCA/" label="+ calculerCA" isInstanceMethod={true} instanceSourceTableId="table-stats-1" />
        </div>
      </main>
    </div>    </div>
  );
};

export default Stats;
