import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";
import { MethodButton } from "../components/MethodButton";

const Disponibilites: React.FC = () => {
  return (
    <div id="page-disponibilites-3">
    <div id="i9czj4" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="ibnd77" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="i69j8w" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="ij6h1w" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}}>
          <a id="iu36q1" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/gestionnaire">{"Gestionnaire"}</a>
          <a id="imou6g" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/stats">{"Stats"}</a>
          <a id="izkl8h" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/reservation">{"Reservation"}</a>
          <a id="itwspg" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "rgba(255,255,255,0.2)", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/disponibilites">{"Disponibilites"}</a>
          <a id="ilbygx" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/materielsprestations">{"Materielsprestations"}</a>
          <a id="i7d4b5" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/evenementsalle">{"EvenementSalle"}</a>
          <a id="ihkh91" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/tarifs">{"Tarifs"}</a>
          <a id="izucsd" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/centredecongres">{"CentredeCongres"}</a>
        </div>
        <p id="ib14i9" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="iyc55k" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="ip1bzi" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"Disponibilites"}</h1>
        <p id="iygiux" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"Manage Disponibilites data"}</p>
        <TableBlock id="table-disponibilites-3" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Disponibilites List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "MotifDisponibilite", "column_type": "field", "field": "motifDisponibilite", "type": "str", "required": true}, {"label": "DateDebut", "column_type": "field", "field": "dateDebut", "type": "date", "required": true}, {"label": "DateFin", "column_type": "field", "field": "dateFin", "type": "date", "required": true}, {"label": "DureeMinim", "column_type": "field", "field": "dureeMinim", "type": "int", "required": true}], "formColumns": [{"column_type": "field", "field": "motifDisponibilite", "label": "motifDisponibilite", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "dateDebut", "label": "dateDebut", "type": "date", "required": true, "defaultValue": null}, {"column_type": "field", "field": "dateFin", "label": "dateFin", "type": "date", "required": true, "defaultValue": null}, {"column_type": "field", "field": "dureeMinim", "label": "dureeMinim", "type": "int", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "reservation_2", "field": "reservation_2", "lookup_field": "nomEvenement", "entity": "Reservation", "type": "list", "required": true}]}} dataBinding={{"entity": "Disponibilites", "endpoint": "/disponibilites/"}} />
        <div id="i6qor7" style={{"marginTop": "20px", "display": "flex", "gap": "10px", "flexWrap": "wrap", "--chart-color-palette": "default"}}>
          <MethodButton id="i5u8tk" className="action-button-component" style={{"display": "inline-flex", "alignItems": "center", "padding": "6px 14px", "background": "linear-gradient(90deg, #2563eb 0%, #1e40af 100%)", "color": "#fff", "textDecoration": "none", "borderRadius": "4px", "fontSize": "13px", "fontWeight": "600", "letterSpacing": "0.01em", "cursor": "pointer", "border": "none", "boxShadow": "0 1px 4px rgba(37,99,235,0.10)", "transition": "background 0.2s", "--chart-color-palette": "default"}} endpoint="/disponibilites/{disponibilites_id}/methods/ajouterIndisponibilite/" label="+ ajouterIndisponibilite" parameters={[{"name": "motif", "type": "any", "required": true}, {"name": "debut", "type": "any", "required": true}, {"name": "fin", "type": "any", "required": true}]} isInstanceMethod={true} instanceSourceTableId="table-disponibilites-3" />
        </div>
      </main>
    </div>    </div>
  );
};

export default Disponibilites;
