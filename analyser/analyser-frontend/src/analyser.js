import React, { useEffect, useState } from "react";
import axios from "axios";

const AccountAnalysis = () => {
    const [transactions, setTransactions] = useState([]);

    useEffect(() => {
        axios.get("http://localhost:8000/api/transactions/")
            .then(res => setTransactions(res.data))
            .catch(err => console.error(err));
    }, []);

    return (
        <div className="p-4">
            <h1 className="text-xl font-bold mb-4">Account Analysis</h1>
            <table className="table-auto w-full border-collapse border border-gray-400">
                <thead>
                    <tr>
                        <th className="border border-gray-400 px-4 py-2">Date</th>
                        <th className="border border-gray-400 px-4 py-2">Description</th>
                        <th className="border border-gray-400 px-4 py-2">Amount</th>
                        <th className="border border-gray-400 px-4 py-2">Type</th>
                    </tr>
                </thead>
                <tbody>
                    {transactions.map(txn => (
                        <tr key={txn.id}>
                            <td className="border border-gray-400 px-4 py-2">{txn.date}</td>
                            <td className="border border-gray-400 px-4 py-2">{txn.description}</td>
                            <td className="border border-gray-400 px-4 py-2">{txn.amount}</td>
                            <td className="border border-gray-400 px-4 py-2">{txn.transaction_type}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default AccountAnalysis;