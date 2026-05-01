import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer
} from "recharts";

const API = "http://127.0.0.1:8000/api";

export default function App() {
  const [revenue, setRevenue] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchData() {
      try {
        const [rev, cust] = await Promise.all([
          axios.get(`${API}/revenue`),
          axios.get(`${API}/top-customers`)
        ]);

        setRevenue(rev.data);
        setCustomers(cust.data);
      } catch (err) {
        setError("Failed to load data");
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) return <h2>Loading...</h2>;
  if (error) return <h2>{error}</h2>;

  return (
    <div style={{ padding: "20px" }}>
      <h2>Revenue Trend</h2>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={revenue}>
          <XAxis dataKey="order_year_month" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="amount" />
        </LineChart>
      </ResponsiveContainer>

      <h2>Top Customers</h2>
      <input
        placeholder="Search..."
        onChange={(e) => {
          const val = e.target.value.toLowerCase();
          setCustomers((prev) =>
            prev.filter(c => c.name.toLowerCase().includes(val))
          );
        }}
      />

      <table border="1" width="100%">
        <thead>
          <tr>
            <th>Name</th>
            <th>Region</th>
            <th>Spend</th>
            <th>Churned</th>
          </tr>
        </thead>
        <tbody>
          {customers.map((c, i) => (
            <tr key={i}>
              <td>{c.name}</td>
              <td>{c.region}</td>
              <td>{c.total_spend}</td>
              <td>{c.churned ? "Yes" : "No"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}