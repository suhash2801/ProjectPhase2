import React, { useState } from "react";
import { Button } from 'react-bootstrap';
import { MILLISECONDS_PYTHON } from "../config";
import Transaction from "./Transaction";

function ToggleTransactionDisplay({ block }) {
    const [displayTransaction, setDisplayTransaction] = useState(false);
    const { data } = block;

    const toggleDisplayTransaction = () => {
        setDisplayTransaction(!displayTransaction);
    };

    if (displayTransaction) {
        return (
            <div>
                {data.map(transaction => (
                    <div key={transaction.id}>
                        <hr />
                        <Transaction transaction={transaction} />
                        {transaction.chip_info && (
                            <div>
                                <strong>Chip Info:</strong><br/>
                                <hr/><hr/>
                                    ID: {transaction.chip_info.chip_id}<br/>
                                    Make: {transaction.chip_info.chip_make}<br/>
                                    Status: {transaction.chip_info.current_status}<br/>
                                
                            </div>
                        )}
                    </div>
                ))}
                <br />
                <Button variant="danger" size="sm" onClick={toggleDisplayTransaction}>
                    Show Less
                </Button>
            </div>
        );
    }
    
    return (
        <div>
            <br />
            <Button variant="danger" size="sm" onClick={toggleDisplayTransaction}>
                Show More
            </Button>
        </div>
    );
}

function Block({ block }) {
    const { timestamp, hash, data } = block;
    const hashDisplay = `${hash.substring(0, 15)}...`;
    const timestampDisplay = new Date(timestamp / MILLISECONDS_PYTHON).toLocaleString();

    return (
        <div className="Block">
            <div>Hash: {hashDisplay}</div>
            <div>Timestamp: {timestampDisplay}</div>
            <ToggleTransactionDisplay block={block} />
        </div>
    );
}

export default Block;
