import React, { useEffect, useState } from "react";
import { FormGroup, FormControl, Button, FormSelect } from "react-bootstrap";
import { API_BASE_URL } from "../config";
import { Link } from "react-router-dom/cjs/react-router-dom.min";

function ConductTransaction() {
    const [amount, setAmount] = useState(0);
    const [recipient, setRecipient] = useState('');
    const [chipId, setChipId] = useState('');
    const [chipMake, setChipMake] = useState('');
    const [currentStatus, setCurrentStatus] = useState('active'); // Default to 'active'
    const [knownAddresses, setKnownAddresses] = useState([]);

    useEffect(() => {
        fetch(`${API_BASE_URL}/known-addresses`)
            .then(response => response.json())
            .then(json => setKnownAddresses(json));
    }, []);

    const updateRecipient = event => setRecipient(event.target.value);
    const updateAmount = event => setAmount(Number(event.target.value));
    const updateChipId = event => setChipId(event.target.value);
    const updateChipMake = event => setChipMake(event.target.value);
    const updateCurrentStatus = event => setCurrentStatus(event.target.value);

    const submitTransaction = () => {
        fetch(`${API_BASE_URL}/wallet/transact`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                recipient,
                amount,
                chip_info: {
                    chip_id: chipId,
                    chip_make: chipMake,
                    current_status: currentStatus
                }
            })
        }).then(response => response.json())
            .then(json => {
                console.log('submitTransaction json', json);
                alert('Success');
            });
    };

    return (
        <div className="ConductTransaction">
            <Link to="/">Home</Link>
            <hr />
            <h3>Conduct a Transaction</h3>
            <br />
            <FormGroup>
                <FormControl
                    input="text"
                    placeholder="Recipient"
                    value={recipient}
                    onChange={updateRecipient} />
            </FormGroup>
            <br />
            <FormGroup>
                <FormControl
                    input="number"
                    placeholder="Amount"
                    value={amount}
                    onChange={updateAmount} />
            </FormGroup>
            <br />
            <h3>Chip Information</h3>
            <FormGroup>
                <FormControl
                    input="text"
                    placeholder="Chip ID"
                    value={chipId}
                    onChange={updateChipId} />
            </FormGroup>
            <br />
            <FormGroup>
                <FormControl
                    input="text"
                    placeholder="Chip Make"
                    value={chipMake}
                    onChange={updateChipMake} />
            </FormGroup>
            <br />
            <FormGroup>
                <FormSelect style={{ color: "black" }} value={currentStatus}  onChange={updateCurrentStatus}>
                    <option value="active">Active</option>
                    <option value="inactive (not in use)">Inactive (Not in Use)</option>
                    <option value="inactive (expired)">Inactive (Expired)</option>
                </FormSelect>
            </FormGroup>
            <br />
            <div>
                <Button variant="danger" onClick={submitTransaction}>Submit</Button>
            </div>
            <br />
            <h4>Known Addresses</h4>
            <div>
                {knownAddresses.map((address, i) => (
                    <span key={address}>
                        <u>{address}</u>{i !== knownAddresses.length - 1 ? ', ' : ''}
                    </span>
                ))}
            </div>
        </div>
    );
}

export default ConductTransaction;
