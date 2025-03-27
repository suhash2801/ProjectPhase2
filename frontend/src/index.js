import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import { BrowserRouter, Switch, Route } from "react-router-dom";
import Blockchain from "./components/Blockchain";
import ConductTransaction from "./components/ConductTransaction";
import App from "./components/App";
import TransactionPool from "./components/TransactionPool";

const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
  <BrowserRouter>
    <Switch>
      <Route path="/" exact component={App} />
      <Route path="/blockchain" component={Blockchain} />
      <Route path="/conduct-transaction" component={ConductTransaction} />
      <Route path="/transaction-pool" component={TransactionPool} />

    </Switch>
  </BrowserRouter>
);
