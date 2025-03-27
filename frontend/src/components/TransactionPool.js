import React, {useState,useEffect} from "react";
import { Link } from "react-router-dom/cjs/react-router-dom.min";
import Transaction from "./Transaction";
import { API_BASE_URL, SECONDS_JS } from "../config";
import { Button } from "react-bootstrap";

const POLL_INTERVAL=10*SECONDS_JS

function TransactionPool(){
    const [transactions,setTransactions]=useState([])

    const fetchTransactions=()=>{
        fetch(`${API_BASE_URL}/transactions`)
        .then(response =>response.json())
        .then(json=> {
            console.log ('transactions json' ,json)
            setTransactions(json)});

    }


    const fetchMineBlock=()=>{
        fetch (`${API_BASE_URL}/blockchain/mine`)
        .then(()=>{
            alert('Success');
        })
    }

    useEffect( ()=>{
        fetchTransactions();
        const intervalID= setInterval(fetchTransactions,POLL_INTERVAL);
        return()=> clearInterval(intervalID);
    },[]);



    return (
        <div className="TransactionPool">
            <Link to="/">Home</Link>
            <hr/>
            <h3>Transaction Pool</h3>
            <div>
                {
                    transactions.map(transaction =>(
                        <div key={transaction.id}>
                            <hr/>
                            <Transaction transaction={transaction}/>
                        </div>
                    ))
                }
            </div>
            <hr/>
            <Button variant="danger" onClick={fetchMineBlock}>
                MineBlock
            </Button>
        </div>
    )
}




export default TransactionPool