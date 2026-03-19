import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";

const Centredecongres: React.FC = () => {
  return (
    <div id="page-centredecongres-7">
    <div id="i6pyfb" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="idzm5w" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="i3lnry" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="iqi5of" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}}>
          <a id="iup2ex" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/gestionnaire">{"Gestionnaire"}</a>
          <a id="ipud9o" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/stats">{"Stats"}</a>
          <a id="ijtd3z" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/reservation">{"Reservation"}</a>
          <a id="iwi5vs" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/disponibilites">{"Disponibilites"}</a>
          <a id="ikj3hk" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/materielsprestations">{"Materielsprestations"}</a>
          <a id="ipzm1u" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/evenementsalle">{"EvenementSalle"}</a>
          <a id="ia9xkq" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/tarifs">{"Tarifs"}</a>
          <a id="i2x1xf" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "rgba(255,255,255,0.2)", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/centredecongres">{"CentredeCongres"}</a>
        </div>
        <p id="ilwqsk" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="iubez2" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="iqlfjm" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"CentredeCongres"}</h1>
        <p id="iiwdrj" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"Manage CentredeCongres data"}</p>
        <TableBlock id="table-centredecongres-7" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="CentredeCongres List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "Nom", "column_type": "field", "field": "nom", "type": "str", "required": true}, {"label": "Adresse", "column_type": "field", "field": "adresse", "type": "str", "required": true}], "formColumns": [{"column_type": "field", "field": "nom", "label": "nom", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "adresse", "label": "adresse", "type": "str", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "gestionnaire_1", "field": "gestionnaire_1", "lookup_field": "identifiant", "entity": "Gestionnaire", "type": "str", "required": true}, {"column_type": "lookup", "path": "evenementsalle_1", "field": "evenementsalle_1", "lookup_field": "nom", "entity": "EvenementSalle", "type": "list", "required": false}]}} dataBinding={{"entity": "CentredeCongres", "endpoint": "/centredecongres/"}} />
      </main>
    </div>    </div>
  );
};

export default Centredecongres;
