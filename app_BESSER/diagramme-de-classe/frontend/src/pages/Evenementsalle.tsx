import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";
import { MethodButton } from "../components/MethodButton";

const Evenementsalle: React.FC = () => {
  return (
    <div id="page-evenementsalle-5">
    <div id="ixhd2f" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="iq9w08" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="i0srv5" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="itj4l7" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}}>
          <a id="id5wnr" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/gestionnaire">{"Gestionnaire"}</a>
          <a id="i06e2y" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/stats">{"Stats"}</a>
          <a id="ircqg7" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/reservation">{"Reservation"}</a>
          <a id="ir0jsh" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/disponibilites">{"Disponibilites"}</a>
          <a id="ij2rek" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/materielsprestations">{"Materielsprestations"}</a>
          <a id="ied0p2" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "rgba(255,255,255,0.2)", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/evenementsalle">{"EvenementSalle"}</a>
          <a id="idrfvk" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/tarifs">{"Tarifs"}</a>
          <a id="itpx2u" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/centredecongres">{"CentredeCongres"}</a>
        </div>
        <p id="i55pxk" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="i6t9oa" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="iqru4z" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"EvenementSalle"}</h1>
        <p id="i9a972" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"Manage EvenementSalle data"}</p>
        <TableBlock id="table-evenementsalle-5" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="EvenementSalle List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "Nom", "column_type": "field", "field": "nom", "type": "str", "required": true}, {"label": "CapaciteMax", "column_type": "field", "field": "capaciteMax", "type": "int", "required": true}, {"label": "TypeElement", "column_type": "field", "field": "typeElement", "type": "str", "required": true}], "formColumns": [{"column_type": "field", "field": "nom", "label": "nom", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "capaciteMax", "label": "capaciteMax", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "typeElement", "label": "typeElement", "type": "str", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "centredecongres", "field": "centredecongres", "lookup_field": "nom", "entity": "CentredeCongres", "type": "str", "required": false}, {"column_type": "lookup", "path": "tarifs", "field": "tarifs", "lookup_field": "saison", "entity": "Tarifs", "type": "list", "required": false}, {"column_type": "lookup", "path": "reservation", "field": "reservation", "lookup_field": "delaiConfirmation", "entity": "Reservation", "type": "str", "required": false}]}} dataBinding={{"entity": "EvenementSalle", "endpoint": "/evenementsalle/"}} />
        <div id="ilt67h" style={{"marginTop": "20px", "display": "flex", "gap": "10px", "flexWrap": "wrap", "--chart-color-palette": "default"}}>
          <MethodButton id="i85gll" className="action-button-component" style={{"display": "inline-flex", "alignItems": "center", "padding": "6px 14px", "background": "linear-gradient(90deg, #2563eb 0%, #1e40af 100%)", "color": "#fff", "textDecoration": "none", "borderRadius": "4px", "fontSize": "13px", "fontWeight": "600", "letterSpacing": "0.01em", "cursor": "pointer", "border": "none", "boxShadow": "0 1px 4px rgba(37,99,235,0.10)", "transition": "background 0.2s", "--chart-color-palette": "default"}} endpoint="/evenementsalle/{evenementsalle_id}/methods/verifierCapacite/" label="+ verifierCapacite" parameters={[{"name": "nb_a_tester", "type": "any", "required": true}]} isInstanceMethod={true} instanceSourceTableId="table-evenementsalle-5" />
        </div>
      </main>
    </div>    </div>
  );
};

export default Evenementsalle;
